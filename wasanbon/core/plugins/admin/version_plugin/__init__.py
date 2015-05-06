import sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):
    """ Show version of wasanbon """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return []

    @manifest
    def __call__(self, argv):
        """ Manifesting __call__ function is available but not recommended """
        sys.stdout.write('platform version: %s\n' % wasanbon.platform())
        sys.stdout.write('wasanbon version: %s\n' % wasanbon.get_version())
        pass


