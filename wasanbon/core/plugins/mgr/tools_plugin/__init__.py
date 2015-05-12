import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.eclipse', 'admin.package']

    @manifest
    def rtcb(self, argv):
        """ Launch RTC Builder in this package.
        """
        #self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        #force   = options.force_flag
        
        package = admin.package.get_package_from_path(os.getcwd())        
        return admin.eclipse.launch_eclipse(workbench=package.get_rtcpath(), verbose=verbose)
