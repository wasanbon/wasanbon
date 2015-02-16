import os, sys, types, optparse
import wasanbon

class PluginFunction(object):
    def __init__(self):
        self.parser = optparse.OptionParser(usage="", add_help_option=False)
        self.parser.add_option('-v', '--verbose', help='Verbosity option (default=False)', default=False, action='store_true', dest='verbose_flag')
        self.parser.add_option('-a', '--alternative', help='print Alternatives of next argument (default=False)', default=False, action='store_true', dest='alt_flag')
        pass

    def depends(self):
        return []

    def parse_args(self, arg, print_alt_func=None):
        options, argv =  self.parser.parse_args(arg)
        if options.alt_flag:
            if print_alt_func == None:
                print ' '
                sys.exit(0)
                raise wasanbon.PrintAlternativeException()
            else:
                print_alt_func()
                sys.exit(0)
                raise wasanbon.PrintAlternativeException()

        return options, argv
    

class FunctionList():
    def __init__(self):
        pass

class Loader():
    
    ext = '_plugin'
    filename = 'plugin.yaml'

    def __init__(self, directories, verbose=False):
        self.mgr = FunctionList()
        self.admin = FunctionList()

        self._directories = directories
        self._plugin_list = {}
        for d in directories:
            self.list_plugins(d, verbose=verbose)

        for name, dir in self._plugin_list.items():
            self.load_plugin(name, dir, verbose=verbose)

        
    def list_plugins(self, directory, verbose=False):
        if 'admin' in os.listdir(directory):
            admin_dir = os.path.join(directory, 'admin')
            for d in os.listdir(admin_dir):
                if d.endswith(self.ext):
                    name = d[:-len(self.ext)]
                    if verbose: sys.stdout.write('# Plugin: %s Found.\n' % name)
                    self._plugin_list['admin.' + name] = os.path.join(admin_dir, d)

        if 'mgr' in os.listdir(directory):
            admin_dir = os.path.join(directory, 'mgr')
            for d in os.listdir(admin_dir):
                if d.endswith(self.ext):
                    name = d[:-len(self.ext)]
                    if verbose: sys.stdout.write('# Plugin: %s Found.\n' % name)
                    self._plugin_list['mgr.' + name] = os.path.join(admin_dir, d)



    
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

        pass


    def load_plugin(self, name, directory, verbose=False):
        if verbose: sys.stdout.write('# Loading (%s) in %s\n' % (name, directory))

        sys.path.append(os.path.dirname(directory))
        m = __import__(os.path.basename(directory))
        plugin = m.Plugin()

        #import yaml
        #dict_ = yaml.load(open(os.path.join(directory, 'plugin.yaml'), 'r'))
        #depends_plugin_names = dict_.get('depends', [])
        depends_plugin_names = plugin.depends()
        if type(depends_plugin_names) == types.StringType:
            depends_plugin_names = [depends_plugin_names]
        for n in depends_plugin_names:
            if verbose: sys.stdout.write('# Plugin (%s) depends on %s.\n' % (name, n))
            if not n in self._plugin_list.keys():
                sys.stdout.write('# Plugin %s is not found.\n' % n)
                return -1
            

            if n.startswith('admin.'):
                if getattr(self.admin, n[6:], None) != None:
                    # sys.stdout.write('# Plugin %s is already loaded.\n')
                    pass
                else:
                    if verbose: sys.stdout.write('# Plugin %s is not loaded yet.\n' % n)
                    self.load_plugin(n, self._plugin_list[n])

            elif n.startswith('mgr.'):
                if getattr(self.mgr, n[4:], None) != None:
                    #sys.stdout.write('# Plugin %s is already loaded.\n')
                    pass
                else:
                    if verbose: sys.stdout.write('# Plugin %s is not loaded yet.\n' % n)
                    self.load_plugin(n, self._plugin_list[n])
            pass

        if name.startswith('admin.'):
            setattr(self.admin, name[6:], m.Plugin())
        elif name.startswith('mgr.'):
            setattr(self.mgr, name[4:], m.Plugin())

        if verbose: sys.stdout.write('# Loaded (%s) \n' % name)
    
