import os, sys, traceback
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        #import repository
        #repository.plugin_obj = self
        pass

    def depends(self):
        return ['admin.environment', 'admin.package', 'admin.git', 'admin.binder']

    def _list_package_repos(self):
        for r in admin.binder.get_package_repos():
            print r.name
    
    #@property
    #def repository(self):
    #    import repository
    #    return repository

    @manifest
    def list(self, args):
        admin.binder.packages(args)
        
    @manifest
    def clone(self, args):
        #self.parser.add_option('-r', '--remove', help='Remove All Files (default=False)', default=False, action='store_true', dest='remove_flag')
        options, argv = self.parse_args(args[:], self._list_package_repos)
        verbose = options.verbose_flag
        #remove = options.remove_flag

        wasanbon.arg_check(argv, 4)
        repo_name = argv[3]
        package_repo = admin.binder.get_package_repo(repo_name)

        #import repository
        self.clone_package(package_repo, path=package_repo.basename, verbose=verbose)
        return 0
        
    def clone_package(self, package_repo, path=None, verbose=False):
        if verbose: sys.stdout.write('# Cloning package %s\n' % package_repo)

        if path is None:  path = package_repo.basename
        url = package_repo.url

        import wasanbon
        try:
            p = admin.package.get_package(path, verbose=verbose)
            raise wasanbon.PackageAlreadyExistsException()
        except:
            pass
        
        admin.git.git_command(['clone', url, path], verbose=verbose)
    
        admin.package.create_package(path, verbose=verbose, force_create=True, overwrite=False)
        pack = admin.package.get_package(path, verbose=verbose)
        admin.package.validate_package(pack, verbose=verbose, autofix=True, ext_only=True)

        current_dir = os.getcwd()
        try:
            os.chdir(pack.get_rtcpath())

            repos = self.get_rtc_repositories_from_package(pack, verbose=verbose)
            for repo in repos:
                self.clone_rtc(repo, verbose=verbose)
                pass
        except Exception, ex:
            traceback.print_exc()
            raise ex
        finally:
            os.chdir(current_dir)
            pass

    def clone_rtc(self, rtc_repo, verbose=False):
        import wasanbon
        admin.git.git_command(['clone', rtc_repo.url, rtc_repo.name], verbose=verbose)
        return 0

    def get_rtc_repositories_from_package(self, package_obj, verbose=False):
        if verbose: sys.stdout.write('# Loading Repository File from package(%s)\n' % (package_obj.name))
        repos = []
        import wasanbon
        import yaml
        dict_ = yaml.load(open(package_obj.rtc_repository_file, 'r'))
        if not dict_ is None:
            for name, value in dict_.items():
                if 'git' in value.keys():
                    typ = 'git'
                    pass

                if verbose: sys.stdout.write('## Loading Repository (name=%s, url=%s)\n'%(name, value[typ]))

                repo = admin.binder.Repository(name=name, type=typ, url=value[typ], platform=wasanbon.platform(), description=value['description'])
                repos.append(repo)
                pass
            pass
        return repos
