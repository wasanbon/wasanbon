import os
import wasanbon
from wasanbon.core.plugins import PluginFunction

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    def __call__(self, args):
        print 'admin.git plugin:  version=1.0.0'

    @property
    def git(self):
        import git
        return git
