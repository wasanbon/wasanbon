import os
import sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest


class Plugin(PluginFunction):
    """ Repository management Plugin. """

    def __init__(self):
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment',
                'admin.binder',
                'admin.repository',
                'admin.package',
                'admin.git',
                'admin.github',
                'admin.rtc']

    @manifest
    def list(self, argv):
        """ List RTC Repository
        $ ./mgr.py repository list """
        admin.binder.rtcs(argv)

    def _print_alternative_rtcs(self, args=None):
        rtc_command = ['git_init', 'pull', 'push', 'remote_create', 'commit']

        if args[2] in rtc_command:
            pack = admin.package.get_package_from_path(os.getcwd())
            rtcs = admin.rtc.get_rtcs_from_package(pack)
            for r in rtcs:
                print(r.rtcprofile.basicInfo.name)
            return
        else:
            for r in admin.binder.get_rtc_repos():
                print(r.name)

    @manifest
    def clone(self, args):
        """ Clone RTC to package.
        $ ./mgr.py repository clone <REPO_NAME>
        """
        self.parser.add_option('-u', '--url', help='Directory point the url of repository  (default="None")',
                               default="None", type="string", dest="url")
        self.parser.add_option('-t', '--type', help='Set the type of repository  (default="git")', default="git", type="string", dest="type")
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag
        url = options.url
        typ = options.type

        if url == "None":
            wasanbon.arg_check(argv, 4)
        pack = admin.package.get_package_from_path(os.getcwd())
        repos = admin.binder.get_rtc_repos()
        curdir = os.getcwd()
        os.chdir(pack.get_rtcpath())
        match = False
        failed_flag = False
        if url == "None":
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
                            pass
                        match = True
                        break
        else:
            match = True
            rtc_name = os.path.basename(url).split(".")[0]
            repo = admin.binder.Repository(rtc_name, type=typ, platform=wasanbon.platform, url=url, description="")

            sys.stdout.write('# Cloning RTC (%s)\n' % rtc_name)
            ret = admin.repository.clone_rtc(repo, verbose=verbose)
            if ret < 0:
                sys.stdout.write('## Failed. Return Code = %s\n' % ret)
                failed_flag = True
            else:
                sys.stdout.write('## Success.\n')
                pass
            match = True

        os.chdir(curdir)
        if not match:
            raise wasanbon.RepositoryNotFoundException()

        if failed_flag:
            return -1
        return 0

    @manifest
    def fix_gitignore(self, args):
        """ Fix .gitignore files in RTC directories.
        $ ./mgr.py repository fix_gitignore
        """
        self.parser.add_option('-l', '--long', help='Long Format (default=False)', default=False,
                               action='store_true', dest='long_flag')
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag
        long = options.long_flag

        if len(argv) == 3:
            argv = argv + ['all']

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
                sys.stdout.write('%s : \n' % rtc.rtcprofile.basicInfo.name)

                if not admin.repository.check_dot_gitignore(repo, verbose=verbose):
                    admin.repository.add(repo, [os.path.join(repo.path, '.gitignore')], verbose=verbose)

        return 0

    @manifest
    def status(self, args):
        """ Show Repository Status of RTCs.
        $ ./mgr.py repository status
        """
        self.parser.add_option('-l', '--long', help='Long Format (default=False)', default=False,
                               action='store_true', dest='long_flag')
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag
        long = options.long_flag

        if len(argv) == 3:
            argv = argv + ['all']

        package = admin.package.get_package_from_path(os.getcwd())
        rtcs = admin.rtc.get_rtcs_from_package(package, verbose=verbose)

        for rtc in rtcs:
            if argv[3] != 'all' and argv[3] != rtc.rtcprofile.basicInfo.name:
                continue

            repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
            if repo is None:
                sys.stdout.write('%s does not have local repository.\n' % rtc.rtcprofile.basicInfo.name)
                continue

            if long:
                output = admin.repository.get_status(repo)
                sys.stdout.write(output)
            else:
                sys.stdout.write('%s : \n' % rtc.rtcprofile.basicInfo.name)

                if not admin.repository.check_dot_gitignore(repo, verbose=False):
                    sys.stdout.write('## Warning! .gitignore seems to have some problems.\n')

                if admin.repository.is_modified(repo, verbose=verbose):
                    sys.stdout.write('  Modified\n')
                elif admin.repository.is_untracked(repo, verbose=False):
                    sys.stdout.write('  Untracked\n')
                elif admin.repository.is_added(repo, verbose=False):
                    sys.stdout.write('  Added\n')
                else:
                    sys.stdout.write('  Up-to-date\n')
        return 0

    @manifest
    def commit(self, args):
        """ Commit local changes to local repository.
        $ ./mgr.py repository commit <RTC_NAME> <COMMENT>
        """
        self.parser.add_option('-p', '--push', help='Commit with push  (default="False")', default=False, action="store_true", dest="push_flag")
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag
        push = options.push_flag
        verbose = True
        package = admin.package.get_package_from_path(os.getcwd())
        wasanbon.arg_check(argv, 5)
        if argv[3] == 'all':
            rtcs = admin.rtc.get_rtcs_from_package(package, verbose=verbose)
        else:
            rtcs = [admin.rtc.get_rtc_from_package(package, argv[3], verbose=verbose)]
        return_value_map = {}
        failed_flag = False
        for rtc in rtcs:
            sys.stdout.write('# Committing RTC (%s) \n' % rtc.rtcprofile.basicInfo.name)
            repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
            comment = argv[4]
            if admin.repository.commit(repo, comment, verbose=verbose) == 0:
                sys.stdout.write('## Success\n')
                if push:
                    p_branch = admin.git.git_command(['rev-parse', '--abbrev-ref', 'HEAD'], path=repo._path)
                    output, stderr = p_branch.communicate()
                    branch = output.decode(encoding="utf-8").strip()

                    sys.stdout.write('# Pushing RTC (%s) \n' % rtc.rtcprofile.basicInfo.name)
                    sys.stdout.write('Set Username:"your_username" and Password:"your_token"\n')
                    sys.stdout.flush()
                    if admin.repository.push(repo, verbose=verbose, branch=branch) == 0:
                        sys.stdout.write('## Success\n')
                        return_value_map[rtc.rtcprofile.basicInfo.name] = True
                    else:
                        sys.stdout.write('## Failed.\n')
                        return_value_map[rtc.rtcprofile.basicInfo.name] = False
                else:
                    return_value_map[rtc.rtcprofile.basicInfo.name] = True
            else:
                sys.stdout.write('## Failed.\n')
                return_value_map[rtc.rtcprofile.basicInfo.name] = False
                failed_flag = True

        if verbose:
            for key, value in list(return_value_map.items()):
                sys.stdout.write('# RTC (' + key + ') Commit : ' + ' ' * (25 - len(key)) + ('Success' if value else 'Failed') + '\n')
        if failed_flag:
            return -1
        return 0

    @manifest
    def push(self, args):
        """ Push Repository to server (default origin, master)
        $ ./mgr.py repository push <RTC_NAME>
        """
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
            repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)

            p_branch = admin.git.git_command(['rev-parse', '--abbrev-ref', 'HEAD'], path=repo._path)
            output, stderr = p_branch.communicate()
            branch = output.decode(encoding="utf-8").strip()

            sys.stdout.write('# Pushing RTC (%s) \n' % rtc.rtcprofile.basicInfo.name)
            sys.stdout.write('Set Username:"your_username" and Password:"your_token"\n')
            sys.stdout.flush()
            if admin.repository.push(repo, verbose=verbose, branch=branch) == 0:
                sys.stdout.write('## Success\n')
                return_value_map[rtc.rtcprofile.basicInfo.name] = True
            else:
                sys.stdout.write('## Failed\n')
                return_value_map[rtc.rtcprofile.basicInfo.name] = False
                failed_flag = False
        if verbose:
            for key, value in list(return_value_map.items()):
                sys.stdout.write('# RTC (' + key + ') Push : ' + ' ' * (25 - len(key)) + ('Success' if value else 'Failed') + '\n')
        if failed_flag:
            return -1
        return 0

    @manifest
    def pull(self, args):
        """ Pull Repository from server
        $ ./mgr.py repository pull <RTC_NAME>
        """
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
            sys.stdout.write('# Pulling RTC (%s) \n' % rtc.rtcprofile.basicInfo.name)
            repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
            if admin.repository.pull(repo, verbose=verbose) == 0:
                sys.stdout.write('## Success\n')
            else:
                sys.stdout.write('## Failed\n')
                failed_flag = True

        if failed_flag:
            return -1
        return 0

    @manifest
    def sync(self, args):
        """ Synchronize rtc/repository.yaml file and each rtc repository version hash.
        $ ./mgr.py repository sync
        """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        sys.stdout.write('# Writing repository.yaml for package distribution\n')

        sys.stdout.write('## Parsing RTC directory\n')
        package = admin.package.get_package_from_path(os.getcwd())
        repos = []
        for rtc in admin.rtc.get_rtcs_from_package(package, verbose=verbose):
            sys.stdout.write('### RTC %s\n' % rtc.rtcprofile.basicInfo.name)
            repo = admin.repository.get_repository_from_path(rtc.path, description=rtc.rtcprofile.basicInfo.description)

            repos.append(repo)

        repo_file = os.path.join(package.get_rtcpath(), 'repository.yaml')

        bak_file = repo_file + wasanbon.timestampstr()
        if os.path.isfile(bak_file):
            os.remove(bak_file)
        import shutil
        import yaml
        shutil.copy(repo_file, bak_file)
        dic = yaml.safe_load(open(bak_file, 'r'))
        if not dic:
            dic = {}
        for repo in repos:
            if getattr(repo, 'url') != None:
                url = repo.url.strip().decode('utf-8')
            else:
                url = ''
            hash = repo.hash.decode('utf-8')
            dic[repo.name] = {'repo_name': repo.name, 'git': url, 'description': repo.description, 'hash': hash}

        yaml.dump(dic, open(repo_file, 'w'), encoding='utf8', allow_unicode=True, default_flow_style=False)
        return 0

    @manifest
    def url(self, args):
        """ Get Repository URL of RTC.
        $ ./mgr.py repository url <RTC_NAME>
        """
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        verbose = True
        wasanbon.arg_check(argv, 4)
        rtc_name = argv[3]
        repo = admin.binder.get_rtc_repo(rtc_name, verbose=verbose)
        if repo is None:
            sys.stdout.write('# Repository Not Found.\n')
            return -1
        print(repo.url.strip())
        return 0

    @manifest
    def name(self, args):
        """ Get Repository URL of RTC.
        $ ./mgr.py repository name <RTC_NAME>
        """
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag

        verbose = True
        wasanbon.arg_check(argv, 4)
        rtc_name = argv[3]
        repo = admin.binder.get_rtc_repo(rtc_name, verbose=verbose)
        if repo is None:
            sys.stdout.write('# Repository Not Found.\n')
            return -1
        print(repo.name)
        return 0

    @manifest
    def git_init(self, args):
        """ Initialize git repository in RTC directory.
        $ ./mgr.py repository git_init <RTC_NAME>
        """
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
            sys.stdout.write('# Initializing git local repository on RTC (%s) \n' % rtc.rtcprofile.basicInfo.name)
            repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
            if not repo is None:
                failed_flag = True
                sys.stdout.write('## RTC already has local repository.\n')
                continue

            sys.stdout.write('## Creating git repository in %s\n' % rtc.path)
            repo = admin.repository.init_git_repository_to_path(rtc.path, verbose=verbose)
            sys.stdout.write('## Adding Files to repository\n')
            admin.repository.add_files(repo, verbose=verbose, exclude_pattern='^\.|.*\.pyc$|.*~$|.*\.log$|build-.*')
            comment = 'First comment.'
            sys.stdout.write('## Commiting ...\n')
            if admin.repository.commit(repo, comment, verbose=verbose) != 0:
                sys.stdout.write('## First Commit failed.')
            sys.stdout.write('## Success\n')

        if failed_flag:
            sys.stdout.write('## Failed.\n')
            return -1
        sys.stdout.write('### Success.\n')
        return 0

    def get_registered_repository_from_rtc(self, rtc, verbose=False):
        """ Search Repository Object from RTC Information """
        target_repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
        if target_repo is None:
            return None
        target_url = target_repo.url.strip().decode('utf-8')
        repos = admin.binder.get_rtc_repos()
        result_repo = None
        for repo in repos:
            if getattr(repo, 'url') != None:
                if repo.url.strip() == target_url:
                    return repo

        return None

    @manifest
    def get_rtcprofile(self, args):
        """ Get RTCProfile from Repository
        $ ./mgr.py repository get_rtcprofile <RTC_NAME>
        """
        self.parser.add_option('-r', '--repositoryuri', help='Directory point the url of repository  (default="None")',
                               default="None", type="string", dest="url")
        self.parser.add_option('-u', '--username', help='Username of github', default=None, dest='username', action='store', type='string')
        self.parser.add_option('-p', '--password', help='Password of github', default=None, dest='password', action='store', type='string')
        self.parser.add_option('-k', '--token', help='Token of github', default=None, dest='token', action='store', type='string')
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag
        url = options.url

        username, password, token = wasanbon.user_pass(options.username, passwd=options.password, token=options.token)
        github = admin.github.Github(user=username, passwd=password, token=token)

        if url == "None":
            wasanbon.arg_check(argv, 4)
        pack = admin.package.get_package_from_path(os.getcwd())
        repos = admin.binder.get_rtc_repos()
        curdir = os.getcwd()
        os.chdir(pack.get_rtcpath())
        match = False

        if url == "None":
            for rtc_name in argv[3:]:
                for repo in repos:
                    if repo.name == argv[3]:
                        sys.stdout.write('# Accessing Remote repository named %s\n' % repo.name)
                        url = repo.url
                        match = True
        else:
            match = True

        failed_flag = True
        if match:
            urlarr = url.split('/')
            service = ""
            if "github" in urlarr[2]:
                service = "github"
            else:
                service = urlarr[2]
            owner = urlarr[3]
            repo_name = urlarr[4].split(".")[0]

            if verbose:
                sys.stdout.write('## Repository Service is %s\n' % service)

            if service != 'github':
                sys.stdout.write('## Error Service (%s) is not available\n' % service)

            if not os.path.exists(repo_name):
                os.mkdir(repo_name)
            os.chdir(repo_name)

            sys.stdout.write('# Collectiong RTC.xml (%s)\n' % repo_name)

            github = admin.github.Github(user=username, passwd=password, token=token)
            ret = github.get_file_contents(owner, repo_name, 'RTC.xml', verbose=verbose)
            if ret < 0:
                sys.stdout.write('## Failed. Return Code = %s\n' % ret)
            else:
                sys.stdout.write('## Success.\n')
                failed_flag = False

        os.chdir(curdir)
        if not match:
            raise wasanbon.RepositoryNotFoundException()

        if failed_flag:
            return -1
        return 0

    @manifest
    def remote_create(self, args):
        """ Create local repository.
        $ ./mgr.py repository remote_create <RTC_NAME>
        """
        self.parser.add_option('-u', '--username', help='Username of github', default=None, dest='username', action='store', type='string')
        self.parser.add_option('-p', '--password', help='Password of github', default=None, dest='password', action='store', type='string')
        self.parser.add_option('-t', '--token', help='Token of github', default=None, dest='token', action='store', type='string')
        options, argv = self.parse_args(args[:], self._print_alternative_rtcs)
        verbose = options.verbose_flag
        p = admin.package.get_package_from_path(os.getcwd())

        wasanbon.arg_check(argv, 4)
        rtc = admin.rtc.get_rtc_from_package(p, argv[3])
        try:
            repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
            if repo is None:
                sys.stdout.write('# Repository is not found.\n')
                return -1
        except wasanbon.RepositoryNotFoundException as e:
            sys.stdout.write('# Repository is not found.\n')
            return -1

        username, password, token = wasanbon.user_pass(options.username, passwd=options.password, token=options.token)
        rtcp = rtc.rtcprofile
        github = admin.github.Github(user=username, passwd=password, token=token)
        sys.stdout.write('# Creating Remote repository named %s\n' % rtcp.basicInfo.name)
        if github.exists_repo(rtcp.basicInfo.name):
            sys.stdout.write('## Error. Repository %s already exists.\n' % rtcp.basicInfo.name)
            return -1

        github_repo = github.create_repo(rtcp.basicInfo.name)
        _url = 'https://github.com/' + username + '/' + rtcp.basicInfo.name + '.git'
        sys.stdout.write('## Set Username:"your_username" and Password:"your_token"\n')
        sys.stdout.flush()
        admin.git.git_command(['remote', 'add', 'origin', _url], path=rtc.path, verbose=verbose)

        if admin.repository.push(repo, verbose=verbose) != 0:
            sys.stdout.write('## Failed.\n')
            return -1
        sys.stdout.write('## Success.\n')
        return 0
