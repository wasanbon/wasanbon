import os, sys, traceback
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest


default_setting_dic = {
    'user': None,
    'password' : None,
    'list_filename' : 'application_list.html',
    'appshare_url': 'http://sugarsweetrobotics.com/pub/wasanbon/web/applications/',
    'upload_host' : 'ysuga.net',
    'upload_dir'  : '/home/ysuga/www/ssr/www2/pub/wasanbon/web/applications/'
}

class Plugin(PluginFunction):
    """ Plugin for Web interface """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def _print_alternative_packages(self, argv):
        packages = self.get_packages()
        for p in packages:
            sys.stdout.write('%s\n' % p)
        return 0
        
    def depends(self):
        return ['admin.environment']

    def sigusr1_isr(self, signal, stack):
        from twisted.internet import reactor
        pass
    def sigint_isr(self, signal, stack):
        sys.stdout.write(' - SIGINT captured.\n')
        from twisted.internet import reactor
        reactor.stop()


    @property
    def web_dir(self):
        return os.path.join(wasanbon.home_path, 'web')

    @property
    def app_dir(self):
        return os.path.join(self.web_dir, 'applications')

    @property
    def pack_dir(self):
        return os.path.join(self.web_dir, 'packages')

    @manifest
    def init(self, args):
        self.parser.add_option('-f', '--force', help='Force Initialize Setting', default=False, action='store_true',  dest='force')
        
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        force = options.force

        if not os.path.isdir(self.web_dir):
            os.mkdir(self.web_dir)
        
        if not os.path.isdir(self.app_dir):
            os.mkdir(self.app_dir)
        
        if not os.path.isdir(self.pack_dir):
            os.mkdir(self.pack_dir)

        style_file = 'index.css'
        style_file_path = os.path.join(self.app_dir, style_file)
        if not os.path.isfile(style_file_path):
            import shutil
            shutil.copy(os.path.join(__path__[0], 'styles', style_file), style_file_path)

        if (not os.path.isfile(os.path.join(wasanbon.get_wasanbon_home(), 'web', 'web_setting.yaml'))) or force:
            import yaml
            print 'CP', yaml.dump(default_setting_dic)
            with open(os.path.join(wasanbon.get_wasanbon_home(), 'web', 'web_setting.yaml'), 'w') as f:

                f.write(yaml.dump(default_setting_dic))
                f.close()
        self.download_from_appshare('Apps')
        self.install_app('Apps', force=force, verbose=verbose)
        self.download_from_appshare('Setting')
        self.install_app('Setting', force=force, verbose=verbose)

    def download_from_appshare(self, appname, version=None):
        dic = self.get_app_dict()
        if not appname in dic.keys():
            sys.stdout.write('Error. %s can not be found in AppShare.\n' % appname)
            return -1

        if version:
            if not version in dic[appname].keys():
                sys.stdout.write('Error. %s version %s can not be found in AppShare.\n' % (appname, version))
                return -2

        else:
            vs = dic[appname].keys()
            vs.sort()
            version = vs[-1]

        url = self.appshare_url + dic[appname][version]['url']
        sys.stdout.write('# Downloading %s-%s from url (%s)\n' % (appname, version, url))
        
        import urllib2
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        target_file = os.path.join(self.pack_dir, dic[appname][version]['url'])
        if sys.platform == 'win32':
            CHUNK = 16*1024
            fout = open(target_file, 'wb')
            while True:
                chunk =  response.read(CHUNK)
                if not chunk: break
                fout.write(chunk)
            pass
        else:
            page_content = response.read()
            open(target_file, 'w').write(page_content)
            pass
        return 0

    @manifest
    def download_appshare(self, args):
        self.parser.add_option('-s', '--specify-version', help='Download application from AppShare', default=None, dest='version')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        version = options.version
        
        wasanbon.arg_check(argv, 4)
        appname = argv[3]
        return self.download_from_appshare(appname, version)

    @manifest
    def start(self, args):
        """ Start Web Server """
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory
        port = options.port

        pid_dir = directory
        if directory is None:
            directory = os.path.join(wasanbon.home_path, 'web', 'applications')
            pid_dir = os.path.join(wasanbon.home_path, 'web')

        sys.stdout.write('# Starting Web Application in %s\n' % directory)

        if not os.path.isdir(pid_dir):
            os.mkdir(pid_dir)
        pid_file = os.path.join(pid_dir, 'pid')
        if os.path.isfile(pid_file):
            os.remove(pid_file)

        open(pid_file, 'w').write(str(os.getpid()))

        from nevow import appserver
        from twisted.web import server
        from twisted.internet import reactor
        
        import site, rpc
        from site import resource
        from rpc import manager
        
        #self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        #options, argv = self.parse_args(args[:])
        #verbose = options.verbose_flag # This is default option
        #force   = options.force_flag


        import signal
        
        #if sys.platform == 'win32':
        #    SIGUSR1 = 30
        #else:
        #    SIGUSR1 = signal.SIGUSR1
        #    pass
        
        #signal.signal(SIGUSR1, self.sigusr1_isr) # SIGUSR1 = 30 -
        signal.signal(signal.SIGINT, self.sigint_isr) # SIGUSR1 = 30

        #if directory is None:
        #    directory = os.path.join(__path__[0], 'www')
        if not os.path.isdir(directory):
            directory = os.path.join(os.getcwd(), directory)
            if not os.path.isdir(directory):
                sys.stdout.write('%s not found\n' % directory)
                #raise wasanbon.InvalidArgumentException()
                os.mkdir(directory)

        work_directory = directory
        self.res = resource.ResourceManager(directory)
        self.res.putChild('RPC', manager.RpcManager(directory=work_directory, verbose=verbose));
        self.site = appserver.NevowSite(self.res)
        reactor.listenTCP(port, self.site)
        reactor.run()
        sys.stdout.write(' - Web reactor stopped.\n')
        os.remove(pid_file)
        return 0

    @manifest
    def stop(self, args):
        """ Stop Web Server """
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory
        port = options.port

        pid_dir = directory
        if directory is None:
            directory = os.path.join(wasanbon.home_path, 'web', 'applications')
            pid_dir = os.path.join(wasanbon.home_path, 'web')

        sys.stdout.write('# Stopping Web Application in %s\n' % directory)

        pid_file = os.path.join(pid_dir, 'pid')

        if not os.path.isfile(pid_file):
            sys.stdout.write(' - Server not found.\n')
            return -1
        import signal
        pid = int(open(pid_file, 'r').read())
        if verbose: sys.stdout.write('# Stopping Web Service (PID = %s)\n' % pid)
        try:
            os.kill(pid, signal.SIGINT)
        except:
            print '# Exception in Stopping Web Service.'
            traceback.print_exc()
            
            print '# Searching wasanbon-admin.py processes......'
            import psutil
            for p in psutil.process_iter():
                try:
                    cl = p.cmdline()
                    python_flag = False
                    wsbadm_flag = False
                    web_flag = False
                    start_flag = False
                    for c in cl:
                        if c.find('python') >= 0: python_flag = True
                        if c.find('wasanbon-admin.py') >= 0: wsbadm_flag = True
                        if c.find('web') >= 0: web_flag = True
                        if c.find('start') >= 0: start_flag = True

                    if all([python_flag, wsbadm_flag, web_flag, start_flag]):
                        print '# Found wasanbon-admin.py web process(PID=%s)', p.pid
                        # Found
                        p.kill()
                except:
                    continue

        return 0
        

    @manifest
    def restart(self, args):
        """ Restarting Web Server """
        self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        self.parser.add_option('-t', '--timedelay', help='Delay time for stopping server', type='int', default=0, dest='delay')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        directory = options.directory
        delay = options.delay
        port = options.port

        def _restart():
            self.stop(args)
            import time
            time.sleep(0.5)
            self.start(args)

        _restart()

        return 0
        

    def get_packages(self, without_version=False):
        """ List packages """
        package_names = []
        for f in os.listdir(self.pack_dir):
            if f.endswith('.zip'):
                pn = f[0:-4]
                if without_version:
                    pn = pn.split('-')[0]
                package_names.append(pn)

        return package_names

    def get_applications(self):
        """ List applications """

        app_names = []
        for f in os.listdir(self.app_dir):

            path = os.path.join(self.app_dir, f)
            if os.path.isdir(path):
                app_names.append(f)
        return app_names

    @manifest
    def package_dir(self, args):
        #self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        sys.stdout.write('%s\n' % self.pack_dir)
        return 0
    
    @manifest
    def packages(self, args):
        #self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        #directory = options.directory
        package_names = self.get_packages()
        sys.stdout.write('# Install ready packages:\n')
        for p in package_names:
            sys.stdout.write(' - %s\n' % p)
        return 0

    @manifest
    def applications(self, args):
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        package_names = self.get_applications()
        sys.stdout.write('# Installed Applications:\n')
        for p in package_names:
            sys.stdout.write(' - %s\n' % p)
        return 0
        
    @manifest
    def install(self, args):
        """ install application """
        self.parser.add_option('-s', '--specify-version', help='Specify Version of App', default=None, dest='version')
        self.parser.add_option('-f', '--force', help='Force install', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(args[:], self._print_alternative_packages)
        verbose = options.verbose_flag # This is default option
        version = options.version
        force = options.force_flag

        wasanbon.arg_check(argv, 4)
        appname = argv[3]

        if appname == 'all':
            apps = []
            for p in self.get_packages():
                n = p.split('-')[0]
                if not n in apps:
                    apps.append(n)
        else:
            apps = [appname]

        for app in apps:
            self.install_app(app, version, force)

        return 0


    def install_app(self, appname, version=None, force=False, verbose=False):
        # Check if Web Application is already installed or not
        #if not app_name in package_names
        #    sys.stdout.write('''# Argument '%s' is not ready to install.\n
        # Place .zip package file in the packages package_dir in %s''' % (app_name, package_dir))
        #    return -1

        if version is None:
            versions = []
            for f in os.listdir(self.pack_dir):
                if f.startswith(appname) and f.endswith('.zip'):
                    v = f.split('-')[-1][:-4]
                    versions.append(v)
            versions.sort()
            version = versions[-1]
        
        package_path = os.path.join(self.pack_dir, appname + '-' + version + '.zip')
        if not os.path.isfile(package_path):
            sys.stdout.write('# Can not find package (%s).\n' % package_path)
            return -1


        # Check if Web Application is already installed or not
        for an in self.get_applications():
            if an.split('-')[0] != appname:
                continue

            sys.stdout.write('''# '%s' is already installed.\n''' % (an))
                
            if not force:
                sys.stdout.write('# Add -f option to force installing.\n')
                return -1
            
            sys.stdout.write('# Removing installed %s application\n' % an)
            import shutil
            shutil.rmtree(os.path.join(self.app_dir, an))

        sys.stdout.write('# Installing %s.\n' % (appname))

        import zipfile
        z = zipfile.ZipFile(package_path)

        cwd = os.getcwd()
        os.chdir(self.app_dir)

        for n in z.namelist():
            if verbose: sys.stdout.write(' - %s\n' % n)
            z.extract(n)


        print z.namelist()[0]
        if z.namelist()[0].find('-') < 0:
            name = z.namelist()[0]
            if name.endswith('/'):
                name = name[:-1]
            os.rename(z.namelist()[0], name + '-' + version)

        os.chdir(cwd)


    @manifest
    def uninstall(self, args):
        """ uninstall application """
        options, argv = self.parse_args(args[:], self._print_alternative_packages)
        verbose = options.verbose_flag # This is default option
        
        appdist = self.app_dir

        wasanbon.arg_check(argv, 4)

        app_name = argv[3]
        if app_name.find('-') >= 0:
            app_name = app_name.split('-')[0]

        package_names = self.get_packages()
        application_names = self.get_applications()

        for an in application_names:
            if app_name != an.split('-')[0]:
                continue

            sys.stdout.write('''# Removing '%s'.\n''' % (an))
            
            import shutil
            #os.removedirs(os.path.join(appdist, app_name))
            shutil.rmtree(os.path.join(appdist, an))

        return 0


    @manifest
    def upload_appshare(self, args):
        """ Start Web Server """
        self.parser.add_option('-d', '--description', help='Set Description', default="", dest='description')
        #self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        description = options.description
        wasanbon.arg_check(argv, 4)
        filepath = argv[3]
        
        if not os.path.isfile(filepath):
            sys.stdout.write(' - file (%s) not found.\n')
        
        import apps
        apps.update_cache(url=self.applist_url, verbose=verbose)
        dic = self.get_setting_dic()
        user = dic['user']
        password = dic['password']
        apps.upload(filepath, user, password, self.applist_filename, hostname=self.upload_host, dir=self.upload_dir, description=description)
        return 0

    @property
    def applist_filename(self):
        dic = self.get_setting_dic()
        return dic.get('list_filename', '')

    @property
    def applist_url(self):
        return self.appshare_url + self.applist_filename
        
    @property
    def appshare_url(self):
        dic = self.get_setting_dic()
        url= dic['appshare_url']
        if not url.endswith('/'):
            url = url + '/'
        return url

    @property
    def upload_host(self):
        dic = self.get_setting_dic()
        return dic['upload_host']

    @property
    def upload_dir(self):
        dic = self.get_setting_dic()
        return dic['upload_dir']

    def get_setting_dic(self, verbose=True):
        user = None
        password = None
        dic = {}
        if not os.path.isfile('web_setting.yaml') and not os.path.isfile(os.path.join(wasanbon.get_wasanbon_home(), 'web', 'web_setting.yaml')):
            dic = default_setting_dic
        else:
            import yaml
            if os.path.isfile('web_setting.yaml'):
                dic = yaml.load(open('web_setting.yaml', 'r').read())
            else:
                dic = yaml.load(open(os.path.join(wasanbon.get_wasanbon_home(), 'web', 'web_setting.yaml'), 'r').read())
                pass

        if dic is None:
            if verbose: sys.stdout.write('# Invalid web_setting_file (./web_setting.yaml or ~/.wasanbon/web/web_setting.yaml\n')
            dic = default_setting_dic
        return dic

    def get_app_dict(self, verbose=False):
        # print self.applist_url
        import apps
        apps.update_cache(url=self.applist_url, verbose=verbose)
        dic = apps.cache_to_dict()
        return dic
        
    @manifest
    def list_appshare(self, args):
        """ List Applications in AppShare """
        #self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        #self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        dic = self.get_app_dict(verbose=verbose)
        import yaml
        print yaml.dump(dic, default_flow_style=False)
        return 0
    
    @manifest
    def generate_dart_app(self, args):
        """ Start Web Server """
        #self.parser.add_option('-d', '--directory', help='Set Static File Directory Tree Root', default=None, dest='directory')
        #self.parser.add_option('-p', '--port', help='Set TCP Port number for web server', type='int', default=8000, dest='port')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag # This is default option
        template_dir = os.path.join(__path__[0], 'app_template')
        app_template_name = "App Template"
        app_template_module_name = app_template_name.replace(' ', '-').lower()
        app_template_module_file_name = app_template_module_name.replace('-', '_')
        app_template_strip_name = "AppTemplate"
        app_template_dir_name = app_template_strip_name.lower()

        wasanbon.arg_check(argv, 4)
        app_name = argv[3]
        app_module_name = app_name.replace(' ', '-').lower()
        app_module_file_name = app_module_name.replace('-', '_')
        app_strip_name = ""
        for s in app_name.split(' '):
            app_strip_name = app_strip_name + s
        app_dir_name = app_strip_name.lower()
            
        sys.stdout.write('$APP_NAME       = %s\n' % app_name)
        sys.stdout.write('$APP_MODULE_NAME= %s\n' % app_module_name)
        sys.stdout.write('$APP_STRIP_NAME = %s\n' % app_strip_name)
        sys.stdout.write('$APP_DIR_NAME   = %s\n' % app_dir_name)
        
        cwd = os.getcwd()
        
        if os.path.isdir(app_dir_name):
            sys.stdout.write(' - Error. Directory %s already exists.\n' % app_dir_name)
        os.mkdir(app_dir_name)
        verbose = True

        def _replace_dir_name(src):
            src = src.replace(app_template_dir_name, app_dir_name)
            src = src.replace(app_template_module_file_name, app_module_file_name)
            return src

        def _replace_content(src):
            src = src.replace(app_template_name, app_name)
            src = src.replace(app_template_dir_name, app_dir_name)
            src = src.replace(app_template_strip_name, app_strip_name)
            src = src.replace(app_template_module_file_name, app_module_file_name)
            src = src.replace(app_template_module_name, app_module_name)
            return src
            

        def _dir_copy(src, dst):
            if verbose: sys.stdout.write(' - src is %s.\n - changing to %s\n' % (src, dst))
            os.chdir(dst)
            for s in os.listdir(src):
                src_p = os.path.join(src, s)
                if verbose: sys.stdout.write(' - parsing %s\n' % src_p)

                if os.path.isdir(src_p):
                    sys.stdout.write(' - %s is directory.\n' % src_p)
                    dir_name = _replace_dir_name(s)
                    os.mkdir(dir_name)
                    _dir_copy(src_p, dir_name)
                elif os.path.isfile(src_p):
                    sys.stdout.write(' - %s is file.\n' % src_p)
                    src_f = open(src_p, 'r')
                    dst_f = open(_replace_dir_name(s), 'w')
                    for line in src_f:
                        dst_f.write(_replace_content(line))
                    dst_f.close()

        _dir_copy(template_dir, app_dir_name)

        return 0


