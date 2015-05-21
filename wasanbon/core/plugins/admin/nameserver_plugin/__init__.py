#from rtctree import tree as rtctree_tree
#from rtctree import path as rtctree_path

import os, sys, time, threading, types, subprocess, signal, traceback
from ctypes import *

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest



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



class Plugin(PluginFunction):
    """ Nameserver Management plugin """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    def get_nameservers_from_package(self, package, verbose=False):
        """ Get Nameserver object from package.
        :rtype: list<NameServer>:
        :return: NameServer class objects.
        """
        nss = []
        ns_paths = package.setting['nameservers']
        if not type(ns_paths) == types.ListType: ns_paths = [ns_paths]
        return [NameServer(path) for path in ns_paths]

    def is_running(self, ns, verbose=False, try_count=3, interval=5.0):
        """ Check NameServer (specified by NameServer class object) is running or not.
        :param NameServer ns: NameServer class object.
        :param bool verbose: Verbosity.
        :param int try_count: Retry in this count if connecting nameserver failed.
        :param float interval: Interval between retry.
        :rtype bool:
        :return: True if success
        """
        for i in range(0, try_count):
            if verbose: sys.stdout.write('## Checking Nameservice(%s) is running\n' % ns.path)
            from rtctree import path as rtctree_path
            import rtctree, omniORB
            try:
                if not ns.tree:
                    if verbose: sys.stdout.write('### Parsing path....\n')

                    path, port = rtctree_path.parse_path('/' + ns.path)
                    if verbose: sys.stdout.write('### Initializing rtctree...\n')


                    ns.tree = None
                    from wasanbon.util import task
                    from rtctree import tree as rtctree_tree
                    def task_func(args):
                        try:
                            if verbose: sys.stdout.write('#### Checking RTCTree.....\n')
                            ns.tree = rtctree_tree.RTCTree(paths=path, filter=[path])
                            if verbose: sys.stdout.write('#### Done.\n')
                        except:
                            if verbose: sys.stdout.write('#### Exception.\n')
                            pass

                    args = None
                    task.task_with_wdt(task_func, args, interval)
                    if not ns.tree:
                        if verbose: sys.stdout.write('### RTCTree Failed.\n')
                        continue
                    else:
                        if verbose: sys.stdout.write('### RTCTree Success.\n')

                if verbose: sys.stdout.write('### Getting Node...\n')
                self. dir_node = ns.tree.get_node(path)
                if verbose: sys.stdout.write('### Success.\n')
                if verbose: sys.stdout.write('### Nameservice(%s) is found.\n' % ns.path)
                return True
            except rtctree.exceptions.InvalidServiceError, e:
                continue
            except omniORB.CORBA.OBJECT_NOT_EXIST, e:
                continue
        if verbose: sys.stdout.write('### Nameservice not found.\n')
        return False

    def get_running_nss_from_pidfile(self, path=None, verbose=False, pidFilePath='pid'):
        if verbose: sys.stdout.write('## checking Nameservice is runing or not with pid file.\n')
        curdir = os.getcwd()
        if path != None: os.chdir(path)

        pids = []
        for file in os.listdir(pidFilePath):
            if file.startswith('nameserver_'):
                pid = file[len('nameserver_'):]
                pids.append(int(pid))
        os.chdir(curdir)
        return pids

    def remove_nss_pidfile(self, pid=None, path=None, verbose=False, pidFilePath='pid'):
        if verbose: sys.stdout.write('## checking Nameservice is runing or not with pid file.\n')
        curdir = os.getcwd()
        if path != None: os.chdir(path)

        pids = []
        for file in os.listdir(pidFilePath):
            if file.startswith('nameserver_'):
                pid_str = file[len('nameserver_'):]
                if pid == None or int(pid_str) == pid:
                    os.remove(os.path.join(pidFilePath, file))
        pass


    def terminate(self, ns, verbose=False, path=None):
        if ns.address != 'localhost' and ns.address != '127.0.0.1': return -1
        curdir = os.getcwd()
        if path != None: os.chdir(path)

        if not os.path.isdir(ns.pidFilePath):
            return -2

        pids = self.get_running_nss_from_pidfile(path=path, verbose=verbose, pidFilePath=ns.pidFilePath)
        import psutil
        for pid in pids:
            for proc in psutil.process_iter():
                if proc.pid == pid:
                    if verbose: sys.stdout.write('## Stopping Nameservice of PID (%s)\n' % pid)                    
                    proc.kill()
                    self.remove_nss_pidfile(pid=pid, path=path, verbose=verbose, pidFilePath=ns.pidFilePath)
        os.chdir(curdir)
        return 0


    @manifest 
    def start(self, argv):
        """ Start Naming Service
        """
        self.parser.add_option('-f', '--force', help='Force option (default=False)', 
                               default=False, action='store_true', dest='force_flag')
        self.parser.add_option('-p', '--port', help='Set TCP Port number for server', 
                               type='int', default=2809, dest='port')
        self.parser.add_option('-d', '--directory', help='Directory for log and pid file', 
                               type='string', default=os.path.join(wasanbon.home_path, 'pid'), dest='directory')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        force   = options.force_flag
        port = options.port
        directory = options.directory

        ns = NameServer('localhost:%s' % port, pidFilePath=directory)
        if self.launch(ns, verbose=verbose, force=force, pidFilePath=directory) == 0:
            sys.stdout.write('Success\n')
            return 0
        else:
            sys.stdout.write('Failed\n')
            return -1

    @manifest
    def stop(self, argv):
        """ Stop NamingService
        """
        self.parser.add_option('-d', '--directory', help='Directory for log and pid file', 
                               type='string', default=os.path.join(wasanbon.home_path, 'pid'), dest='directory')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory
        ns = NameServer('localhost:2809', pidFilePath=directory)
        if self.terminate(ns) == 0:
            sys.stdout.write('Success\n')
            return 0
        else:
            sys.stdout.write('Failed\n')
            return -1

    @manifest
    def check_running(self, argv):
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        if self.check_global_running():
            sys.stdout.write('Running\n')
            return 1
        else:
            sys.stdout.write('Not Running\n')
            return 0

    def check_global_running(self):
        import psutil
        for process in psutil.process_iter():
            if process.name().find('omniNames') >= 0:
                return True
        return False

    @manifest
    def tree(self, argv):
        self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=2809, dest='port')
        self.parser.add_option('-l', '--long', help='long format', default=False, action="store_true", dest='long_flag')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        long = options.long_flag
        port = options.port
        ns = NameServer('localhost:%s' % port, pidFilePath='.')
        if not self.check_global_running():
            sys.stdout.write('\n')
            return 0

        ns.refresh()
        sys.stdout.write('/ :\n')
        sys.stdout.write('  "%s" :\n' % ns.path)
        for comp in ns.components(verbose=verbose):
            sys.stdout.write('    %s :\n' % comp.name)
            if long:
                for p in comp.outports:
                    sys.stdout.write('      - DataOutPorts:\n')
                    sys.stdout.write('        name : %s\n' % p.name)
                    for key in p.properties.keys():
                        sys.stdout.write('        - Propertiews : %s\n' % p.name)
                        sys.stdout.write('          name : %s\n' % key)
                        sys.stdout.write('          value : %s\n' % p.properties[key])
                    for con in p.connections:
                        sys.stdout.write('        - Connections :\n')
                        sys.stdout.write('          name : %s\n' % con.name)
                        sys.stdout.write('          id   : %s\n' % con.id)
                        sys.stdout.write('          ports :\n')
                        for path, pp in con.ports:
                            sys.stdout.write('          - DataPorts:\n')
                            sys.stdout.write('            name : %s\n' % pp.name)

                        for key in p.properties.keys():
                            sys.stdout.write('          - Propertiews : %s\n' % p.name)
                            sys.stdout.write('            name : %s\n' % key)
                            sys.stdout.write('            value : %s\n' % p.properties[key])
                        

        
            

    def launch(self, ns, verbose=False, force=False, path=None, pidfile=True, pidFilePath='pid'):
        """ Launch Name Server 
        :param: NameService ns:
        """
        if ns.address != 'localhost' and ns.address != '127.0.0.1': return False
        
        curdir = os.getcwd()
        if path != None: os.chdir(path)

        if pidfile:
            if not os.path.isdir(pidFilePath):
                os.mkdir(pidFilePath)
            pids = self.get_running_nss_from_pidfile(path=path, verbose=verbose, pidFilePath=ns.pidFilePath)
            import psutil
            for pid in pids:
                for proc in psutil.process_iter():
                    if proc.pid == pid:
                        if verbose: sys.stdout.write('## Stopping Nameservice of PID (%s)\n' % pid)                    
                        proc.kill()
                        self.remove_nss_pidfile(pid=pid, path=path, verbose=verbose, pidFilePath=ns.pidFilePath)

        if verbose: sys.stdout.write('## Starting Nameserver \n')

        pstdout = None if verbose else subprocess.PIPE 
        pstderr = None if verbose else subprocess.PIPE
        pstdin = subprocess.PIPE
        if sys.platform == 'win32':
            path = os.path.join(os.environ['RTM_ROOT'], 'bin', 'rtm-naming.bat')
            cmd = [path, ns.port]
            creationflag = 512
            preexec_fn = None
            pass
        else:
            cmd = ['rtm-naming', ns.port]
            creationflag = 0
            preexec_fn = disable_sig
            pass

        if verbose: sys.stdout.write('### Command:%s\n' % cmd)
        
        process = subprocess.Popen(cmd, creationflags=creationflag, stdout=pstdout, stdin=pstdin, stderr=pstderr, preexec_fn=preexec_fn)
        if force: process.stdin.write('y\n')

        if pidfile:
            time.sleep(0.5);
            process_pid = process.pid
            for p in psutil.process_iter():
                if p.name() == 'omniNames':
                    process_pid = p.pid
            if verbose:
                sys.stdout.write('## Creating PID file (%s)\n' % process_pid)
                sys.stdout.write('### Filename :%s\n' % os.path.join(os.getcwd(), pidFilePath, 'nameserver_' + str(process_pid)))
            open(os.path.join(pidFilePath, 'nameserver_' +  str(process_pid)), 'w').close()

        if verbose: sys.stdout.write('## OK.\n')
        os.chdir(curdir)
        return 0
    

    
class NameServer(object):

    def __init__(self, path, pidFilePath='pid'):
        if path.find(':') < 0:
            path = path.strip() + ':2809'
        if path.strip().startswith('/'):
            path = path.strip()[1:]
        self._path = path
        self._process = None
        self._rtcs = None
        self.tree = None
        self.pidFilePath = pidFilePath

    @property
    def path(self):
        return self._path

    @property
    def address(self):
        return self._path.split(':')[0].strip()

    @property
    def port(self):
        return self._path.split(':')[1].strip()

    @property
    def rtcs(self, try_count=5):
        from rtctree import path as rtctree_path
        from rtctree import tree as rtctree_tree
        for i in range(0, try_count):
            try:
                if not self.tree:
                    self.__path, self.__port = rtctree_path.parse_path('/' + self.path)
                    self.tree = rtctree_tree.RTCTree(paths=self.__path, filter=[self.__path])
                    self.dir_node = self.tree.get_node(self.__path)
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
        from rtctree import path as rtctree_path
        from rtctree import tree as rtctree_tree
        import omniORB
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
                    sys.stdout.write('# Refreshing tree... for %s\n' % self.path)
                    self.__path, self.__port = rtctree_path.parse_path('/' + self.path)
                    self.tree = rtctree_tree.RTCTree(paths=self.__path, filter=[self.__path], orb=orb)
                    self.dir_node = self.tree.get_node(self.__path)
                    sys.stdout.write('## Success.\n')
                    return 
            except omniORB.CORBA.OBJECT_NOT_EXIST, e:
                print 'omniORB.CORBA.OBJECT_NOT_EXIST'
            except omniORB.OBJECT_NOT_EXIST_NoMatch, e:
                print 'omniORB.OBJECT_NOT_EXIST_NoMatch'
            except Exception, e:
                print e
                pass

    def dataports(self, data_type="any", port_type=['DataInPort', 'DataOutPort'], try_count=5, polarity="any", verbose=False):
        from rtctree import tree as rtctree_tree
        from rtctree import path as rtctree_path
        ports = []
        if verbose:
            sys.stdout.write('## get dataports from nameserver(%s)\n' % self.path)

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

        for i in range(0, try_count):
            try:
                if not self.tree:
                    self.__path, self.__port = rtctree_path.parse_path('/' + self.path)
                    self.tree = rtctree_tree.RTCTree(paths=self.__path, filter=[self.__path])
                    self.dir_node = self.tree.get_node(self.__path)

                self.dir_node.iterate(func, ports, [filter_func])
                break
            except Exception, e:
                sys.stdout.write('## Exception occurred when getting dataport information from nameserver(%s)\n' % self.path)
                if verbose:
                    traceback.print_exc()
                self.tree = None
                pass
            time.sleep(0.5)
        if not self.tree:
            return []

        return ports
        


    def svcports(self, interface_type="any", try_count=5, polarity="any"):
        from rtctree import tree as rtctree_tree
        from rtctree import path as rtctree_path

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


        for i in range(0, try_count):
            try:
                if not self.tree:
                    self.__path, self.__port = rtctree_path.parse_path('/' + self.path)
                    self.tree = rtctree_tree.RTCTree(paths=self.__path, filter=[self.__path])
                    self.dir_node = self.tree.get_node(self.__path)
                self.dir_node.iterate(func, ports, [filter_func])
                break
            except Exception, e:
                sys.stdout.write('## Exception occurred when getting dataport information from nameserver(%s)\n' % self.path)
                if verbose:
                    traceback.print_exc()
                pass
            time.sleep(0.5)
        if not self.tree:
            return []


        return ports
        

    def components(self, instanceName=None, verbose=False, try_count=5):
        from rtctree import tree as rtctree_tree
        from rtctree import path as rtctree_path
        comps = []
        if verbose:
            sys.stdout.write('## get components from nameserver(%s)\n' % self.path)

        def func(node, comps, instanceName=instanceName):
            if instanceName:
                if node.instanceName == instanceName:
                    comps.append(node)
            else:
                comps.append(node)

        def filter_func(node):
            if node.is_component and not node.parent.is_manager:
                return True
            return False

        for i in range(0, try_count):
            try:
                if not self.tree:
                    self.__path, self.__port = rtctree_path.parse_path('/' + self.path)
                    self.tree = rtctree_tree.RTCTree(paths=self.__path, filter=[self.__path])
                    self.dir_node = self.tree.get_node(self.__path)

                self.dir_node.iterate(func, comps, [filter_func])
                break
            except Exception, e:
                sys.stdout.write('## Exception occurred when getting component information from nameserver(%s)\n' % self.path)
                if verbose:
                    traceback.print_exc()
                self.tree = None
                pass
            time.sleep(0.5)
        if not self.tree:
            return []

        return comps
        
