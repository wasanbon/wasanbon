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
    try:
        libc = CDLL('libc.dylib')
    except:
        libc = CDLL('/usr/lib/libc.dylib')
        #libc = cdll.LoadLibrary('libSystem.dylib')
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
        return ['admin.environment', 'admin.systemeditor']

    def get_nameservers_from_package(self, package, verbose=False):
        """ Get Nameserver object from package.
        :rtype: list<NameServer>:
        :return: NameServer class objects.
        """
        nss = []
        ns_paths = package.setting['nameservers']
        if not type(ns_paths) == types.ListType: ns_paths = [ns_paths]
        return [NameServer(path) for path in ns_paths]

    def component(self, path, func, verbose=False, try_count=5):
        from rtctree import tree as rtctree_tree
        from rtctree import path as rtctree_path
        comps = []
        if verbose:
            sys.stdout.write('## get components from nameserver(%s)\n' % path)

        for i in range(0, try_count):
            try:
                path_, port_ = rtctree_path.parse_path('/' + path)
                tree = rtctree_tree.RTCTree(paths=path_, filter=[path_])
                dir_node = tree.get_node(path_)
                if dir_node.is_component:
                    if func:
                        func(dir_node)
                    return dir_node
                break
            except Exception, e:
                sys.stdout.write('## Exception occurred when getting component information from nameserver(%s)\n' % path)
                if verbose:
                    traceback.print_exc()
                self.tree = None
                pass
            time.sleep(0.5)
        if not self.tree:
            return []

        return None

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
    	""" Get Running Name Services from PID files.
    	:param path 
    	:param verbose
    	:param pidFilePath 
    	:rtype NameService
    	:return:
    	"""
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
        if verbose: sys.stdout.write('## checking Nameservice is running or not with pid file in %s.\n' % pidFilePath)
        curdir = os.getcwd()

        if path != None: os.chdir(path)

        pids = []
        for file in os.listdir(pidFilePath):
            
            if file.startswith('nameserver_'):
                pid_str = file[len('nameserver_'):]
                if pid == None or int(pid_str) == pid:
                    os.remove(os.path.join(pidFilePath, file))
        os.chdir(curdir)
        pass

    def remove_nss_datfile(self, path=None, verbose=False, logFilePath='.'):
        if verbose: sys.stdout.write('## remove Nameservice dat file is in %s' % path)
        curdir = os.getcwd()
        if path != None: os.chdir(path)

        for file in os.listdir(logFilePath):
            if file.endswith('.dat'):
                os.remove(os.path.join(logFilePath, file))
        os.chdir(curdir)
        pass

    def remove_all_nss_pidfile(self, path=None, verbose=False, pidFilePath='pid'):
        if verbose: sys.stdout.write('## checking Nameservice is running or not with pid file in %s.\n' % pidFilePath)
        curdir = os.getcwd()
        if path != None: os.chdir(path)

        pids = []
        for file in os.listdir(pidFilePath):
            if file.startswith('nameserver_'):
                os.remove(os.path.join(pidFilePath, file))
        pass


    def terminate(self, ns, verbose=False, path=None, logdir=None):
        if verbose: sys.stdout.write('# Terminating Nameservice in %s\n' % ns.address)
        if ns.address != 'localhost' and ns.address != '127.0.0.1': return -1
        curdir = os.getcwd()
        if path != None: os.chdir(path)

        if not os.path.isdir(ns.pidFilePath):
            return -2

        pids = self.get_running_nss_from_pidfile(path=path, verbose=verbose, pidFilePath=ns.pidFilePath)
        if verbose: sys.stdout.write("# Running NameServer's PID == %s\n" % pids)
        import psutil

        for pid in pids:
            for proc in psutil.process_iter():
                if proc.pid == pid:
                    if verbose: sys.stdout.write('## Stopping Nameservice of PID (%s)\n' % pid)                    
                    proc.kill()
                    self.remove_nss_pidfile(pid=pid, path=path, verbose=verbose, pidFilePath=ns.pidFilePath)
        os.chdir(curdir)

        if logdir:
            for f in os.listdir(logdir):
                if f.startswith('omninames'):
                    if verbose:
                        sys.stdout.write('## Removing file (%s)\n' % os.path.join(logdir, f))
                    os.remove(os.path.join(logdir, f))

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
                               type='string', default=os.path.join(wasanbon.home_path), dest='directory')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        force   = options.force_flag
        port = options.port
        directory = options.directory

        ns = NameServer('localhost:%s' % port, pidFilePath=os.path.join(directory, 'pid'))
        sys.stdout.write('# Starting Nameserver (%s)\n' % str(ns))
        if self.launch(ns, verbose=verbose, path=os.path.join(directory, 'log'), force=force, pidFilePath=os.path.join(directory, 'pid')) == 0:
            sys.stdout.write('Success\n')
            return 0
        else:
            sys.stdout.write('Failed\n')
            return -1

    @manifest
    def stop(self, argv):
        """ Stop NamingService
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
        directory = options.directory
        ns = NameServer('localhost:2809', pidFilePath=directory)
        sys.stdout.write('# Stopping Nameserver (%s)\n' % str(ns))
        if self.terminate(ns, verbose=verbose, logdir=os.path.join(wasanbon.home_path, 'log')) == 0:
            sys.stdout.write('Success\n')
            self.remove_all_nss_pidfile(verbose=verbose, pidFilePath=os.path.join(wasanbon.home_path, 'pid'))
            return 0
        else:
            sys.stdout.write('Failed\n')
            return -1
        
    @manifest 
    def restart(self, argv):
        """ Stop and Start NameServer """
        if self.stop(argv) == 0:
            return self.start(argv)
        return -1

    @manifest
    def check_running(self, argv):
        self.parser.add_option('-p', '--port', help='Set TCP Port number for server', 
                               type='int', default=2809, dest='port')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        port = options.port
        sys.stdout.write('# Checking Nameserver\n')
        if self.check_global_running(port=port):
            sys.stdout.write('Running\n')
            return 1
        else:
            sys.stdout.write('Not Running\n')
            return 0

    def check_global_running(self, port=None):
        import psutil
        for process in psutil.process_iter():
            try:
                if process.name().find('omniNames') >= 0:
                    if port is None:
                        return True
                    else:
                        if str(port) in process.cmdline():
                            return True
                        else:
                            pass # return False
            except psutil.AccessDenied, e:
                continue
            except psutil.ZombieProcess, e:
                continue
        return False

         
    @manifest
    def tree(self, argv):
        self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=2809, dest='port')
        self.parser.add_option('-l', '--long', help='long format', default=False, action="store_true", dest='long_flag')
        self.parser.add_option('-d', '--detail', help='detail format', default=False, action="store_true", dest='detail_flag')
        self.parser.add_option('-u', '--url', help='Host Address', default='localhost', action="store", dest='url')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        long = options.long_flag
        detail = options.detail_flag
        port = options.port
        url = options.url
        nss = []
        def func(args):
            ns = NameServer(url + ':%s' % port, pidFilePath='.')
            if not self.check_global_running():
                sys.stdout.write('## Nameserver is not running.\n')
                sys.stdout.write('\n')
                return 0
            
            ns.yaml_dump(long=long, detail=detail)
            nss.append(ns)

        from wasanbon.util import task
        interval = 10
        task.task_with_wdt(func, [], interval)
        if len(nss) == 0:
            sys.stdout.write('Timeout\n')
            return -1

        return 0

    @manifest
    def configure(self, argv):
        self.parser.add_option('-s', '--set', help='Configuration Set Name (default=default)', type='string', default='default', dest='set_name')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        wasanbon.arg_check(argv, 6)
        set_name = options.set_name
        rtc_full_path = argv[3]
        conf_name = argv[4]
        conf_value = argv[5]
        found_conf = False
        def func(comp):
            for cs in comp.conf_sets:
                if cs == set_name:
                    cset = comp.conf_sets[set_name]
                    for key, value in cset.data.items():
                        if key == conf_name:
                            comp.set_conf_set_value(set_name, conf_name, conf_value)
                            found_conf = True
        
        comps = []
        def taskfunc(args):
            try:
                comp = self.component(rtc_full_path, func, verbose=verbose)
            except:
                sys.stdout.write('Failed. Exception occured.\n');
                traceback.print_exc()
                return

            if found_conf:
                sys.stdout.write('Success.\n')
            else:
                sys.stdout.write('Failed.\n');

            comps.append(comp)

        from wasanbon.util import task
        interval = 10
        task.task_with_wdt(taskfunc, [], interval)
        if len(comps) == 0:
            sys.stdout.write('Timeout\n')
            return -1

        return 0

    def ___hoge(self):
        tab =  '  '
        ns.refresh()
        sys.stdout.write('/ :\n')
        sys.stdout.write(tab + '"%s" :\n' % ns.path)
        if len(ns.components()) == 0:
            sys.stdout.write(tab * 2 + '{}\n')
            return 0
        for comp in ns.components(verbose=verbose):
            sys.stdout.write(tab * 2 + '%s :\n' % comp.name)
            if long or detail:
                sys.stdout.write(tab * 3 + 'DataInPorts:\n')
                if len(comp.inports) == 0:
                    sys.stdout.write(tab * 4 + '{}\n')
                else:
                    for p in comp.inports:
                        self._print_port(p, long, detail, 4)
                sys.stdout.write(tab * 3 + 'ServicePorts:\n')
                if len(comp.svcports) == 0:
                    sys.stdout.write(tab * 4 + '{}\n')
                else:
                    for p in comp.svcports:
                        self._print_port(p, long, detail, 4)
        return 0


    @manifest
    def activate_rtc(self, argv):
        self.parser.add_option('-i', '--id', help='Set EC_ID', 
                               type='int', default=0, dest='ec_id')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        
        wasanbon.arg_check(argv, 4)
        sys.stdout.write('# Activating RTC (%s)\n' % argv[3])
        ec_id = options.ec_id
        comp = self.component(argv[3], lambda c : c.activate_in_ec(ec_id), verbose=verbose)
        return 0


    @manifest
    def deactivate_rtc(self, argv):
        self.parser.add_option('-i', '--id', help='Set EC_ID', 
                               type='int', default=0, dest='ec_id')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        
        wasanbon.arg_check(argv, 4)
        sys.stdout.write('# Deactivating RTC (%s)\n' % argv[3])
        ec_id = options.ec_id
        comp = self.component(argv[3], lambda c : c.deactivate_in_ec(ec_id), verbose=verbose)
        return 0

    @manifest
    def reset_rtc(self, argv):
        self.parser.add_option('-i', '--id', help='Set EC_ID', 
                               type='int', default=0, dest='ec_id')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        
        wasanbon.arg_check(argv, 4)
        sys.stdout.write('# Resetting RTC (%s)\n' % argv[3])
        ec_id = options.ec_id
        comp = self.component(argv[3], lambda c : c.reset_in_ec(ec_id), verbose=verbose)
        return 0

    @manifest
    def exit_rtc(self, argv):
        self.parser.add_option('-i', '--id', help='Set EC_ID', 
                               type='int', default=0, dest='ec_id')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        wasanbon.arg_check(argv, 4)
        sys.stdout.write('# Resetting RTC (%s)\n' % argv[3])
        ec_id = options.ec_id
        comp = self.component(argv[3], lambda c : c.exit(), verbose=verbose)
        return 0

    def launch(self, ns, verbose=False, force=False, path=None, pidfile=True, pidFilePath='pid'):
        """ Launch Name Server 
        :param: NameService ns:
        """
        if ns.address != 'localhost' and ns.address != '127.0.0.1': return False
        
        curdir = os.getcwd()
        if path != None: 
            if not os.path.isdir(path):
                os.mkdir(path)
            os.chdir(path)

            
        if pidfile:
            if not os.path.isdir(pidFilePath):
                os.mkdir(pidFilePath)
            pids = self.get_running_nss_from_pidfile(path=path, verbose=verbose, pidFilePath=ns.pidFilePath)
            import psutil
            for pid in pids:
                for proc in psutil.process_iter():
                    if proc.pid == pid:
                        if verbose: sys.stdout.write('## Stopping Nameservice of PID (%s)\n' % pid)                    
                        try:
                            proc.kill()
                        except psutil.AccessDenied, e:
                            sys.stdout.write('### PID(%d) access denyed. Proceeding... \n' % pid)
                        self.remove_nss_pidfile(pid=pid, path=path, verbose=verbose, pidFilePath=ns.pidFilePath)
            self.remove_nss_datfile(path=path, verbose=verbose)

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
                try:
                    if p.name().find('omniNames') >= 0:
                        process_pid = p.pid
                except psutil.AccessDenied, e:
                    continue
                except psutil.ZombieProcess, e:
                    continue
            if verbose:
                sys.stdout.write('## Creating PID file (%s)\n' % process_pid)
                sys.stdout.write('### Filename :%s\n' % os.path.join(os.getcwd(), pidFilePath, 'nameserver_' + str(process_pid)))
            open(os.path.join(pidFilePath, 'nameserver_' +  str(process_pid)), 'w').close()

        if verbose: sys.stdout.write('## OK.\n')
        os.chdir(curdir)
        return 0

    @manifest
    def list_connectable_pair(self, argv):
        self.parser.add_option('-n', '--nameservers', help='Set NameServers. If plural servers, separate with ",".', 
                               type='string', default='localhost:2809', dest='nameservers')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        nameserver_uris = [n.strip() for n in options.nameservers.split(',')]

        nss = [NameServer(path) for path in nameserver_uris]

        import omniORB
        try:
            pairs = admin.systemeditor.get_connectable_pairs(nss, verbose=verbose)
            for pair in pairs:
                def get_port_fullpath(port):
                    path = ""
                    for p in port.owner.full_path[1:]:
                        path = path + '/' + p
                        pass
                    portName = port.name
                    if portName.find('.') >= 0:
                        portName = portName.split('.')[1]
                        pass

                    return path + ':' + portName
                def is_connected(p0, p1):
                    return len(p0.get_connections_by_dest(p1)) > 0
                sys.stdout.write('%s %s %s\n' % (get_port_fullpath(pair[0]), '==>' if is_connected(pair[0], pair[1]) else '   ',
                                                 get_port_fullpath(pair[1])))
        except omniORB.CORBA.OBJECT_NOT_EXIST, e:
            print 'corba'
            print e
            pass

        return 0
    
    @manifest
    def connect(self, argv):
        def property_callback(option, opt, option_value, parser):
            if option_value.count('=') != 1:
                raise wasanbon.InvalidUsageException()
            key, equals, value = option_value.partition('=')
            if not getattr(parser.values, option.dest):
                setattr(parser.values, option.dest, {})
            if key in getattr(parser.values, option.dest):
                raise wasanbon.InvalidUsageException()
            getattr(parser.values, option.dest)[key] = value


        self.parser.add_option('-n', '--name', help='Name of connection. (Default: None)', 
                               type='string', default=None, dest='name')
        self.parser.add_option('-i', '--id', help='id of connection. (Default: "")', 
                               type='string', default='', dest='id')
        self.parser.add_option('-p', '--property', help='Properties of connection. Use A=B Format (Default:"")', 
                               type='string', dest='properties', action='callback', callback=property_callback)
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        if not getattr(options, 'properties'):
            setattr(options, 'properties', {})
        
        from rtshell import path
        from rtshell.rtcon import connect_ports
        
        paths = [(arg, path.cmd_path_to_full_path(arg)) for arg in argv[3:]]
        try:
            connect_ports(paths, options, tree=None)
            sys.stdout.write('Success.\n')
        except:
            sys.stdout.write('Failed. Exception occurred.\n')
        
        return 0

    @manifest
    def disconnect(self, argv):
        self.parser.add_option('-i', '--id', help='id of connection. (Default: "")', 
                               type='string', default='', dest='id')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        
        from rtshell import path
        from rtshell.rtdis import disconnect_ports
        
        paths = [(arg, path.cmd_path_to_full_path(arg)) for arg in argv[3:]]
        try:
            disconnect_ports(paths, options, tree=None)
            sys.stdout.write('Success.\n')
        except:
            sys.stdout.write('Failed. Exception occurred.\n')
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

    def _print_conf_set(self, name, conf_set, long, detail, tablevel):
        tab =  '  '
        if not long and not detail:
            if name.startswith('__'):
                return
            sys.stdout.write(tab*tablevel + ' - %s\n' % name)
        elif long and not detail:
            if name.startswith('__'):
                return
            sys.stdout.write(tab*tablevel + '%s : \n' % name)
            for key, value in conf_set.data.items():
                sys.stdout.write(tab*(tablevel+1) + '%s : %s\n' % (key, value))
            if len(conf_set.data.keys()) == 0:
                sys.stdout.write(tab*(tablevel+1) + '{}\n')
        elif detail:
            sys.stdout.write(tab*tablevel + '%s : \n' % name)
            #sys.stdout.write(tab*(tablevel+1) + 'properties : \n')
            for key, value in conf_set.data.items():
                sys.stdout.write(tab*(tablevel+1) + '%s : %s\n' % (key, value))
            if len(conf_set.data.keys()) == 0:
                sys.stdout.write(tab*(tablevel+1) + '{}\n')
        

    def _print_port(self, port, long, detail, tablevel):
        tab =  '  '
        if not long and not detail:
            sys.stdout.write(tab*tablevel + ' - %s\n' % port.name)
        elif long and not detail:
            sys.stdout.write(tab*tablevel + '%s : \n' % port.name)
            if 'dataport.data_type' in port.properties.keys():
                sys.stdout.write(tab*(tablevel+1) + 'type : %s\n' % port.properties['dataport.data_type'])
            pass
        elif detail:
            sys.stdout.write(tab*tablevel + '%s : \n' % port.name)
            if port.properties['port.port_type'] == 'CorbaPort':
                sys.stdout.write(tab*(tablevel+1) + 'interfaces : \n')

                for intf in port.interfaces:
                    sys.stdout.write(tab*(tablevel+2) + 'ServiceInterface : \n')
                    sys.stdout.write(tab*(tablevel+3) + 'instance_name : ' + intf.instance_name + '\n')
                    sys.stdout.write(tab*(tablevel+3) + 'type_name : ' + intf.type_name + '\n')
                    sys.stdout.write(tab*(tablevel+3) + 'polarity : ' + intf.polarity_as_string(add_colour=False) + '\n')
            sys.stdout.write(tab*(tablevel+1) + 'properties : \n')
            for key, value in port.properties.items():
                sys.stdout.write(tab*(tablevel+2) + '%s : "%s"\n' % (key, value))
            sys.stdout.write(tab*(tablevel+1) + 'connections :\n')
            if len(port.connections) == 0:
                sys.stdout.write(tab*(tablevel+2) + '{}\n')
            else:
                for con in port.connections:
                    sys.stdout.write(tab*(tablevel+2) + con.name + ' : \n')
                    #sys.stdout.write(tab*(tablevel+3) + 'name : %s\n' % con.name)
                    sys.stdout.write(tab*(tablevel+3) + 'id   : %s\n' % con.id)
                    sys.stdout.write(tab*(tablevel+3) + 'ports :\n')
                    for path, pp in con.ports:
                        name = pp.name
                        if name.find('.') >= 0:
                            name = name.split('.')[-1].strip()
                        fullpath = pp.owner.full_path_str + ':' + name
                        sys.stdout.write(tab*(tablevel+4) + ' - %s\n' % fullpath)
                        pass
                    sys.stdout.write(tab*(tablevel+3) + 'properties :\n')
                    for key, value in con.properties.items():
                        sys.stdout.write(tab*(tablevel+4) + '%s : "%s"\n' % (key, value))
                        


    def yaml_dump(self, long=False, detail=False, verbose=False):
        from rtctree import tree as rtctree_tree
        from rtctree import path as rtctree_path
        ports = []
        tab = '  '
        ns_only = True

        def show_func(node, tablevel, long=False, detail=False):

            if node.is_nameserver:
                full_path  = node.full_path[1]
                if full_path.startswith('/'): full_path = full_path[1:]
                sys.stdout.write(tab * tablevel + '"' + full_path + '":' + '\n')
            elif node.is_manager:
                sys.stdout.write(tab * tablevel + '' + node.name + ': {}\n')                
            elif node.is_directory:
                sys.stdout.write(tab * tablevel + '' + node.name + ':\n')
            elif node.is_zombie:
                sys.stdout.write(tab * tablevel + '' + node.name + '* : {}\n')                
            elif node.is_component:
                if not long and not detail:
                    sys.stdout.write(tab * tablevel + '' + node.name + '\n')
                else:
                    sys.stdout.write(tab * tablevel + '' + node.name + ':\n')
                    sys.stdout.write(tab * (tablevel + 1) + 'DataOutPorts:\n')
                    if len(node.outports) == 0:
                        sys.stdout.write(tab * (tablevel + 2) + '{}\n')
                    else:
                        for p in node.outports:
                            self._print_port(p, long, detail, 4)

                    sys.stdout.write(tab * (tablevel + 1) + 'DataInPorts:\n')
                    if len(node.inports) == 0:
                        sys.stdout.write(tab * (tablevel + 2) + '{}\n')
                    else:
                        for p in node.inports:
                            self._print_port(p, long, detail, 4)
                    sys.stdout.write(tab * (tablevel + 1) + 'ServicePorts:\n')
                    if len(node.svcports) == 0:
                        sys.stdout.write(tab * (tablevel + 2) + '{}\n')
                    else:
                        for p in node.svcports:
                            self._print_port(p, long, detail, 4)
                    sys.stdout.write(tab * (tablevel + 1) + 'ConfigurationSets:\n')
                    if len(node.conf_sets) == 0:
                        sys.stdout.write(tab * (tablevel + 2) + '{}\n')
                    else:
                        for cs in node.conf_sets:
                            self._print_conf_set(cs, node.conf_sets[cs], long, detail, 3+1)

                    sys.stdout.write(tab * (tablevel + 1) + 'properties:\n')
                    for key in sorted(node.properties.keys()):
                        value = node.properties[key]
                        sys.stdout.write(tab * (tablevel + 2) + key + ' : "' + value + '"\n')
                    sys.stdout.write(tab * (tablevel + 1) + 'state : ' + node.get_state_string(add_colour=False) + '\n')
                    sys.stdout.write(tab * (tablevel + 1) + 'exec_cxts:\n')
                    ec = node.get_ec(0)
                    for ec1 in node.owned_ecs:
                        #sys.stdout.write(tab * (tablevel + 2) + 'owner : ' + str(ec.participants) + '\n')
                        #sys.stdout.write(tab * (tablevel + 2) + 'state : ' + str(ec.get_component_state(node)) + '\n')
                        sys.stdout.write(tab * (tablevel + 2) + 'properties:\n')
                        for key in sorted(ec.properties.keys()):
                            value = ec.properties[key]
                            sys.stdout.write(tab * (tablevel + 3) + key + ' : "' + value + '"\n')

            if not node.is_manager:
                for c in node.children:
                    show_func(c, tablevel+1, long, detail)
                if not node.is_component and not node.is_zombie:
                    if len(node.children) == 0:
                        sys.stdout.write(tab * tablevel + tab  + '{}\n');
            
        try_count = 5
        import omniORB
        for i in range(0, try_count):
            try:
                if not self.tree:
                    if verbose: sys.stdout.write('## Refreshing Name Server Tree.\n')
                    self.__path, self.__port = rtctree_path.parse_path('/' + self.path)
                    self.tree = rtctree_tree.RTCTree(paths=self.__path, filter=[self.__path])
                    self.dir_node = self.tree.get_node(self.__path)
                sys.stdout.write('"' + self.path + '":\n')
                for c in self.dir_node.children:
                    show_func(c, 1, long, detail)
                if len(self.dir_node.children) == 0:
                    sys.stdout.write('  {}\n')
                
                break
            except Exception, e:
                sys.stdout.write('## Exception occurred when getting tree information from nameserver(%s)\n' % self.path)
                if verbose:
                    traceback.print_exc()
                pass
            except omniORB.CORBA.OBJECT_NOT_EXIST_NoMatch, e:
                sys.stdout.write('## CORBA.OBJECT_NOT_EXIST\n')
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
                    if verbose: sys.stdout.write('## Refreshing Name Server Tree.\n')
                    self.__path, self.__port = rtctree_path.parse_path('/' + self.path)
                    self.tree = rtctree_tree.RTCTree(paths=self.__path, filter=[self.__path])
                    self.dir_node = self.tree.get_node(self.__path)
                self.dir_node.iterate(func, ports, [filter_func])
                break
            except Exception, e:
                sys.stdout.write('## Exception occurred when getting service port information from nameserver(%s)\n' % self.path)
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
        
