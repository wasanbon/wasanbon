import os, sys, time, subprocess, signal
from ctypes import *
from rtshell import rtstart, rtresurrect, rtstop

import wasanbon

SIGSET_NWORDS = 1024 / (8 * sizeof(c_ulong))

class SIGSET(Structure):
    _fields_ = [
        ('val', c_ulong * SIGSET_NWORDS)
    ]

sigs = (c_ulong * SIGSET_NWORDS)()
sigs[0] = 2 ** (signal.SIGINT - 1)
mask = SIGSET(sigs)

if sys.platform == 'darwin':
    libc = CDLL('libc.dylib')
elif sys.platform == 'linux2':
    libc = CDLL('libc.so.6')

def handle(sig, _):
    if sig == signal.SIGINT:
        pass

def disable_sig():
    '''Mask the SIGINT in the child process'''
    SIG_BLOCK = 0
    libc.sigprocmask(SIG_BLOCK, pointer(mask), 0)

def start_rtcd(pkg, language, filepath, verbose=False):
    if language == 'C++':
        return start_cpp_rtcd(filepath, verbose=verbose)
    elif language == 'Java':
        return start_java_rtcd(pkg, filepath, verbose=verbose)
    elif language == 'Python':
        return start_python_rtcd(filepath, verbose=verbose)
    else:
        raise wasanbon.UnsupportedPlatformException()

def start_cpp_rtcd(filepath, verbose=True):
    if verbose:
        sys.stdout.write(' - Starting C++ rtcd.\n')
    args = {}
    args['env'] = os.environ.copy()
    args['preexec_fn'] = None if sys.platform == 'win32' else disable_sig
    args['stdout'] = None if verbose else subprocess.PIPE
    args['stdin'] = None if verbose else subprocess.PIPE
    if sys.platform == 'win32':
        args['creationflags'] = 512
    cmd = ['rtcd', '-f', filepath]
    return subprocess.Popen(cmd, **args)

def start_python_rtcd(filepath, verbose=False):
    if verbose:
        sys.stdout.write(' - Starting Python rtcd.\n')
    args = {}
    args['env'] = os.environ.copy()
    args['preexec_fn'] = None if sys.platform == 'win32' else disable_sig
    args['stdout'] = None if verbose else subprocess.PIPE
    args['stdin'] = None if verbose else subprocess.PIPE
    #args['stdin'] = subprocess.PIPE
    if sys.platform == 'win32':
        args['creationflags'] = 512
    if sys.platform == 'win32':
        for path in sys.path:
            if os.path.isfile(os.path.join(path, 'python.exe')):
                exe = os.path.join(path, 'python.exe')
                file = os.path.join(path, 'rtcd.py')
                cmd = [exe, file, '-f', filepath]
                break
    else:
        cmd = ['rtcd_python', '-f', filepath]
    p = subprocess.Popen(cmd, **args)
    #p.stdin.write('N\n')
    return p
 
def start_java_rtcd(pkg, filepath, verbose=False):
    if verbose:
        sys.stdout.write(' - Starting Java rtcd.\n')

    args = {}
    #args['env'] = os.environ.copy()
    args['preexec_fn'] = None if sys.platform == 'win32' else disable_sig
    args['stdout'] = None if verbose else subprocess.PIPE
    args['stdin'] = None if verbose else subprocess.PIPE
    if sys.platform == 'win32':
        args['creationflags'] = 512


    rtm_java_classpath = os.path.join(wasanbon.rtm_home(), 'jar')
    java_env = os.environ.copy()
    if not "CLASSPATH" in java_env.keys():
        java_env["CLASSPATH"]=os.getcwd() 
    if sys.platform == 'win32':
        sep = ';'
    else:
        sep = ':'
    for jarfile in os.listdir(rtm_java_classpath):
        java_env["CLASSPATH"]=java_env["CLASSPATH"] + sep + os.path.join(rtm_java_classpath, jarfile)
    #java_env["CLASSPATH"]=java_env["CLASSPATH"] + ':bin/LeapTest.jar'

    rtm_jars = [j for j in os.listdir(rtm_java_classpath) if j.endswith('.jar')]
    for r in pkg.rtcs:
        if os.path.isdir(os.path.join(r.path, 'jar')):
            for jarfile in [j for j in os.listdir(os.path.join(r.path, 'jar')) if j.endswith('.jar')]:
                if not jarfile in rtm_jars:
                    java_env["CLASSPATH"]=java_env["CLASSPATH"] + sep + os.path.join(r.path, 'jar', jarfile)

    #print java_env

    args['env'] = java_env
    
    cmd = [wasanbon.setting()['local']['java'], 'rtcd.rtcd', '-f', filepath]
    return subprocess.Popen(cmd, **args)


def exe_rtresurrect(file=None):
    if not file:
        file = wasanbon.setting()['application']['system']
    return rtresurrect.main([file]) == 0

def cmd_rtresurrect():
    if sys.platform == 'win32':
        cmd = ['rtresurrect.bat', wasanbon.setting()['application']['system']]
    else:
        cmd = ['rtresurrect', wasanbon.setting()['application']['system']]
    while True:
        p = subprocess.Popen(cmd)
        if p.wait() == 0:
            break;
        time.sleep(1)

def exe_rtstart(file=None):
    if not file:
        file = wasanbon.setting()['application']['system']
    return rtstart.main([file]) == 0

def exe_rtstop(file=None):
    if not file:
        file = wasanbon.setting()['application']['system']
    return rtstop.main([file]) == 0

def cmd_rtstart(file=None):
    if not file:
        file = wasanbon.setting()['application']['system']
    
    if sys.platform == 'win32':
        cmd = ['rtstart.bat', file]
    else:
        cmd = ['rtstart', file]
    while True:
        p = subprocess.Popen(cmd)
        if p.wait() == 0:
            break;
        time.sleep(1)

