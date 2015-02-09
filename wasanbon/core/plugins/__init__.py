
import os, sys, types

class Loader():
    
    ext = '_plugin'
    filename = 'plugin.yaml'

    def __init__(self, directory):
        self._directory = directory

        sys.path.append(os.path.join(directory))
        for d in os.listdir(directory):
            if d.endswith(self.ext):
                full_path = os.path.join(directory, d, self.filename)
                if os.path.isfile(full_path):
                    import yaml
                    dict_ = yaml.load(open(full_path, 'r'))
                    depends_plugins = dict_.get('depends', [])
                    if type(depends_plugins) != types.ListType:
                        depends_plugins = [depends_plugins]
                    for p in depends_plugins:
                        self.load_plugin(directory, p)

                    self.load_plugin(directory, d[:-len(self.ext)])

        pass

    def load_plugin(self, directory, name):
        sys.path.append(os.path.join(directory, name + self.ext))
        m = __import__(name + self.ext)
        setattr(self, name, m.Plugin())

    
    
