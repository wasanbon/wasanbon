import wasanbon
from wasanbon.core.plugins import PluginFunction

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    def __call__(self, argv):
        print '# rtcconf plugin version 1.0.0'

        
    @property
    def rtcconf(self):
        import rtcconf
        return rtcconf
