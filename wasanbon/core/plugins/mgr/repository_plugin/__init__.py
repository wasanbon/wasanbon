import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment',
                'admin.binder', 
                'admin.repository', 
                'admin.package', 
                'admin.rtc']

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
            if admin.repository.is_updated(repo, verbose=verbose):
                sys.stdout.write('  Modified\n' )
            else:
                sys.stdout.write('  Up-to-date\n')
        return 0


    @manifest
    def commit(self, args):
        """ Show Repository Status of RTCs
        $ mgr.py repository commit [RTC_NAME] [COMMENT]"""
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        verbose = True
        package = admin.package.get_package_from_path(os.getcwd())
        wasanbon.arg_check(argv, 5)
        rtc_name = argv[3]
        rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
        sys.stdout.write('# Committing RTC (%s) \n' %  rtc.rtcprofile.basicInfo.name)
        repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
        comment = argv[4]
        if admin.repository.commit(repo, comment, verbose=verbose) == 0:
            sys.stdout.write('## Success\n')
            return 0
        sys.stdout.write('## Failed.\n')
        return -1
        
    @manifest
    def push(self, args):
        """ Push Repository to server
        $ mgr.py repository push [RTC_NAME]"""
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        verbose = True
        package = admin.package.get_package_from_path(os.getcwd())
        wasanbon.arg_check(argv, 4)
        rtc_name = argv[3]
        rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
        sys.stdout.write('# Pushing RTC (%s) \n' %  rtc.rtcprofile.basicInfo.name)
        repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
        if admin.repository.push(repo, verbose=verbose) == 0:
            sys.stdout.write('## Success\n')
            return 0

        sys.stdout.write('## Failed\n')
        return -1


    @manifest
    def pull(self, args):
        """ Pull Repository from server
        $ mgr.py repository pull [RTC_NAME]"""
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        verbose = True
        package = admin.package.get_package_from_path(os.getcwd())
        wasanbon.arg_check(argv, 4)
        rtc_name = argv[3]
        rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
        sys.stdout.write('# Pulling RTC (%s) \n' %  rtc.rtcprofile.basicInfo.name)
        repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
        if admin.repository.pull(repo, verbose=verbose) == 0:
            sys.stdout.write('## Success\n')
            return 0

        sys.stdout.write('## Failed\n')
        return -1

        

