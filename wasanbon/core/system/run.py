import os, sys, time, subprocess, signal
from ctypes import *
from rtshell import rtstart, rtresurrect

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

def start_cpp_rtcd():
    cpp_env = os.environ.copy()

    if sys.platform == 'win32':
        return subprocess.Popen(['rtcd', '-f', 'conf/rtc_cpp.conf'], env=cpp_env, creationflags=512, stdout=subprocess.PIPE)
    else:
        return subprocess.Popen(['rtcd', '-f', 'conf/rtc_cpp.conf'], env=cpp_env, preexec_fn=disable_sig)


def start_python_rtcd():
    py_env = os.environ.copy()
    if sys.platform == 'win32':
        for path in sys.path:
            if os.path.isfile(os.path.join(path, 'python.exe')):
                cmd = os.path.join(path, 'python.exe')
                file = os.path.join(path, 'rtcd.py')
        p = subprocess.Popen([cmd, file, '-f', 'conf/rtc_py.conf'], env=py_env, creationflags=512, stdin=subprocess.PIPE)
        p.stdin.write('N')
        return p
    else:
        return subprocess.Popen(['rtcd_python', '-f', 'conf/rtc_py.conf'], env=py_env, preexec_fn=disable_sig)
 

def start_java_rtcd():
    rtm_java_classpath = os.path.join(wasanbon.rtm_home, 'jar')
    java_env = os.environ.copy()
    if not "CLASSPATH" in java_env.keys():
        java_env["CLASSPATH"]=os.getcwd() 
    if sys.platform == 'win32':
        sep = ';'
    else:
        sep = ':'
    for jarfile in os.listdir(rtm_java_classpath):
        java_env["CLASSPATH"]=java_env["CLASSPATH"] + sep + os.path.join(rtm_java_classpath, jarfile)
    if sys.platform == 'win32':
        return subprocess.Popen([wasanbon.setting['local']['java'], 'rtcd.rtcd', '-f', 'conf/rtc_java.conf'], env=java_env, creationflags=512)
    else:
        #print java_env["CLASSPATH"]
        return subprocess.Popen([wasanbon.setting['local']['java'], 'rtcd.rtcd', '-f', 'conf/rtc_java.conf'], env=java_env)

def exe_rtresurrect():
    return rtresurrect.main([wasanbon.setting['application']['system']]) == 0

def cmd_rtresurrect():
    if sys.platform == 'win32':
        cmd = ['rtresurrect.bat', wasanbon.setting['application']['system']]
    else:
        cmd = ['rtresurrect', wasanbon.setting['application']['system']]
    while True:
        p = subprocess.Popen(cmd)
        if p.wait() == 0:
            break;
        time.sleep(1)

def exe_rtstart():
    return rtstart.main([wasanbon.setting['application']['system']]) == 0

def cmd_rtstart():

    if sys.platform == 'win32':
        cmd = ['rtstart.bat', wasanbon.setting['application']['system']]
    else:
        cmd = ['rtstart', wasanbon.setting['application']['system']]
        
    while True:
        p = subprocess.Popen(cmd)
        if p.wait() == 0:
            break;
        time.sleep(1)

