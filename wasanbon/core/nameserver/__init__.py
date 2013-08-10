import os, sys, subprocess
import rtctree



def launch_nameserver(ns, verbose=False):
    if vrerbose:
        sys.stdout.write(' - Starting Nameserver %s\n' % ns)

    if ns.startswith('/'):
        ns = ns[1:]
    token = ns.split(':')
    if len(token) == 1:
        addr = token[0].strip()
        port = 2809
    else:
        addr = token[0].strip()
        port = token[1].strip()
        
    if addr == 'localhost' or addr == '127.0.0.1':
        pstdout = None if verbose else subprocess.PIPE 
        pstdin = None if verbose else subprocess.PIPE

        if sys.platform == 'win32':
            path = os.path.join(os.environ['RTM_ROOT'], 'bin', 'rtm-naming.bat')
            cmd = [path, port]
            creationflag = 512
        else:
            cmd = ['rtm-naming', port]
            creationflag = 0

        if verbose:
            print ' - Command = %s' % cmd
        p = subprocess.Popen(cmd, creationflags=creationflag, stdout=pstdout, stdin=pstdin)
        for i in range(0,5):
            time.sleep(1)
        if verbose:
            print ' - Starting Nameservice okay.'
        return p
    return None


def is_nameserver_launched(ns, try_count=3, verbose=False):
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
