import os
import sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest


class Plugin(PluginFunction):
    """ RTC development tool management Plugin. """

    def __init__(self):
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.eclipse', 'admin.package']

    @manifest
    def rtcb(self, argv):
        """ Launch RTC Builder in this package.
        $ ./mgr.py tools rtcb
        """
        options, _ = self.parse_args(argv[:])
        verbose = options.verbose_flag  # This is default option

        package = admin.package.get_package_from_path(os.getcwd())
        return admin.eclipse.launch_eclipse(workbench=package.get_rtcpath(), verbose=verbose)
