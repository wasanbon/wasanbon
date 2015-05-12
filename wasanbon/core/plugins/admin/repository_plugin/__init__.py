import os, sys, traceback
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):
    """ Repository management plugin (mainly for package repository) """

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        #import repository
        #repository.plugin_obj = self
        pass

    def depends(self):
        return ['admin.environment', 
                'admin.package', 
                'admin.rtc',
                'admin.git',
                'admin.binder']

    def _list_package_repos(self, args):
        for r in admin.binder.get_package_repos():
            print r.name
    
    #@property
    #def repository(self):
    #    import repository
    #    return repository

    @manifest
    def list(self, args):
        """ Listing Repository in Binder """
        admin.binder.packages(args)
        
    @manifest
    def clone(self, args):
        """ Cloning Package from repository. 
        $ wasanbon-admin.py repository clone [PACKAGE_REPOSITORY_NAME] """
        #self.parser.add_option('-r', '--remove', help='Remove All Files (default=False)', default=False, action='store_true', dest='remove_flag')
        options, argv = self.parse_args(args[:], self._list_package_repos)
        verbose = options.verbose_flag
        #remove = options.remove_flag

        wasanbon.arg_check(argv, 4)
        repo_name = argv[3]
        package_repo = admin.binder.get_package_repo(repo_name)
        sys.stdout.write('# Cloning Package %s\n' % package_repo.name)
        #import repository
        try:
            if self.clone_package(package_repo, path=package_repo.basename, verbose=verbose) == 0:
                sys.stdout.write('## Success.\n')
                return 0
        except:
            return -1
        else:
            sys.stdout.write('## Failed.\n')
            return -1
        
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
        retval = 0
        try:
            os.chdir(pack.get_rtcpath())

            repos = self.get_rtc_repositories_from_package(pack, verbose=verbose)
            for repo in repos:
                if self.clone_rtc(repo, verbose=verbose) != 0:
                    retval = -1
                pass
        except Exception, ex:
            traceback.print_exc()
            raise ex
        finally:
            os.chdir(current_dir)
        return retval

    def clone_rtc(self, rtc_repo, verbose=False):
        import wasanbon
        admin.git.git_command(['clone', rtc_repo.url, rtc_repo.name], verbose=verbose)
        curdir = os.getcwd()
        os.chdir(os.path.join(curdir, rtc_repo.name))
        admin.git.git_command(['submodule', 'init'], verbose=verbose)
        admin.git.git_command(['submodule', 'update'], verbose=verbose)
        os.chdir(curdir)
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
                    url = value[typ]
                    pass
                elif 'url'in value.keys():
                    typ = value['type']
                    url = value['url']
                if verbose: sys.stdout.write('## Loading Repository (name=%s, url=%s)\n'%(name, url))
                path = None
                try:
                    rtc = admin.rtc.get_rtc_from_package(package_obj, name)
                    path = rtc.path
                except wasanbon.RTCNotFoundException:
                    pass

                repo = admin.binder.Repository(name=name, type=typ, url=url, platform=wasanbon.platform(), description=value['description'], path=path)
                repos.append(repo)
                pass
            pass
        return repos

    def get_repository_from_rtc(self, rtc, verbose=False):
        path = rtc.path
        if '.git' in os.listdir(path):
            return self.get_git_repository_from_rtc(rtc, verbose=verbose)
        else:
            return None


    def get_repository_from_path(self, path, verbose=False, description=""):
        if '.git' in os.listdir(path):
            return self.get_git_repository_from_path(path, verbose=verbose, description=description)
        return None
        
    def get_git_repository_from_path(self, path, verbose=False, description=""):
        typ = 'git'
        p = admin.git.git_command(['config', '--get', 'remote.origin.url'], path=path)
        p.wait()
        url = p.stdout.read()
        name = os.path.basename(url).strip()
        desc = description
        if name.endswith('.git'): name = name[:-4]
        repo = admin.binder.Repository(name=name, type=typ, url=url, description=desc, platform=wasanbon.platform(), path=path)
        return repo

    def get_git_repository_from_rtc(self, rtc, verbose=False):
        typ = 'git'
        name = rtc.rtcprofile.basicInfo.name
        p = admin.git.git_command(['config', '--get', 'remote.origin.url'], path=rtc.path)
        p.wait()
        url = p.stdout.read()
        repo = admin.binder.Repository(name=rtc.rtcprofile.basicInfo.name, type=typ, url=url, description=rtc.rtcprofile.basicInfo.description, platform=wasanbon.platform(), path=rtc.path)
        return repo

    def get_repository_hash(self, repo):
        if repo.type == 'git':
            p = admin.git.git_command(['rev-parse', 'HEAD'], path=repo.path)
            p.wait()
            hash = p.stdout.read()
            return hash.strip()
        return None

    def is_updated(self, repo, verbose=False):
        output = self.get_status(repo, verbose=verbose)
        return (output.find("modified") > 0) or (output.find("Untracked") > 0)

    def is_modified(self, repo, verbose=False):
        output = self.get_status(repo, verbose=verbose)
        return (output.find("modified") > 0)

    def is_added(self, repo, verbose=False):
        output = self.get_status(repo, verbose=verbose)
        return (output.find("Untracked") > 0)
            
    def get_status(self, repo, verbose=False):
        if not repo.is_local():
            sys.stdout.write('# Given Repository is not local repository.\n')
            return ""
        if repo.type == 'git':
            p = admin.git.git_command(['status'], path=repo.path)
            p.wait()
            output = p.stdout.read()
            if verbose:
                sys.stdout.write(output)
            return output
        return None

    def commit(self, repo, comment, verbose=False):
        if repo.type == 'git':
            if verbose: sys.stdout.write('## Committing GIT type repository (%s)\n' % repo.name)
            p = admin.git.git_command(['commit', '-am', comment], path=repo.path)
            p.wait()
            output = p.stdout.read()
            if verbose: sys.stdout.write(output)
            return 0
            
    def push(self, repo, verbose=False, remote='origin'):
        if repo.type == 'git':
            if verbose: sys.stdout.write('## Pushing GIT type repository (%s)\n' % repo.name)
            p = admin.git.git_command(['push', 'origin', 'master'], path=repo.path)
            p.wait()
            output = p.stdout.read()
            if verbose: sys.stdout.write(output)
            return p.returncode

    def pull(self, repo, verbose=False, remote='origin'):
        if repo.type == 'git':
            if verbose: sys.stdout.write('## Pulling GIT type repository (%s)\n' % repo.name)
            p = admin.git.git_command(['pull', 'origin', 'master'], path=repo.path)
            p.wait()
            output = p.stdout.read()
            if verbose: sys.stdout.write(output)
            return p.returncode
