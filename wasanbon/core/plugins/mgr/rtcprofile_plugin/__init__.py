import os, sys

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.package', 'admin.rtc']

    @manifest
    def __call__(self, argv):
        print ' # this is plain function'
        pass

    def show(self, argv):
        """ This is print function
        """
        print " # This is example plugin's print function"

    def _print_rtcs(self, args):
        pack = admin.package.get_package_from_path(os.getcwd())
        rtcs = admin.rtc.get_rtcs_from_package(pack)
        for r in rtcs:
            print r.rtcprofile.basicInfo.name

    @manifest
    def dump(self, argv):
        """ This is help text
        """
        options, argv = self.parse_args(argv[:], self._print_rtcs)
        verbose = options.verbose_flag # This is default option

        wasanbon.arg_check(argv, 4)
        
        pack = admin.package.get_package_from_path(os.getcwd())
        rtc = admin.rtc.get_rtc_from_package(pack, argv[3])

        path = rtc.get_rtc_profile_path()
        with open(path, 'r') as f:
            sys.stdout.write(f.read())

        return 0

        
