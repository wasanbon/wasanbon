import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.binder', 'admin.repository', 'admin.package', 'admin.rtc']

    @manifest
    def list(self, argv):
        """ List RTC Repository
        $ mgr.py repository list """
        #options, argv = self.parse_args(args[:])
        #verbose = options.verbose_flag
        
        admin.binder.rtcs(argv)

        pass

    def _print_alternative_rtcs(self, args=None):
        for r in admin.binder.get_rtc_repos():
            print r.name

    @manifest
    def clone(self, args):
        """ Clone RTC.
        $ mgr.py repository clone [repo_name] """

        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        wasanbon.arg_check(argv, 4)
        pack = admin.package.get_package_from_path(os.getcwd())        
        repos = admin.binder.get_rtc_repos()

        curdir = os.getcwd()
        os.chdir(pack.get_rtcpath())
        match = False
        for rtc_name in argv[3:]:
            for repo in repos:
                if repo.name == argv[3]:
                    sys.stdout.write('# Cloning RTC (%s)\n' % rtc_name)
                    admin.repository.clone_rtc(repo, verbose=verbose)
                    match = True
        os.chdir(curdir)
        if not match: raise wasanbon.RepositoryNotFoundException()
        
        return 0


    @manifest
    def status(self, args):
        """ Show Repository Status of RTCs """
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        if len(argv) == 2: argv = argv + ['all']
        
        package = admin.package.get_package_from_path(os.getcwd())
        rtcs = admin.rtc.get_rtcs_from_package(package, verbose=verbose)
        
        for rtc in rtcs:
            sys.stdout.write('%s : \n' %  rtc.rtcprofile.basicInfo.name)
            repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
            print repo
        

        pass
