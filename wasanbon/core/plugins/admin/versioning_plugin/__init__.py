import wasanbon
from wasanbon.core.plugins import PluginFunction

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.git']

    def __call__(self, argv):
        print '# Versioning Plugin : version = 1.0.0'

    @property
    def versioning(self):
        import versioning
        return versioning
