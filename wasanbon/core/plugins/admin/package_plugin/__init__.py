import os, sys, traceback, optparse, subprocess
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest


class Plugin(PluginFunction):
    """ This plugin provides package access command and APIs """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        #import package
        #package.plugin_obj = self
        pass

    def depends(self):
        return ['admin.environment', 'admin.rtcconf', 'admin.rtc', 'admin.systemlauncher']

    #@property
    #def package(self):
    #    import package
    #    return package

    def print_packages(self, args):
        packages = self.get_packages()
        for p in packages:
            print p.name

    def create_package(self, prjname, verbose=False, overwrite=False, force_create=False):
        return create_package(prjname, verbose=verbose, overwrite=overwrite, force_create=force_create)

    @manifest
    def list(self, args):
        """ List Packages installed this machie.
        # Usage $ wasanbon-admin.py package list [-l, -v]
        """
        self.parser.add_option('-l', '--long', help='Long Format (default=False)', default=False, action='store_true', dest='long_flag')
        self.parser.add_option('-q', '--quiet', help='Verbosity option (default=False)', default=False, action='store_true', dest='quiet_flag')
        self.parser.add_option('-r', '--running', help='List Running Package only', default=False, action='store_true', dest='running_flag')
        options, argv = self.parse_args(args[:])

        verbose = options.verbose_flag
        running_only = options.running_flag
        if options.quiet_flag: verbose = False
        long = options.long_flag

        #import package
        
        packages = sorted(self.get_packages(verbose=verbose), key= lambda x : x.name)
        
        for p in packages:
            if running_only:
                if not admin.systemlauncher.is_launched(p, verbose=verbose):
                    continue
            if not long:
                print p.name
            else:
                print '%s : ' % p.name
                print '  description : %s' % p.description
                print '  path : '
                print '    root   : %s' % p.path
                print '    rtc    : %s' % p.get_rtcpath(fullpath=False)
                print '    conf   : %s' % p.get_confpath(fullpath=False)
                print '    bin    : %s' % p.get_binpath(fullpath=False)
                print '    system : %s' % p.get_systempath(fullpath=False)
                print '  rtcs : '
                for r in admin.rtc.get_rtcs_from_package(p):
                    print '   -  %s ' % r.rtcprofile.basicInfo.name
                print '  nameservers : %s' % p.setting.get('nameservers', '')
                print '  conf:'
                print '    C++    : %s' % os.path.basename(p.rtcconf['C++'])
                print '    Python : %s' % os.path.basename(p.rtcconf['Python'])
                print '    Java   : %s' % os.path.basename(p.rtcconf['Java'])
                print '  defaultSystem : %s' % p.default_system_filepath
                print '  running  : %s' % admin.systemlauncher.is_launched(p)
        return 0

    
    
    @manifest
    def directory(self, args):
        """ Show Directory of Package.
        Usage: wasanbon-admin.py package directory [PROJ_NAME] """
        options, argv = self.parse_args(args[:], self.print_packages)
        verbose = options.verbose_flag

        #import package
        packages = self.get_packages(verbose=verbose)
        for p in packages:
            if p.name == argv[3]:
                print p.path

        return 0
    
    @manifest
    def create(self, args):
        """ Create Package
        # Usage $ wasanbon-admin.py package create [PACK_NAME]  """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag

        wasanbon.arg_check(argv, 4)
        sys.stdout.write('# Creating package %s\n' % args[3])
        #import package
        return self.create_package(prjname = argv[3], verbose=verbose)

    @manifest
    def register(self, args):
        """ Register Package 
        # Usage $ wasanbon-admin.py package reigster [PACKAGE_PATH] """
        options, argv = self.parse_args(args[:], self.print_packages)
        verbose = options.verbose_flag

        package_path = argv[3]
        if not os.path.isabs(package_path):
            package_path = os.path.normpath(os.path.join(os.getcwd(), package_path))
            
        if not os.path.isdir(package_path):
            sys.stdout.write('# Can not find %s.\n' % package_path)
            return -1

        setting_file_path = os.path.join(package_path, 'setting.yaml')
        if not os.path.isfile(setting_file_path):
            sys.stdout.write('# Setting file %s can not be found.' % setting_file_path)
            return -1

        p = PackageObject(path=package_path)
        sys.stdout.write('# Registering Package %s\n' % p.name)


        register_package(p.name, p.path)

        return 0
            
    
    @manifest
    def delete(self, args):
        """ Delete Package
        # Usage $ wasanbon-admin.py package delete [PACK_NAME]
         -r : remove directory (default False) """

        self.parser.add_option('-r', '--remove', help='Remove All Files (default=False)', default=False, action='store_true', dest='remove_flag')
        options, argv = self.parse_args(args[:], self.print_packages)
        verbose = options.verbose_flag
        remove = options.remove_flag

        wasanbon.arg_check(args, 4)
        retval = 0
        for n in argv[3:]:
            sys.stdout.write('# Removing package %s\n' % n)
            ret = self.delete_package(n, deletepath=remove, verbose=verbose)
            if ret != 0:
                retval = 1
        return retval
    
    def delete_package(self, package_name, deletepath=False, verbose=False):
        return delete_package(package_name, deletepath=deletepath, verbose=verbose)


    def get_package_from_path(self, path, verbose=False):
        return get_package_from_path(path, verbose=verbose)


    def get_packages(self,verbose=False, force=True):
        return get_packages(verbose=verbose, force=force)

    def get_package(self, name, verbose=False):
        return get_package(name, verbose=verbose)

    def validate_package(self, package, verbose=False, autofix=False, interactive=False, ext_only=False):
        return validate_package(package, verbose=verbose, autofix=autofix, interactive=interactive, ext_only=ext_only)

import os, sys, types, subprocess
import wasanbon

def parse_and_copy(src, dist, dic, verbose=False):
    fin = open(src, "r")
    fout = open(dist, "w")
    for line in fin:
        for key, value in dic.items():
            index = line.find(key)
            if index >= 0:
                line = line[:index] + value + line[index + len(key):]
        fout.write(line)
    fin.close()
    fout.close()

def load_workspace(verbose=False):
    ws_file_name = os.path.join(wasanbon.home_path, "workspace.yaml")
    if not os.path.isfile(ws_file_name):
        if verbose:
            sys.stdout.write(' - Can not find workspace.yaml: %s\n' % ws_file_name)
            sys.stdout.write(' - Creating workspace.yaml\n')
        open(ws_file_name, "w").close()
        return {}
    else:
        if verbose: sys.stdout.write(' - Opening workspace.yaml.\n')
        import yaml
        y= yaml.load(open(ws_file_name, "r"))
        if not y: y = {}
        return y

def save_workspace(dic):
    ws_file_name = os.path.join(wasanbon.home_path, 'workspace.yaml')
    import yaml
    yaml.dump(dic, open(ws_file_name, 'w'), encoding='utf8', allow_unicode=True, default_flow_style=False)


def create_package(prjname, verbose=False, overwrite=False, force_create=False):
    projs = get_packages(verbose)
    proj_names = [prj.name for prj in projs]
    if prjname in proj_names:
        if verbose: sys.stdout.write(' - There is %s package in workspace.yaml already\n' % prjname)
        raise wasanbon.PackageAlreadyExistsException()

    tempdir = os.path.join(wasanbon.__path__[0], 'template')
    appdir = os.path.join(os.getcwd(), prjname)
    if not force_create:
        if os.path.isdir(appdir) or os.path.isfile(appdir):
            if verbose: sys.stdout.write(' - There seems to be %s here. Please change application name.\n' % prjname)
            raise wasanbon.DirectoryAlreadyExistsException()

    for root, dirs, files in os.walk(tempdir):
        distdir = os.path.join(appdir, root[len(tempdir)+1:])
        if not os.path.isdir(distdir):
            os.mkdir(distdir)
        for file in files:
            if os.path.isfile(os.path.join(distdir, file)) and not overwrite:
                pass
            else:
                if verbose:
                    sys.stdout.write(" - copy file: %s\n" % file)
                parse_and_copy(os.path.join(root, file), os.path.join(distdir, file), {'$APP' : prjname})
            
    #y = yaml.load(open(os.path.join(appdir, 'setting.yaml'), 'r'))
    #file = os.path.join(wasanbon.__path__[0], 'settings', sys.platform, 'repository.yaml')
    #shutil.copy(file, os.path.join(appdir, y['application']['RTC_DIR'], 'repository.yaml'))
    
    if sys.platform == 'darwin' or sys.platform == 'linux2':
        cmd = ['chmod', '755', os.path.join(prjname, 'mgr.py')]
        subprocess.call(cmd)
        
    register_package(prjname, appdir)
    return 0

def register_package(prjname, appdir):
    y = load_workspace()
    y[prjname] = appdir
    save_workspace(y)
    return 0


def delete_package(name, deletepath=False, verbose=False):
    p = get_package(name)
    
    dic = load_workspace()
    dic.pop(p.name)
    save_workspace(dic)

    if deletepath:
        import shutil, stat
        def remShut(*args):
            func, path, _ = args 
            os.chmod(path, stat.S_IWRITE)
            os.remove(path)
        shutil.rmtree(p.path, onerror = remShut)
    return 0
        

def validate_package(package, verbose=False, autofix=False, interactive=False, ext_only=False):
    for lang in ['C++', 'Java', 'Python']:
        rtcc = admin.rtcconf.RTCConf(package.rtcconf[lang])
        if lang == 'C++':
            rtcc.ext_check(verbose=verbose, autofix=autofix, interactive=interactive)
        if not ext_only:
            rtcc.validate(verbose=verbose, autofix=autofix, interactive=interactive)
        rtcc.sync()
    
def get_packages(verbose=False, force=True):
    y = load_workspace()
    projs = []
    if type(y) != types.NoneType:
        for key, value in y.items():
            try:
                projs.append(PackageObject(name=key, path=value))
            except wasanbon.InvalidPackagePathError, ex:
                if force:
                    if verbose:
                        sys.stdout.write(' - Invalid Package Path (%s:%s)\n' % (key,value))
                        pass
                else:
                    raise wasanbon.PackageNotFoundException()
    return projs


def get_package(name, verbose=False):
    y = load_workspace()
    if not name in y.keys():
        raise wasanbon.PackageNotFoundException()
    return PackageObject(name=name, path=y[name])


def get_package_from_path(path, verbose=False):
    if verbose:
        sys.stdout.write('# Searching Package from path(%s)\n' % path)
    y = load_workspace()
    for key, value in y.items():
        if value == path:
            return PackageObject(name=key, path=value)
    

    raise wasanbon.PackageNotFoundException()



import os, sys

#plugin_obj = None


class PackageObject(object):

    def __init__(self, name=None, path=None):

        self._path = path
        self._setting_file_path = os.path.join(path, 'setting.yaml')
        if not os.path.isfile( self._setting_file_path):
            import wasanbon
            raise wasanbon.InvalidPackagePathError()
        self._setting = None
        self._rtcconf = None

        if name:
            self._name = name
        else:
            self._name = self.setting['name']
                
    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def setting_file_path(self):
        return self._setting_file_path

    @property
    def description(self):
        return self.setting.get('description', '""')

    @property
    def setting(self):
        if self._setting is None:
            import yaml
            self._setting = yaml.load(open(self._setting_file_path, 'r'))
        return self._setting['application']

    def get_binpath(self, fullpath=True):
        dir = self.setting.get('BIN_DIR', "bin")
        if fullpath:
            return os.path.join(self.path, dir)
        return dir

    def get_systempath(self, fullpath=True):
        dir = self.setting['RTS_DIR']
        if fullpath:
            return os.path.join(self.path, dir)
        return dir


    def get_confpath(self, fullpath=True):
        dir = self.setting.get('CONF_DIR', 'conf')
        if fullpath:
            return os.path.join(self.path, dir)
        return dir

    def get_rtcpath(self, fullpath=True):
        dir = self.setting.get('RTC_DIR', 'rtc')
        if fullpath:
            return os.path.join(self.path, dir)
        return dir

    @property
    def rtc_repository_file(self):
        return os.path.join(self.get_rtcpath(), 'repository.yaml')

    def __repr__(self):
        return self.name + '(' + self.path + ')'

    @property
    def default_system_filepath(self, fullpath=True):
        system_file = self.setting['system']
        if fullpath:
            path = self.path
        else:
            path = ""
        old_manner = os.path.join(path, system_file)
        if os.path.isfile(old_manner):
            sys.stdout.write('# This package contains old manner system description\n')
            return old_manner
        file = os.path.join(path, self.get_systempath(), system_file)
        #if os.path.isfile(file):
        #    return file
        #return None
        return file

    @property
    def rtcconf(self):
        #from . import plugin_obj
        if self._rtcconf is None:
            self._rtcconf = {}
            #import wasanbon
            for lang in ['C++', 'Java', 'Python']:
                path = os.path.join(self.path, self.setting['conf.'+lang])
                if os.path.isfile(path):
                    sys.stdout.write('# setting.yaml is written in old manner.\n')
                    sys.stdout.write('# conf.%s must be filename, and path of conffile must be writtein in CONF_DIR\n'%lang)
                else:
                    path = os.path.join(self.get_confpath(), self.setting['conf.'+lang])
                if not os.path.isfile(path):
                    sys.stdout.write('# Config file %s is not found.\n' % path)
                    continue
                #self._rtcconf[lang] = plugin_obj.admin.rtcconf.rtcconf.RTCConf(path) #wasanbon.plugins.admin.rtcconf.rtcconf.RTCConf(path)
                self._rtcconf[lang] = path
        return self._rtcconf


    @property
    def standalone_rtc_commands(self):
        return self.setting.get('standalone', [])
