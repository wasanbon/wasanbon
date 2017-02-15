import os, sys, traceback, optparse, subprocess
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest
import setup
import shutil

class Plugin(PluginFunction):
    """ Environment initialization functions
        Use to initialize wasanbon environment."""

    _install_list = ['setuptools', 'pip', 'yaml', 'github', 'psutil', 'requests', 'requests_oauthlib', 'bitbucket', #'lxml',
                     ]
    _install_rtms = ['rtm_c++', 'rtm_python', 'rtm_java', 'rtctree', 'rtsprofile', 'rtshell']

    def __init__(self):
        super(Plugin, self).__init__()
        pass

    @manifest
    def status(self, args):
        """ This command shows Environment status for wasanbon. """
        sys.stdout.write('# Showing the status of wasanbon environment initialization...\n')
        options, argv = self.parse_args(args[:])
        verbose = True #options.verbose_flag

        for key, value in self.path.items():
            sys.stdout.write('%s : %s\n' % (key, value))
        return 0

    @manifest
    def update_path(self, args):
        """ Update Search Path for commands. """
        options, argv = self.parse_args(args[:])
        verbose = True #options.verbose_flag

        self._update_path(verbose=verbose)
        return 0

    @manifest
    def init(self, args):
        """ This command must be called first.
        Install Pip, PyYAML, PyGithub, psutil, python-bitbucket, and several modules 
        if not installed. After that, Initialize $HOME/.wasanbon directory, 
        and search commands used in wasanbon. If some command-line tools are not installed, 
        this will tries to install them.
        """

        sys.stdout.write('# Starting wasanbon environment initialization...\n')
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        self.parser.add_option('-q', '--quiet', help='Verbosity option (default=False)', default=False, action='store_true', dest='quiet_flag')
        options, argv = self.parse_args(args[:])
        verbose = True #options.verbose_flag
        if options.quiet_flag: verbose = False
        force = options.force_flag

        sys.stdout.write('# Checking Installationg and Repair Environment.....\n')

        # This order is very important

        retval = []
        for install_pack in self._install_list:
            ret = setup.try_import_and_install(install_pack, verbose=verbose, force=force, workpath=wasanbon.temp_path)
            retval.append(ret == 0)

        if not all(retval):
            sys.stdout.write('# Failed. Try again.\n')
            return -1

        sys.stdout.write('# Success.\n')
        sys.stdout.write('# Initializing .wasanbon directory....\n')
        
        if verbose:sys.stdout.write('## Platform: %s\n' % wasanbon.platform())

        self._copy_path_yaml_from_setting_dir(force=force, verbose=verbose)
        self._update_path(verbose)

        if verbose: sys.stdout.write('# Installing Commands....\n')

        ret = self._install_commands(verbose)
        
        if ret == 0:
            sys.stdout.write('# Success.\n')
        else:
            sys.stdout.write('# Failed. Try again.\n')
            return -1


        sys.stdout.write('# Installing RTMs...\n')
        for rtm in self._install_rtms:
            if verbose: sys.stdout.write('# Installing %s\n' % rtm)
            if self._install_package(rtm, verbose=verbose, force=force) != 0:
                sys.stdout.write('# Installng %s Failed. Try again.\n' % rtm)
            else:
                if verbose: sys.stdout.write('## Installing %s succeeded.\n' % rtm)
                
        sys.stdout.write('## Installing RTMs Ends.\n')
        return 0

    def _print_install_opts(self, args):
        for i in self._install_list + self._install_rtms:
            print i

    @manifest
    def install(self, args):
        """ Install Command. This command allows users to install comand-line tool manually. """
        self.parser.add_option('-f', '--force', help='Force option (default=Flase)', default=False, action='store_true', dest='force_flag')
        self.parser.add_option('-q', '--quiet', help='Verbosity option (default=Flase)', default=False, action='store_true', dest='quiet_flag')
        options, argv = self.parse_args(args[:], self._print_install_opts)
        #verbose = True 
        verbose = options.verbose_flag
        if options.quiet_flag: verbose = False
        force = options.force_flag
        

        if len(argv) < 4:
            raise wasanbon.InvalidUsageException()
        cmd = argv[3]

        if cmd in self.path.keys():
            if verbose: sys.stdout.write('# Installing Command [%s]\n' % cmd)
            self._install_command(cmd, verbose=verbose, force=force)
        else:
            self._install_package(cmd, verbose=verbose, force=force)
            
        return 0

    @manifest
    def register(self, args):
        """ Register some specific information of users. 1. account of github.com, 2. version of Visual Studio (in windows) """
        self.parser.add_option('-u', '--username', help='Username of github.com', default=None, dest='username', action='store', type='string')
        self.parser.add_option('-p', '--password', help='Password of github.com', default=None, dest='password', action='store', type='string')
        if sys.platform == 'win32':
            self.parser.add_option('-c', '--compiler', help='Compiler of Win32 system', default='', dest='compiler', action='store', type='string')
        options, argv = self.parse_args(args[:], self._print_install_opts)

        verbose = True #options.verbose_flag
        
        if os.path.isfile(wasanbon.register_file):
            try:
                open(wasanbon.register_file, 'w').close()
            except:
                sys.stdout.write(
                    """# Creating Register file failed.\n This may be caused by incorrectly initialized the path of $HOME/.wasanbon.\n Use wasanbon-admin.py environment init command.\n""")
                return -1

        sys.stdout.write('# Input Username and Password of github.com\n')
        user, passwd = wasanbon.user_pass(options.username, options.password)

        # Try to register 
        reg_dict = {'github.com': 
                    {'username' : user,
                     'password' : passwd},
                    }
        
        if sys.platform == 'win32':
            if len(options.compiler ) == 0:
                sys.stdout.write('# Input compiler of current system [default=Visual Studio 12]')
                comp = raw_input()
                options.compiler = comp
            reg_dict['compiler'] = options.compiler
        
        sys.stdout.write('# Saving registration data...\n')
        import yaml
        open(wasanbon.register_file, 'w').write(yaml.dump(reg_dict))
        sys.stdout.write('## Success\n')
        return 0

    @property
    def setting_path(self):
    	""" This plugin's setting directory path. This includes OS dependent information like packages. """
        setting_path = os.path.join(__path__[0], 'settings', wasanbon.platform())
        if not os.path.isdir(setting_path):
            sys.stdout.write('# Error. UnsupportedPlatform (%s)\n' % wasanbon.platform())
            raise wasanbon.UnsupportedPlatformException()
        return setting_path

    def getIDE(self):
    	""" Environment's default IDE (Integrated Development Environment) like Visual Studio. """
        return wasanbon.IDE

    @property
    def path(self):
    	""" Environment's command paths. Ex., paths for cmake, doxygen, git, svn, and so on. """
        path_filename = os.path.join(wasanbon.home_path, 'path.yaml')
        if not os.path.isfile(path_filename): return {}
        try:
            yaml = __import__('yaml')
            return yaml.load(open(path_filename, 'r'))
        except ImportError, e:
            return {}
        
    @manifest
    def setup_bashrc(self, verbose=False):
    	""" Setup bashrc profile. In Ubuntu, $HOME/.bashrc. In OSX, $HOME/.bash_profile. """
        if sys.platform == 'darwin':
            filename = '.bash_profile'
        elif sys.platform == 'linux2':            
            filename = '.bashrc'
        else:
            return -1

        start_str = '#-- Starting Setup Script of wasanbon --#'
        stop_str  = '#-- Ending Setup Script of wasanbon --#'
        target = os.path.join(wasanbon.get_home_path(), filename)
        script = open(os.path.join(__path__[0], "settings", wasanbon.platform(), "bashrc"), "r").read()
        
        if verbose: sys.stdout.write('# Initializing $HOME/%s\n' % filename)
        
        if os.path.isfile(target):
            erase = False
            file = open(target, "r")
            fout = open(target + '.bak', "w")
            for line in file:
                if line.strip() == start_str:
                    erase = True
                    continue

                elif line.strip() == stop_str:
                    erase = False
                    continue

                if not erase:
                    fout.write(line)
                    pass
                pass
        
            file.close()
            fout.close()

            os.remove(target)
            os.rename(target + ".bak" , target)
            
            fout = open(target, "a")
        else:
            fout = open(target, "w")
            pass

        fout.write("\n\n" + start_str + "\n")
        fout.write(script)
        fout.write("\n" + stop_str + "\n\n")
            

        fout.close()
        return 0


    # Private Functions
    def _install_commands(self, verbose=False, force=False):
        retval = True
        ret = {}
        flag = False
        for key, value in self.path.items():
            ret[key] = self._install_command(key, verbose=verbose, force=force)
            if ret[key] != 0:
                if verbose: sys.stdout.write('# Installing %s failed.\n' % key)
                retval = False

        return 0 if retval else -1



    def _install_command(self, cmd, verbose=False, force=False):
        if cmd == 'java': return False
        path  = self.path[cmd]
        verbose = True
        if setup.check_command(cmd, path, verbose=verbose) and not force:
            if verbose: sys.stdout.write('# Command [%s%s] is already installed.\n' %(cmd, " "*(10-len(cmd))))
            return 0
            
        if verbose: sys.stdout.write('# Installing Command [%s%s] ...\n' % (cmd, " "*(10-len(cmd))))
        return self._install_package(cmd, verbose=verbose, force=force)

    def _post_install_rtm_cpp_darwin(self, verbose=False, force=False):
        sys.stdout.write(' - Please check license agreement of Xcode.\n')
        cmd = ['xcodebuild', '-license']
        ret = subprocess.call(cmd)
        if ret < 0:
            return -1
            
        srcdir = '/usr/local/lib/python2.7/site-packages' 
        distdir = os.path.split(wasanbon.__path__[0])[0]
        sys.stdout.write(' - Copying omniORBpy modules\n');
        for file in os.listdir(srcdir):

            filepath = os.path.join(srcdir, file)
            distpath = os.path.join(distdir, file)
            if verbose: sys.stdout.write('# Copying %s to %s\n' % (filepath, distpath))

            if os.path.isfile(filepath):
                if os.path.isfile(distpath) and force:
                    os.remove(distpath)
                if not os.path.isfile(distpath):
                    shutil.copy2(filepath, distpath)
            elif os.path.isdir(filepath):
                if os.path.isdir(distpath) and force:
                    shutil.rmtree(distpath)
                if not os.path.isdir(distpath):
                    shutil.copytree(os.path.join(srcdir, file), os.path.join(distdir, file))

    def _install_package(self, pack, verbose=False, force=False, install_path=None):
        if self._is_installed(pack, verbose=verbose) and not force:
            if verbose: sys.stdout.write('# %s is already installed.\n' % pack)
            return 0
        if install_path is None:
            install_path = wasanbon.home_path
            
        import yaml
        from wasanbon import util
        package_dict = yaml.load(open(os.path.join(self.setting_path, 'packages.yaml'), 'r'))
        
        if sys.platform == 'darwin':
            #if pack == 'eclipse':
            #    return setup.download_and_unpack(wasanbon.setting()[wasanbon.platform()]['packages'][pack],
            #                                     path=wasanbon.home_path, 
            #                                     verbose=verbose, force=force)    

            retval = setup.download_and_install(package_dict[pack],
                                                verbose=verbose, force=force,
                                                temppath = wasanbon.temp_path,
                                                installpath = wasanbon.home_path)
            if pack == 'rtm_c++':
                self._post_install_rtm_cpp_darwin(verbose=verbose, force=force)

            return 0


        elif sys.platform == 'win32':

            if pack == 'emacs':
                retval = setup.download_and_install(package_dict[pack],
                                                  verbose=verbose,
                                                  force=force, 
                                                  temppath=os.path.join(wasanbon.temp_path, pack),
                                                  installpath=wasanbon.home_path)

                import shutil
                shutil.move(os.path.join(wasanbon.temp_path, 'emacs', 'emacs-23.4-bin-i386'),
                            os.path.join(wasanbon.home_path, 'emacs'))

                return retval
            elif pack == 'eclipse':
                retval = setup.download_and_install(package_dict[pack],
                                                  verbose=verbose,
                                                  force=force, 
                                                  temppath=os.path.join(wasanbon.temp_path, pack),
                                                  installpath=None)
                extracted_eclipse_dir = os.path.join(wasanbon.temp_path, 'eclipse')
                extracted_eclipse_dir_path= None
                for root, dirs, files in os.walk(extracted_eclipse_dir):
                    for f in files:
                        if f == 'eclipse.exe':
                            sys.stdout.write('## eclipse.exe found.\n')
                            extracted_eclipse_dir_path = root

                import shutil
                shutil.move(extracted_eclipse_dir_path, 
                            os.path.join(wasanbon.home_path, 'eclipse'))

                return retval
            else:
                return setup.download_and_install(package_dict[pack],
                                                  verbose=verbose,
                                                  force=force, 
                                                  temppath=os.path.join(wasanbon.temp_path, pack),
                                                  installpath=wasanbon.home_path)
        elif sys.platform == 'linux2':
            if pack == 'rtm_c++':
                apt_prepare()
            return setup.download_and_install(package_dict[pack],
                                              verbose=verbose,
                                              force=force,
                                              temppath=os.path.join(wasanbon.temp_path, pack),
                                              installpath=wasanbon.home_path)
            #wasanbon.setting()[wasanbon.platform()]['packages'][pack],
            #                                 verbose=verbose, force=force, path=wasanbon.temp_path)
        raise wasanbon.UnsupportedPlatformError()


    def _update_path(self, verbose=False):
        self._copy_path_yaml_from_setting_dir(force=False, verbose=verbose)
        import yaml
        path_filename = os.path.join(wasanbon.home_path, 'path.yaml')
        dir = yaml.load(open(path_filename, 'r'))
        hints = yaml.load(open(os.path.join(self.setting_path, 'hints.yaml'), 'r'))
            


        path_dict = {}
        for key, value in dir.items():
            hints_org = hints[key]
            hints_ = [h.replace('$HOME', wasanbon.get_home_path()) for h in hints_org]
            new_path = setup.search_command(key, value, hints_, verbose=verbose)
            path_dict[key] = new_path

        yaml.dump(path_dict, open(path_filename, 'w'), encoding='utf8', allow_unicode=True, default_flow_style=False)

    def _copy_path_yaml_from_setting_dir(self, force=False, verbose=False):
        src = os.path.join(self.setting_path, 'path.yaml')
        dst = os.path.join(wasanbon.home_path, 'path.yaml')
        if not os.path.isfile(dst) or force:
            shutil.copy2(src, dst)


    def _is_installed(self, pack, verbose=False):
        if pack == 'rtm_c++':
            return self._is_rtmcpp_installed()
        elif pack == 'rtm_java':
            return self._is_rtmjava_installed()
        elif pack == 'rtm_python':
            try:
                try:
                    # If rtctree is already installed,
                    # the rtctree must be imported before OpenRTM_aist.
                    # because the rtctree partly uses original IDL and modules 
                    # compatible with OpenRTM_aist
                    import rtctree
                except:
                    pass
                import OpenRTM_aist
                del OpenRTM_aist
                return True
            except ImportError, e:
                traceback.print_exc()
                return False
        elif pack == 'rtctree':
            try:
                import rtctree
                return True
            except ImportError, e:
                return False
        elif pack == 'rtsprofile':
            try:
                import rtsprofile
                return True
            except ImportError, e:
                return False
        elif pack == 'rtshell':
            try:
                import rtshell
                return True
            except ImportError, e:
                return False
        sys.stdout.write('# Unsupported package name %s\n' % pack)
        return False
                

    def _find_file(self, dirs, filename):
        for d in dirs:
            if os.path.isfile(os.path.join(d, filename)):
                return True
        return False

    def _is_rtmcpp_installed(self):
        if sys.platform == 'darwin':
            paths = ['/usr/local/include/openrtm-1.1/rtm', '/usr/include/openrtm-1.1/rtm', '/opt/local/include/openrtm-1.1/rtm']
            if ('RTM_ROOT' in os.environ.keys()):
                paths.append(os.path.join(os.environ['RTM_ROOT'], 'rtm'))
            return self._find_file(paths, 'version.txt')

        elif sys.platform == 'linux2':
            paths = ['/usr/local/include/openrtm-1.1/rtm', '/usr/include/openrtm-1.1/rtm']
            if ('RTM_ROOT' in os.environ.keys()):
                paths.append(os.path.join(os.environ['RTM_ROOT'], 'rtm'))
            return self._find_file(paths, 'version.txt')

        elif sys.platform == 'win32':
            files = ['version.txt',
                     'version.h']
            paths = ['C:\\Program Files (x86)\\OpenRTM-aist\\1.1\\rtm',
                     'C:\\Program Files\\OpenRTM-aist\\1.1\\rtm']
            if ('RTM_ROOT' in os.environ.keys()):
                paths.append(os.path.join(os.environ['RTM_ROOT'], 'rtm'))
            for f in files:
                if self._find_file(paths, f):
                    return True
            return False

        raise wasanbon.UnsupportedPlatformError()
        

    def _is_rtmjava_installed(self):
        jardir = os.path.join(wasanbon.home_path, 'jar')
        if not os.path.isdir(jardir):
            os.mkdir(jardir)
        for f in os.listdir(jardir):
            if f.endswith('.jar') and f.startswith('OpenRTM'):
                return True
        return False


def apt_prepare():
    import subprocess
    output = subprocess.check_output(['lsb_release', '-c']).split(':')[1].strip()

    srcsfile = '/etc/apt/sources.list.d/openrtm-aist.list'
    key1 = 'deb http://www.openrtm.org/pub/Linux/ubuntu/ %s main\n' % output
    #key2 = 'deb http://www.openrtm.org/pub/Linux/ubuntu/ precise-unstable main'                                                                                                                                
    if os.path.isfile(srcsfile):
        flag1 = False
            #flag2 = False                                                                                                                                                                                      
        file = open(srcsfile, 'r+w')
        for line in file:
            if line.strip() == key1:
                flag1 = True
                #if line.strip() == key2:                                                                                                                                                                       
                #    flag2 = True                                                                                                                                                                               

        if not flag1:
            file.write(key1)
        #if not flag2:                                                                                                                                                                                          
	#    file.write(key2)                                                                                                                                                                                   
        file.close()
    else:
        file = open(srcsfile, 'w')
        file.write(key1)
	#file.write(key2)                                                                                                                                                                                       
	file.close()

    subprocess.call(['apt-get', 'update'])
    
