import sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest


class Plugin(PluginFunction):
    """ Show version of wasanbon. """

    def __init__(self):
        super().__init__()
        pass

    @manifest
    def __call__(self, argv):
        """ Manifesting __call__ function is available but not recommended """
        sys.stdout.write('platform version: %s\n' % wasanbon.platform())
        sys.stdout.write('wasanbon version: %s\n' % wasanbon.get_version())
        pass
