import os, sys, subprocess, time, signal
from ctypes import *
import rtctree


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


def launch_nameserver(verbose=False, port='2809', force=False):
    if verbose:
        sys.stdout.write(' - Starting Nameserver \n')

    pstdout = None if verbose else subprocess.PIPE 
    pstderr = None if verbose else subprocess.PIPE
    pstdin = subprocess.PIPE
    if sys.platform == 'win32':
        path = os.path.join(os.environ['RTM_ROOT'], 'bin', 'rtm-naming.bat')
        cmd = [path, port]
        creationflag = 512
        preexec_fn = None
    else:
        cmd = ['rtm-naming', port]
        creationflag = 0
        preexec_fn = disable_sig
    if verbose:
        print ' - Command = %s' % cmd
    p = subprocess.Popen(cmd, creationflags=creationflag, stdout=pstdout, stdin=pstdin, stderr=pstderr, preexec_fn=preexec_fn)
    if force:
        p.stdin.write('y\n')
    return p



def is_nameserver_running(ns, try_count=3, verbose=False):
    if not ns.startswith('/'):
        ns = '/' + ns.strip()
    if verbose:
        sys.stdout.write(" - Checking the NameServer (%s)\n" % ns)
    for i in range(0, try_count):
        try:
            if verbose:
                sys.stdout.write(' - rtctree.path.parse_path(%s)\n' % ns)
            path, port = rtctree.path.parse_path(ns)
            tree = rtctree.tree.RTCTree(paths=path, filter=[path])
            dir_node = tree.get_node(path)
            if verbose:
                sys.stdout.write(' - Nameserver found.\n')
            return True
            break
        except rtctree.exceptions.InvalidServiceError, e:
            continue
        except omniORB.CORBA.OBJECT_NOT_EXIST, e:
            continue
    if verbose:
        sys.stdout.write(' - Nameserver NOT found.\n')
    return False
