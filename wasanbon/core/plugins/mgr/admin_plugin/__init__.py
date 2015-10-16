import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 
                'admin.repository',
                'admin.rtc',
                'admin.package',
                'admin.github',
                'admin.git']

    def __call__(self, argv):
        print ' # this is plain function'
        pass

    @manifest
    def setting(self, args):
        """ Show setting of Package """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag

        print '# Setting of this package'
        p = admin.package.get_package_from_path(os.getcwd())
        print 'Name : %s' % (p.name)
        print 'Path :'
        print '  /      : %s' % p.path
        print '  rtc    : %s' % p.get_rtcpath(fullpath=False)
        print '  bin    : %s' % p.get_binpath(fullpath=False)
        print '  conf   : %s' % p.get_confpath(fullpath=False)
        print '  system : %s' % p.get_systempath(fullpath=False)
        
        return 0
        
    @manifest
    def status(self, args):
        """ Show status of package local repository
        """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        p = admin.package.get_package_from_path(os.getcwd())        
        sys.stdout.write('%s :\n' % p.name)
        repo = admin.repository.get_repository_from_path(os.getcwd(), verbose=verbose)
        if repo is None:
            raise wasanbon.RepositoryNotFoundException()
        if admin.repository.is_modified(repo, verbose=verbose):
            sys.stdout.write('  Modified\n')
        elif admin.repository.is_untracked(repo, verbose=verbose):
            sys.stdout.write('  Untracked files found\n')
        elif admin.repository.is_added(repo, verbose=False):
            sys.stdout.write('  Added\n' )

        else:
            sys.stdout.write('  Up-to-date\n')

        return 0

    @manifest
    def fix_gitignore(self, args):
        """ Fix .gitignore file in Package directories. """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        
        package = admin.package.get_package_from_path(os.getcwd())
        repo = admin.repository.get_repository_from_path(package.path, verbose=verbose)
        if not admin.repository.check_dot_gitignore(repo, verbose=verbose):
            admin.repository.add(repo, [os.path.join(repo.path, '.gitignore')], verbose=verbose)
        return 0

    @manifest
    def remote_create(self, args):
        """ Create local repository
        """
        self.parser.add_option('-u', '--username', help='Username of github', default=None, dest='username', action='store', type='string')
        self.parser.add_option('-p', '--password', help='Password of github', default=None, dest='password', action='store', type='string')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        p = admin.package.get_package_from_path(os.getcwd())        

        try:
            repo = admin.repository.get_repository_from_path(os.getcwd(), verbose=verbose)
            if repo is None:
                sys.stdout.write('# Repository is not found.\n')
                return -1
        except wasanbon.RepositoryNotFoundException, e:
            sys.stdout.write('# Repository is not found.\n')
            return -1

        username, password = wasanbon.user_pass(options.username, passwd=options.password)

        github = admin.github.Github(user=username, passwd=password)
        sys.stdout.write('# Creating Remote repository named %s\n' % p.name)
        if github.exists_repo(p.name):
            sys.stdout.write('## Error. Repository %s already exists.\n' % p.name)
            return -1

        github_repo = github.create_repo(p.name)
        _url = 'https://github.com/' + username + '/' + p.name + '.git'
        admin.git.git_command(['remote', 'add', 'origin', _url], verbose=verbose)

        if admin.repository.push(repo, verbose=verbose) != 0:
            sys.stdout.write('## Failed.\n')
            return -1
        sys.stdout.write('## Success.\n')
        return 0

    @manifest
    def sync(self, args):
        """ Sync RTC local repository to local package repository record """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag

        package = admin.package.get_package_from_path(os.getcwd())        
        file = package.rtc_repository_file
        import yaml
        repo_dict = yaml.load(open(file, 'r'))
        repos = admin.repository.get_rtc_repositories_from_package(package, verbose=verbose)
        for repo in repos:
            rtc = admin.rtc.get_rtc_from_package(package, repo.name)
            hashcode = admin.repository.get_repository_hash(repo)
            repo_dict[repo.name]['description'] = rtc.rtcprofile.basicInfo.description
            repo_dict[repo.name]['type'] = repo.type
            repo_dict[repo.name]['url'] = repo.url
            repo_dict[repo.name]['hash'] = hashcode
            if repo.type in repo_dict[repo.name].keys():
                del(repo_dict[repo.name][repo.type])
            
        os.rename(file, file+wasanbon.timestampstr())
        yaml.dump(repo_dict, open(file, 'w'), encoding='utf8', allow_unicode=True, default_flow_style=False)
        return 0

    @manifest
    def git_init(self, args):
        """ Create local repository
        """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        p = admin.package.get_package_from_path(os.getcwd())        
        sys.stdout.write('# Initializing git repository of package %s\n' % p.name)
        try:
            repo = admin.repository.get_repository_from_path(os.getcwd(), verbose=verbose)
            if not repo is None:
                sys.stdout.write('# Repository exists already.\n')
                return -1
        except wasanbon.RepositoryNotFoundException, e:
            pass
        sys.stdout.write('## OK. No repository found.\n')

        sys.stdout.write('## Creating git repository in %s\n' % os.getcwd())
        repo = admin.repository.init_git_repository_to_path(os.getcwd(), verbose=verbose)
        sys.stdout.write('## Adding Files to repository\n') 
        admin.repository.add_files(repo, verbose=verbose, exclude_path=[p.get_binpath()])
        if not admin.repository.check_dot_gitignore(repo, verbose=verbose):
            admin.repository.add(repo, [os.path.join(repo.path, '.gitignore')], verbose=verbose)
        comment = 'First Commit'
        if admin.repository.commit(repo, comment, verbose=verbose) != 0:
            sys.stdout.write('## First Commit failed.\n')
            return -1
        sys.stdout.write('## Success\n')
        return 0
        

        if repo is None:
            sys.stdout.write('# Error. Failed to create git repository to %s\n' % os.getcwd())
            return -2

        
        
        return 0

    @manifest
    def commit(self, args):
        """ Commit changes to local Package repository
        """
        self.parser.add_option('-p', '--push', help='Push simultaneously', default=False, dest='push_flag', action='store_true')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        push = options.push_flag

        p = admin.package.get_package_from_path(os.getcwd())        
        sys.stdout.write('# Committing package %s to local repository\n' % p.name)
        repo = admin.repository.get_repository_from_path(os.getcwd(), verbose=verbose)
        wasanbon.arg_check(argv,4)
        comment = argv[3]
        if repo is None:
            raise wasanbon.RepositoryNotFoundException()
        if admin.repository.commit(repo, comment, verbose=verbose) == 0:
            sys.stdout.write('## Success.\n')

            if push:
                sys.stdout.write('# Pushing Package %s\n' % os.path.basename(os.getcwd()))
                repo = admin.repository.get_repository_from_path(os.getcwd(), verbose=verbose)
                if admin.repository.push(repo, verbose=verbose) != 0:
                    sys.stdout.write('## Failed.\n')
                    return -1
                sys.stdout.write('## Success.\n')

            return 0
        sys.stdout.write('## Failed.\n')
        return -1


    @manifest
    def push(self, args):
        """ Commit changes to local Package repository
        """
        self.parser.add_option('-u', '--username', help='Username of github', default=None, dest='username', action='store', type='string')
        self.parser.add_option('-p', '--password', help='Password of github', default=None, dest='password', action='store', type='string')

        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        
        sys.stdout.write('# Pushing Package %s\n' % os.path.basename(os.getcwd()))
        repo = admin.repository.get_repository_from_path(os.getcwd(), verbose=verbose)
        if admin.repository.push(repo, verbose=verbose) != 0:
            sys.stdout.write('## Failed.\n')
            return -1
        sys.stdout.write('## Success.\n')
        return 0
