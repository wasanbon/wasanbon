import os, sys

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):
    """ This plugin provides wasanbon-admin.py make [package] command for building package and rtc outside/inside package """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.package', 'admin.rtc', 'admin.builder', 'admin.systeminstaller']

    @manifest
    def __call__(self, argv):
        """ Make Current Package """
        self.parser.add_option('-o', '--only', help='Build Only (Not Install) (default=False)', default=False, action='store_true', dest='only_flag')
        self.parser.add_option('-s', '--standalone', help='Installing RTC with standalone version (mostly YOUR_RTC_NAMEComp.exe', action='store_true', default=False, dest='standalone_flag')
        self.parser.add_option('-c', '--clean', help='Clean up binaries',  action='store_true', default=False, dest='clean_flag')
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag
        only = options.only_flag
        standalone = options.standalone_flag
        clean = options.clean_flag

        package = None
        if len(argv) >= 3:
            package = admin.package.get_package(argv[2], verbose=verbose)
            
        else:
            packages = admin.package.get_packages(verbose=verbose)        
            for package_ in packages:
                if isparent(package_.path, verbose=verbose):

                    package = package_
                    break
        if package == None:
            raise wasanbon.PackageNotFoundException()
        if verbose: sys.stdout.write('# Found Pcakage %s\n' % package.name)
        
        curdir = os.getcwd()
        rtcs = admin.rtc.get_rtcs_from_package(package)
        for rtc_ in rtcs:
            if isparent(rtc_.path):
                if verbose: sys.stdout.write('## Found RTC %s\n' % rtc_.rtcprofile.basicInfo.name)
                rtcs = [rtc_]
                break
        retval = 0
        for rtc in rtcs:
            
            if not clean:
                sys.stdout.write('# Making RTC %s\n' % rtc.rtcprofile.basicInfo.name)
                ret, msg = admin.builder.build_rtc(rtc.rtcprofile, verbose=verbose)
                if not ret:
                    retval = -1
                else:
                    if not only:
                        admin.systeminstaller.install_rtc_in_package(package, rtc, verbose=verbose, standalone=standalone)
                pass
            else: # clean
                sys.stdout.write('# Cleaning up RTC %s\n' % rtc.rtcprofile.basicInfo.name)
                ret, msg = admin.builder.clean_rtc(rtc.rtcprofile, verbose=verbose)
                if not ret:
                    retval = -1
                pass
        
        return retval

    def _print_alternatives(self):
        for p in admin.package.get_packages():
            print p.name


def isparent(path, verbose=False):
    def checkparent(p, q):
        #print 'check', p, q
        if q == '/':
            return False
        if verbose: sys.stdout.write('# Comparing %s == %s \n' % (p, q))
        if os.stat(p) == os.stat(q):
            return True
        parent= os.path.dirname(q)
        if q == parent:
            return False
        return checkparent(p, parent)
    return checkparent(path, os.getcwd())
