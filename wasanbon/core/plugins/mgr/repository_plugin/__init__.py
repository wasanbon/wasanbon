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
        failed_flag = False
        match = False
        for rtc_name in argv[3:]:
            for repo in repos:
                if repo.name == argv[3]:
                    sys.stdout.write('# Cloning RTC (%s)\n' % rtc_name)
                    ret = admin.repository.clone_rtc(repo, verbose=verbose)
                    if ret < 0:
                        sys.stdout.write('## Failed. Return Code = %s\n' % ret)
                        failed_flag = True
                    else:
                        sys.stdout.write('## Success.\n')
                    match = True
        os.chdir(curdir)
        if not match: raise wasanbon.RepositoryNotFoundException()
        
        if failed_flag:
            return -1
        return 0


    @manifest
    def status(self, args):
        """ Show Repository Status of RTCs """
        self.parser.add_option('-l', '--long', help='Long Format (default=False)', default=False,
                               action='store_true', dest='long_flag')
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag
        long = options.long_flag

        if len(argv) == 2: argv = argv + ['all']
        
        package = admin.package.get_package_from_path(os.getcwd())
        rtcs = admin.rtc.get_rtcs_from_package(package, verbose=verbose)
        
        for rtc in rtcs:
            if argv[3] != 'all' and argv[3] != rtc.rtcprofile.basicInfo.name:
                continue

            repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)

            if long:
                output = admin.repository.get_status(repo)
                sys.stdout.write(output)
            else:
                sys.stdout.write('%s : \n' %  rtc.rtcprofile.basicInfo.name)

                if admin.repository.is_modified(repo, verbose=verbose):
                    sys.stdout.write('  Modified\n' )
                elif admin.repository.is_added(repo, verbose=verbose):
                    sys.stdout.write('  Added\n' )
                else:
                    sys.stdout.write('  Up-to-date\n')
        return 0


    @manifest
    def commit(self, args):
        """ Commit local changes to local repository.
        $ mgr.py repository commit [RTC_NAME] [COMMENT]"""
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        verbose = True
        package = admin.package.get_package_from_path(os.getcwd())
        wasanbon.arg_check(argv, 5)
        if argv[3] == 'all':
            rtcs = admin.rtc.get_rtcs_from_package(package, verbose=verbose)
        else:
            rtcs = [admin.rgc.get_rtc_from_package(package, argv[3], verbose=verbose)]
        #rtc_names = [argv[3]]
        return_value_map = {}
        failed_flag = False
        for rtc in rtcs:
            #rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
            sys.stdout.write('# Committing RTC (%s) \n' %  rtc.rtcprofile.basicInfo.name)
            repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
            comment = argv[4]
            if admin.repository.commit(repo, comment, verbose=verbose) == 0:
                sys.stdout.write('## Success\n')
                return_value_map[rtc.rtcprofile.basicInfo.name] = True
            else:
                sys.stdout.write('## Failed.\n')
                return_value_map[rtc.rtcprofile.basicInfo.name] = False
                failed_flag = True

        if verbose:
            for key, value in return_value_map.items():
                sys.stdout.write('# RTC (' + key + ') Commit : ' + ' '*(25-len(key)) + ('Success' if value else 'Failed') + '\n')
        if failed_flag: return -1
        return 0
        
    @manifest
    def push(self, args):
        """ Push Repository to server (default origin, master)
        $ mgr.py repository push [RTC_NAME]"""
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        verbose = True
        package = admin.package.get_package_from_path(os.getcwd())
        wasanbon.arg_check(argv, 4)
        if argv[3] == 'all':
            rtcs = admin.rtc.get_rtcs_from_package(package, verbose=verbose)
        else:
            rtcs = [admin.rtc.get_rtc_from_package(package, argv[3], verbose=verbose)]

        failed_flag = False
        return_value_map = {}
        for rtc in rtcs:
            #rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
            sys.stdout.write('# Pushing RTC (%s) \n' %  rtc.rtcprofile.basicInfo.name)
            repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
            if admin.repository.push(repo, verbose=verbose) == 0:
                sys.stdout.write('## Success\n')
                return_value_map[rtc.rtcprofile.basicInfo.name] = True
            else:
                sys.stdout.write('## Failed\n')
                return_value_map[rtc.rtcprofile.basicInfo.name] = False
                failed_flag = False
        if verbose:
            for key, value in return_value_map.items():
                sys.stdout.write('# RTC (' + key + ') Push : ' + ' '*(25-len(key)) + ('Success' if value else 'Failed') + '\n')
        if failed_flag: return -1
        return 0


    @manifest
    def pull(self, args):
        """ Pull Repository from server
        $ mgr.py repository pull [RTC_NAME]"""
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        verbose = True
        package = admin.package.get_package_from_path(os.getcwd())
        wasanbon.arg_check(argv, 4)
        if argv[3] == 'all':
            rtcs = admin.rtc.get_rtcs_from_package(package, verbose=verbose)
        else:
            names = argv[3:]
            rtcs = [admin.rtc.get_rtc_from_package(package, name, verbose=verbose) for name in names]
        
        failed_flag = False
        for rtc in rtcs:
            # rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
            sys.stdout.write('# Pulling RTC (%s) \n' %  rtc.rtcprofile.basicInfo.name)
            repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
            if admin.repository.pull(repo, verbose=verbose) == 0:
                sys.stdout.write('## Success\n')
            else:
                sys.stdout.write('## Failed\n')
                failed_flag = True

        return failed_flag

    @manifest
    def sync(self, args):
        """ Synchronize rtc/repository.yaml file and each rtc repository version hash. """
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        package = admin.package.get_package_from_path(os.getcwd())
        for rtc in admin.rtc.get_rtcs_from_package(package, verbose=verbose):
            repo = admin.repository.get_repository_from_path(rtc.path, description=rtc.rtcprofile.basicInfo.description)

        repo_file = os.path.join(package.get_rtcpath(), 'repository.yaml')

        bak_file = repo_file + wasanbon.timestampstr()
        if os.path.isfile(bak_file):
            os.remove(bak_file)
        import shutil, yaml
        shutil.copy(repo_file, bak_file)
        dic = yaml.load(open(bak_file, 'r'))
        if not dic:
            dic = {}
        dic[repo.name] = {'repo_name' : repo.name, 'git': repo.url, 'description':repo.description, 'hash':repo.hash}
        yaml.dump(dic, open(repo_file, 'w'), encoding='utf8', allow_unicode=True)
        pass

    @manifest
    def url(self, args):
        """ Get Repository URL of RTC.
        $ mgr.py repository url [RTC_NAME] """
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        verbose = True
        package = admin.package.get_package_from_path(os.getcwd())
        wasanbon.arg_check(argv, 4)
        rtc_name = argv[3]
        rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
        repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
        print repo.url.strip()
        return 0

    @manifest
    def name(self, args):
        """ Get Repository URL of RTC.
        $ mgr.py repository url [RTC_NAME] """
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        verbose = True
        package = admin.package.get_package_from_path(os.getcwd())
        wasanbon.arg_check(argv, 4)
        rtc_name = argv[3]
        rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
        repo = self.get_registered_repository_from_rtc(rtc,verbose=verbose)
        if repo is None:
            sys.stdout.write('# Repository Not Found.\n')
            return -1
        print repo.name
        return 0

    def get_registered_repository_from_rtc(self, rtc, verbose=False):
        """ Search Repository Object from RTC Information """
        target_repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
        repos = admin.binder.get_rtc_repos()
        result_repo = None
        for repo in repos:
            if repo.url.strip() == target_repo.url.strip():
                return repo

        return None
