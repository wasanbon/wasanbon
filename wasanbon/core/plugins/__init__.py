
import os, sys, types


class Function():
    def __init__(self):
        pass

class Loader():
    
    ext = '_plugin'
    filename = 'plugin.yaml'

    def __init__(self, directory):
        self.package = Function()
        self.admin = Function()

        self._directory = directory

        sys.path.append(os.path.join(directory))
        for d in os.listdir(directory):
            if d.endswith(self.ext):
                dict_ = self.load_package_yaml(os.path.join(directory, d))
                depends_plugins = dict_.get('depends', [])
                if type(depends_plugins) != types.ListType:
                    depends_plugins = [depends_plugins]
                for p in depends_plugins:
                    self.load_plugin(directory, p)

                self.load_plugin(directory, d[:-len(self.ext)])

        pass

    def load_package_yaml(self, directory):
        full_path = os.path.join(directory, self.filename)
        if not os.path.isfile(full_path):
            return {}
        import yaml
        return yaml.load(open(full_path, 'r'))

        

    def load_plugin(self, directory, name, dict_=None):
        if dict_ == None:
            dict_ = self.load_package_yaml(os.path.join(directory, name + self.ext))
        sys.path.append(os.path.join(directory, name + self.ext))
        function = dict_.get('function', 'package')
        m = __import__(name + self.ext)
        function = dict_['function']
        if function == 'admin':
            setattr(self.admin, name, m.Plugin())
        elif function == 'package':
            setattr(self.package, name, m.Plugin())

    
    
