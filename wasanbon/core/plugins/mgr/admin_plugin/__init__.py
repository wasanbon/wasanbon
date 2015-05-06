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
                'admin.package']

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
        if admin.repository.is_updated(repo, verbose=verbose):
            sys.stdout.write('  Modified\n')
        else:
            sys.stdout.write('  Up-to-date\n')

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
    def commit(self, args):
        """ Commit changes to local Package repository
        """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        p = admin.package.get_package_from_path(os.getcwd())        
        sys.stdout.write('# Committing package %s to local repository\n' % p.name)
        repo = admin.repository.get_repository_from_path(os.getcwd(), verbose=verbose)
        wasanbon.arg_check(argv,4)
        comment = argv[3]
        if repo is None:
            raise wasanbon.RepositoryNotFoundException()
        if admin.repository.commit(repo, comment, verbose=verbose) == 0:
            sys.stdout.write('## Success.\n')
            return 0
        sys.stdout.write('## Failed.\n')
        return -1


    @manifest
    def push(self, args):
        """ Commit changes to local Package repository
        """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        
        sys.stdout.write('# Pushing Package %s\n' % os.path.basename(os.getcwd()))
        repo = admin.repository.get_repository_from_path(os.getcwd(), verbose=verbose)
        if admin.repository.push(repo, verbose=verbose) != 0:
            sys.stdout.write('## Failed.\n')
            return -1
        sys.stdout.write('## Success.\n')
        return 0
