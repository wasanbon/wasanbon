import os, sys, types, optparse, traceback
import wasanbon
import functools
class FunctionList(object):
    def __init__(self):
        pass

def manifest(func):
    func.__wasanbon_manifest__ = True
    @functools.wraps(func)
    def wrapper__(*args, **kwds):
        self = args[0]
        if '__doc__' in dir(func):
            usage = func.__doc__
        else:
            usage = "%s (No Comments Found)" % str(func)
        self.parser = optparse.OptionParser(usage=usage)
        self.parser.add_option('-v', '--verbose', help='Verbosity option (default=False)', default=False, action='store_true', dest='verbose_flag')
        self.parser.add_option('-a', '--alternative', help='print Alternatives of next argument (default=False)', default=False, action='store_true', dest='alt_flag')
        return func(*args, **kwds)

    return wrapper__

class PluginFunction(object):
    def __init__(self):
        self._default_property_list = ['admin', 'mgr', 'parser']
        self.admin = FunctionList()
        self.admin.__doc__ = """ This property provides the entrance for admin package plugins.
To access plugins, add the name of the plugin to be used in the list of return value of depends function """
        self.mgr   = FunctionList()
        self.mgr.__doc__ = """ This property provides the entrance for mgr package plugins.
To access plugins, add the name of the plugin to be used in the list of return value of depends function """
        self.__path__ = []

        self.parser = optparse.OptionParser(usage="", add_help_option=False)
        self.parser.__doc__ = """optparse.OptionParser. This parser has default options '-v/--versbose and -a/--alternative'. 
Plugin developer does not have to handle -a/--alternative options explicitly. 
if -v is set, options.verbose_flag is set, which must be handled by developer of each plugin. """
        self.parser.add_option('-v', '--verbose', help='Verbosity option (default=False)', default=False, action='store_true', dest='verbose_flag')
        self.parser.add_option('-a', '--alternative', help='print Alternatives of next argument (default=False)', default=False, action='store_true', dest='alt_flag')
        pass

    __special_functions = ['depends', 'parse_args', 'get_manifest_functions',
                           'get_manifest_function_names', 'is_manifest_plugin',
                           'get_functions', 'get_function_names']
    def depends(self):
        return []

    def parse_args(self, arg, print_alt_func=None):
        options, argv =  self.parser.parse_args(arg)
        if options.alt_flag:
            if print_alt_func == None:
                print ' '
                raise wasanbon.PrintAlternativeException()
            else:
                print_alt_func(arg)
                raise wasanbon.PrintAlternativeException()

        return options, argv

    def get_manifest_functions(self):
        return []


    def get_manifest_function_names(self, verbose=False, nocall=False):
        func_names = []
        for name in dir(self):
            if name != '__call__' and name.startswith('_'):
                continue
            if nocall and name == '__call__':
                continue
            if name in self.__special_functions:
                continue
            func = getattr(self, name)
            if type(func) is types.MethodType:
                if '__wasanbon_manifest__' in dir(func):
                    func_names.append(name)
        return func_names

    def is_manifest_plugin(self):
        return len(self.get_manifest_function_names()) != 0

    def get_functions(self, verbose=False):
        functions_dic = {}
        for name in dir(self):
            if name != '__call__' and name.startswith('_'):
                continue
            func = getattr(self, name)
            if type(func) is types.MethodType:
                functions_dic[name] = func
        return functions_dic

    def get_properties(self, verbose=False):
        properties = {}
        for name in dir(self):
            if name.startswith('_'):
                continue
            if name in self._default_property_list:
                continue
            prop = getattr(self, name)
            if not type(prop) is types.MethodType:
                properties[name] = prop
        return properties
        
    def get_function_names(self, verbose=False):
        return self.get_functions(verbose).keys()

    
class Loader():
    
    ext = '_plugin'
    filename = 'plugin.yaml'

    def __init__(self, directories, verbose=False):
        self._mgr = FunctionList()
        self._admin = FunctionList()
        self._package = {}
        self._package['admin'] = self._admin
        self._package['mgr'] = self._mgr

        self._directories = directories
        self._plugin_list = {}
        for d in directories:
            self.list_plugins(d, verbose=verbose)

        for name, dir in self._plugin_list.items():
            if verbose: sys.stdout.write('# Loading %s plugin\n' % name)
            self.load_plugin(name, dir, verbose=verbose)

    def get_plugin_names(self, package, nocall=False, verbose=False):
        """ Get Plugin Names in Package [admin|mgr] """
        return [p for p in dir(self._package[package]) if not p.startswith('_')]

    def get_plugins(self, package):
        return [getattr(self._package[package], n) for n in self.get_plugin_names(package)]

    def get_plugin(self, package, name):
        return getattr(self._package[package], name)

    """
    def get_admin_plugin_names(self, nocall=False):
        return get_plugin_names('admin', nocall)

    def get_admin_plugins(self):
        return [getattr(self._admin, n) for n in self.get_admin_plugin_names()]

    def get_admin_plugin(self, name):
        return getattr(self._admin, name)

    def get_mgr_plugin_names(self):
        return [p for p in dir(self._mgr) if not p.startswith('_')]

    def get_mgr_plugins(self):
        return [getattr(self._mgr, n) for n in self.get_mgr_plugin_names()]

    def get_mgr_plugin(self, name):
        return getattr(self._mgr, name)
    """

    @property
    def plugin_list(self):
        return self._plugin_list

    def list_package_plugins(self, package, directory, verbose=False):
        admin_dir = os.path.join(directory, package)
        for d in os.listdir(admin_dir):
            if d.endswith(self.ext):
                name = d[:-len(self.ext)]
                if verbose: sys.stdout.write('# Plugin: %s Found.\n' % name)
                self._plugin_list[package + '.' + name] = os.path.join(admin_dir, d)

        
    def list_plugins(self, directory, verbose=False):
        for pkg in ['admin', 'mgr']:
            if pkg in os.listdir(directory):
                self.list_package_plugins(pkg, directory, verbose=verbose)

    def load_directory(self, directory):
        sys.path.append(os.path.join(directory))
        for d in os.listdir(directory):
            if d.endswith(self.ext):
                dict_ = self.load_package_yaml(os.path.join(directory, d))
                depends_plugins = dict_.get('depends', [])
                if type(depends_plugins) != types.ListType:
                    depends_plugins = [depends_plugins]
                for p in depends_plugins:
                    if p.startswith('admin.'):
                        self.load_plugin(p, self._plugin_list[p])

                self.load_plugin(d[:-len(self.ext)], d[:-len(self.ext)])
        sys.path.pop(-1)
        pass


    def load_plugin(self, name, directory, verbose=False):
        if verbose: sys.stdout.write('# Loading (%s) in %s\n' % (name, directory))
        
        if name.startswith('admin.'):
            pack = self._admin
            func = name[6:]
        else:
            pack = self._mgr
            func = name[4:]
        mod = getattr(pack, func, None)
        if mod is not None:
            return mod
            
        sys.path.insert(0, os.path.dirname(directory))
        import imp
        try:
            file, pathname, description = imp.find_module(os.path.basename(directory))
            m = imp.load_module(name, file, pathname, description)
        except:
            sys.stdout.write('# Loading Plugin (%s) Failed.\n' % name)
            traceback.print_exc()
            return None
        if getattr(m, 'admin', None) is None: setattr(m, 'admin', FunctionList())
        if getattr(m, 'mgr', None) is None: setattr(m, 'mgr', FunctionList())
        plugin = m.Plugin()
        plugin.__path__ = [directory]
        sys.path.pop(0)

        depends_plugin_names = plugin.depends()
        if type(depends_plugin_names) == types.StringType:
            depends_plugin_names = [depends_plugin_names]
        for n in depends_plugin_names:
            if verbose: sys.stdout.write('# Plugin (%s) depends on %s.\n' % (name, n))
            if not n in self._plugin_list.keys():
                sys.stdout.write('# Plugin %s is not found when loading %s.\n' % (n, name))
                raise wasanbon.PluginDependencyNotResolvedException()

            if n.startswith('admin.'):
                if getattr(self._admin, n[6:], None) != None:
                    if verbose: sys.stdout.write('# Plugin %s is already loaded.\n')
                    p = getattr(self._admin, n[6:])
                    pass
                else:
                    if verbose: sys.stdout.write('# Plugin %s is not loaded yet.\n' % n)
                    p = self.load_plugin(n, self._plugin_list[n])

                setattr(m.admin, n[6:], p)

            elif n.startswith('mgr.'):
                if getattr(self._mgr, n[4:], None) != None:
                    if verbose: sys.stdout.write('# Plugin %s is already loaded.\n')
                    p = getattr(self._mgr, n[4:])

                    pass
                else:
                    if verbose: sys.stdout.write('# Plugin %s is not loaded yet.\n' % n)
                    p = self.load_plugin(n, self._plugin_list[n])
                    #setattr(plugin.mgr, n[4:], p)
                setattr(m.mgr, n[4:], p)
            pass

        if name.startswith('admin.'):
            setattr(self._admin, name[6:], plugin)
        elif name.startswith('mgr.'):
            setattr(self._mgr, name[4:], plugin)

        if verbose: sys.stdout.write('# Loaded (%s) \n' % name)
        return plugin

    def print_alternative(self, package, args):
        if len(args) >= 3:
            if args[2] == 'api':
                for n in self.get_plugin_names(package):
                    print n,
        else:
            print 'list api'

    def run_command(self, package, subcommand, args):
        if '-a' in args:
            self.print_alternative(package, [arg for arg in args if not arg.startswith('-')])
            return 0

        if '-h' in args or 'help' in args:
            self.print_help(package)
            return 0
        if '-l' in args or 'long' in args:
            long = True
        else: long = False

        args = [arg for arg in args if not arg.startswith('-')]

        if len(args) < 3:
            self.print_help(package)
            return -1
        
        if args[2] == 'list':
            self.print_list_plugins(package, long)
            return 0
        elif args[2] == 'api':
            if len(args) < 4:
                self.print_help(package)
                return -1
            self.show_api(package, args[3], long)


    def print_list_plugins(self, package, long=False):
        """ Print List of Plugin. This is called when application invoked with 
        plugin list argument
        """
        names = self.get_plugin_names(package)
        for name in names:
            print ' - %s:' % name
            

            plugin = self.get_plugin(package, name)
            if long:
                print '  path : ', plugin.__path__[0]
                print '  doc : |'
            if '__doc__' in dir(plugin):
                if plugin.__doc__ != None:
                    docs = [s.strip() for s in plugin.__doc__.split('\n')]
                    for d in docs:
                        print '   ', d
                else:
                    print '   (No Help)'
            else:
                print '   (No Help)'

    def show_api(self, package, plugin_name, long=False):
        """ List api of command
        """
        names = self.get_plugin_names(package)
        if not plugin_name in names:
            self.print_help(package)
            return -1
        plugin = self.get_plugin(package, plugin_name)
        sys.stdout.write('%s :\n' % plugin_name)
        sys.stdout.write('  path : %s\n' % plugin.__path__[0])
        sys.stdout.write('  properties : \n')
        properties = plugin.get_properties()
        for name, prop in properties.items():
            sys.stdout.write('    %s : |\n' % name)
            doc_ = getattr(getattr(plugin.__class__, name, None), '__doc__', None)
            if doc_:
                for line in doc_.split('\n'):
                    sys.stdout.write('      %s\n' % line.strip())
        sys.stdout.write('  methods :\n')
        functions = plugin.get_functions()
        for name, func in functions.items():
            sys.stdout.write('    %s : |\n' % name)
            doc_ = getattr(getattr(plugin.__class__, name, None), '__doc__', None)
            if doc_:
                for line in doc_.split('\n'):
                    if len(line.strip()) > 0:
                        sys.stdout.write('      %s\n' % line.strip())
            else:
                sys.stdout.write('      No doc.\n')
        

    def print_help(self, package):
        """ Print Help Message for Plugin command """
        if package == 'admin':
            print """
This command is for plugin administration.
Usage:
  $ wasanbon-admin.py plugin [subcommand]

subcommands:
  list : list plugins for package administration.
  api : list APIs in the specified plugin. use " $ wasanbon-admin.py plugin api $PLUGIN_NAME "
"""

        if package == 'mgr':
            print """
This command is for plugin administration.
Usage:
  $ mgr.py plugin [subcommand]

subcommands:
  list : list plugins for package management
  api : list APIs in the specified plugin. use " $ mgr.py plugin api $PLUGIN_NAME "
"""
