import os, sys, subprocess, time, signal, psutil,threading
from wasanbon.core.nameserver.rtc_ref import *
from ctypes import *
import rtctree
import omniORB

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




class NameService(object):

    def __init__(self, path):
        if path.find(':') < 0:
            path = path.strip() + ':2809'
        if path.strip().startswith('/'):
            path = path.strip()[1:]
        self._path = path
        self._process = None
        self._rtcs = None
        self.tree = None

    @property
    def path(self):
        return self._path

    @property
    def address(self):
        return self._path.split(':')[0].strip()

    @property
    def port(self):
        return self._path.split(':')[1].strip()

    def check_and_launch(self,verbose=False, force=False):
        if self.address != 'localhost' or self.address != '127.0.0.1':
            if force or not self.is_running(verbose=verbose):
                self.launch(verbose=verbose, force=force)

                for i in range(0, 5):
                    if verbose:
                        sys.stdout.write(' - Starting Nameserver %s. Please Wait %s seconds.\n' % (self.path, 4-i))
                    time.sleep(1)
        return self.is_running(verbose=verbose)

    def is_running(self, verbose=False, try_count=3):
        for i in range(0, try_count):
            try:
                if verbose:
                    sys.stdout.write(' - Checking Nameservice(%s) is running\n' % self.path)
                if not self.tree:
                    if verbose:
                        sys.stdout.write('   - Parsing path....\n')
                    self.__path, self.__port = rtctree.path.parse_path('/' + self.path)
                    if verbose:
                        sys.stdout.write('   - Initializing rtctree...\n')
                    # Here is blocking point ....
                    class Task(threading.Thread):
                        def __init__(self, ns, path):
                            threading.Thread.__init__(self)
                            self.ns = ns
                            self.__path = path
                        def run(self):
                            try:
                                self.ns.tree = rtctree.tree.RTCTree(paths=self.__path, filter=[self.__path])
                            except:
                                pass
                        def quit(self):
                            self._Thread__stop()
                    
                    self.tree = False
                    t = Task(self, self.__path)
                    t.start()
                    def killtask():
                        t.quit()
                    wdt = threading.Timer(3.0, killtask)
                    wdt.start()
                    t.join()
                    if not self.tree:
                        sys.stdout.write('   - Failed.\n')
                        continue
                    #self.tree = rtctree.tree.RTCTree(paths=self.__path, filter=[self.__path])
                    if verbose:
                        sys.stdout.write('   - Getting Node...\n')
                    self.dir_node = self.tree.get_node(self.__path)
                    if verbose:
                        sys.stdout.write('   - success.\n')
                if verbose:
                    sys.stdout.write(' - Nameservice(%s) is found.\n' % self.path)
                return True
            except rtctree.exceptions.InvalidServiceError, e:
                continue
            except omniORB.CORBA.OBJECT_NOT_EXIST, e:
                continue
        if verbose:
            sys.stdout.write(' - Nameservice not found.\n')
        return False
            

    def launch(self, verbose=False, force=False):

        if self.address != 'localhost' and self.address != '127.0.0.1':
            return False

        if not os.path.isdir('pid'):
            os.mkdir('pid')

        if os.path.isdir('pid'):
            for file in os.listdir('pid'):
                if file.startswith('nameserver_'):
                    pid = file[len('nameserver_'):]
                    for proc in psutil.process_iter():
                        if str(proc.pid) == pid:
                            if verbose:
                                sys.stdout.write(' @ Stopping Nameservice of PID (%s)\n' % pid)
                            proc.kill()
                    os.remove(os.path.join('pid', file))
        if verbose:
            sys.stdout.write(' - Starting Nameserver \n')
            pass
        pstdout = None if verbose else subprocess.PIPE 
        pstderr = None if verbose else subprocess.PIPE
        pstdin = subprocess.PIPE
        if sys.platform == 'win32':
            path = os.path.join(os.environ['RTM_ROOT'], 'bin', 'rtm-naming.bat')
            cmd = [path, self.port]
            creationflag = 512
            preexec_fn = None
            pass
        else:
            cmd = ['rtm-naming', self.port]
            creationflag = 0
            preexec_fn = disable_sig
            pass

        if verbose:
            print ' - Command = %s' % cmd
            pass
        self._process = subprocess.Popen(cmd, creationflags=creationflag, stdout=pstdout, stdin=pstdin, stderr=pstderr, preexec_fn=preexec_fn)
        if force:
            self._process.stdin.write('y\n')
            pass

        # print ' ----- waiting 3 sec. -----'
        time.sleep(3);
        
        process_pid = self._process.pid
        for p in psutil.process_iter():
            if p.name() == 'omniNames':
                process_pid = p.pid
        if verbose:
            sys.stdout.write(' - Creating PID file (%s)\n' % process_pid)
            sys.stdout.write('  - Filename :%s\n' % os.path.join(os.getcwd(), 'pid', 'nameserver_' + str(process_pid)))
        open(os.path.join('pid', 'nameserver_' +  str(process_pid)), 'w').close()
        if verbose:
            sys.stdout.write(' - OK.\n')
        return 
    
    def kill(self):
        if self._process:
            self._process.kill()
        if os.path.isdir('pid'):
            for file in os.listdir('pid'):
                if file.startswith('nameserver_'):
                    pid = file[len('nameserver_'):]
                    for proc in psutil.process_iter():
                        if str(proc.pid) == pid:
                            sys.stdout.write(' - Stopping NameService.....\n')
                            proc.kill()
                    os.remove(os.path.join('pid', file))

    @property
    def rtcs(self, try_count=5):
        for i in range(0, try_count):
            try:
                if not self.tree:
                    path, port = rtctree.path.parse_path('/' + self.path)
                    self.tree = rtctree.tree.RTCTree(paths=path, filter=[path])
                    self.dir_node = self.tree.get_node(path)
                break
            except Exception, e:
                pass
        if not self.tree:
            return None

        rtcs = []
        def func(node, rtcs):
            rtcs.append(node)
            
        def filter_func(node):
            if node.is_component and not node.parent.is_manager:
                return True
            return False

        self.dir_node.iterate(func, rtcs, [filter_func])
        return rtcs
    
    @property
    def port_types(self):
        pass

    def refresh(self, verbose=False, force=False, try_count=5):
        for i in range(0, try_count):
            try:
                #if self.tree and force:
                #    del(self.tree)
                #    del(self.dir_node)
                #    self.tree = None
                if self.tree:
                    orb = self.tree.orb
                    self.tree.give_away_orb()
                else:
                    orb = None
                if not self.tree or force:
                    sys.stdout.write(' - refreshing tree... for %s\n' % self.path)
                    self.__path, self.__port = rtctree.path.parse_path('/' + self.path)
                    self.tree = rtctree.tree.RTCTree(paths=self.__path, filter=[self.__path], orb=orb)
                    self.dir_node = self.tree.get_node(self.__path)
                    sys.stdout.write(' - success.\n')
                    return 
            except omniORB.CORBA.OBJECT_NOT_EXIST, e:
                print 'omniORB'
            except omniORB.OBJECT_NOT_EXIST_NoMatch, e:
                print 'omniORB2'
            except Exception, e:
                print 'omniORB3'
                print e
                pass

    def dataports(self, data_type="any", port_type=['DataInPort', 'DataOutPort'], try_count=5, polarity="any"):
        for i in range(0, try_count):
            try:
                if not self.tree:
                    self.__path, self.__port = rtctree.path.parse_path('/' + self.path)
                    self.tree = rtctree.tree.RTCTree(paths=self.__path, filter=[self.__path])
                    self.dir_node = self.tree.get_node(self.__path)
                break
            except Exception, e:
                pass
        if not self.tree:
            return None

        ports = []
        def func(node, ports, data_type=data_type, port_type=port_type):
            ports__ = []
            if 'DataInPort' in port_type:
                ports__ = ports__ + node.inports
            if 'DataOutPort' in port_type:
                ports__ = ports__ + node.outports
            if data_type == 'any':
                for port in ports__:
                    ports.append(port)
            else:
                for port in ports__:
                    if port.properties['dataport.data_type'] == data_type:
                        ports.append(port)
                #for port in [port for port in ports__ if port.properties['dataport.data_type'] == data_type]:
                #    ports.append(port)
            
        def filter_func(node):
            if node.is_component and not node.parent.is_manager:
                return True
            return False

        self.dir_node.iterate(func, ports, [filter_func])
        return ports
        


    def svcports(self, interface_type="any", try_count=5, polarity="any"):
        for i in range(0, try_count):
            try:
                if not self.tree:
                    self.__path, self.__port = rtctree.path.parse_path('/' + self.path)
                    self.tree = rtctree.tree.RTCTree(paths=self.__path, filter=[self.__path])
                    self.dir_node = self.tree.get_node(self.__path)
                break
            except Exception, e:
                pass
        if not self.tree:
            return None

        ports = []
        def func(node, ports, interface_type=interface_type, polarity=polarity):
            for port in node.svcports:
                for intf in port.interfaces:
                    if interface_type != 'any':
                        if not intf.type_name == interface_type:
                            continue
                        pass
                    if polarity != 'any':
                        if not intf.polarity_as_string(False) == polarity:
                            continue
                    ports.append(port)

        def filter_func(node):
            if node.is_component and not node.parent.is_manager:
                return True
            return False

        self.dir_node.iterate(func, ports, [filter_func])
        return ports
        
