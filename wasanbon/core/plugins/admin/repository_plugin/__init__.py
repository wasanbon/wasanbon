import os, sys, traceback, types
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):
    """ Repository management plugin (mainly for package repository) """


    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        #import repository
        #repository.plugin_obj = self

        self.default_dot_gitignore_rtc = "*.pyc *~ *.bak *.BAK build-* *.log *.lock"
        self.default_dot_gitignore_package = "*.pyc *~ bin/* *.bak *.BAK *.log *.lck rtc/*"

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
        self.parser.add_option('-u', '--url', help='Directory point the url of repository  (default="None")', default="None", type="string", dest="url")
        self.parser.add_option('-t', '--type', help='Set the type of repository  (default="git")', default="git", type="string", dest="type")
        options, argv = self.parse_args(args[:], self._list_package_repos)
        verbose = options.verbose_flag
        url = options.url
        typ = options.type

        if url is "None":
            wasanbon.arg_check(argv, 4)
            repo_name = argv[3]
            package_repo = admin.binder.get_package_repo(repo_name)
            sys.stdout.write('# Cloning Package %s\n' % package_repo.name)
        #import repository
            try:
                if self.clone_package(package_repo, path=package_repo.basename, verbose=verbose) == 0:
                    sys.stdout.write('## Success.\n')
                    return 0
                else:
                    sys.stdout.write('## Failed.\n')
                    return -1
            except:
                return -1
        else:
            package_repo = admin.binder.Repository(os.path.basename(url), type=typ, platform=wasanbon.platform, url=url, description="")
            sys.stdout.write('# Cloning Package %s\n' % package_repo.name)
            try:
                if self.clone_package(package_repo, path=package_repo.basename, verbose=verbose) == 0:
                    sys.stdout.write('## Success.\n')
                    return 0
                else:
                    sys.stdout.write('## Failed.\n')
                    return -1
            except:
                return -1
            
        
    def clone_package(self, package_repo, path=None, verbose=False):
    	""" Clone package from Repository.
    	package_repo : 
    	path :
    	verbose :
    	 """
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
        process_ = admin.git.git_command(['clone', rtc_repo.url, rtc_repo.name], verbose=verbose)
        if process_.returncode != 0:
            if verbose: sys.stdout.write('### Cloning RTC (%s) failed.\n' % rtc_repo.name)
            return -1
        curdir = os.getcwd()
        os.chdir(os.path.join(curdir, rtc_repo.name))
        process_ = admin.git.git_command(['submodule', 'init'], verbose=verbose)
        if process_.returncode != 0:
            if verbose: sys.stdout.write('### Init Submodule RTC (%s) failed.\n' % rtc_repo.name)
            return -2
        process_ = admin.git.git_command(['submodule', 'update'], verbose=verbose)
        if process_.returncode != 0:
            if verbose: sys.stdout.write('### Update Submodule RTC (%s) failed.\n' % rtc_repo.name)
            return -3
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
        url = p.stdout.read().strip()
        name = os.path.basename(url).strip()
        desc = description.strip()
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

    def init_git_repository_to_path(self, path, verbose=False):
        if verbose: sys.stdout.write('# Initializing git repository to %s\n' % path)
        p =admin.git.git_command(['init'], path=path, verbose=verbose)
        p.wait()
        if p.returncode != 0:
            if verbose: sys.stdout.write('## Error git command returns non zero value (%s)\n' % p.returncode)
            return None
        return self.get_git_repository_from_path(path, verbose=verbose)
    
    def is_rtc_repo(self, repo, verbose=False):
        filepath = os.path.join(repo.path, 'RTC.xml')
        return os.path.isfile(filepath)


    def add_default_dot_gitignore(self, repo, verbose=False):
        if self.is_rtc_repo(repo, verbose):
            default_dot_gitignore = self.default_dot_gitignore_rtc
        else:
            default_dot_gitignore = self.default_dot_gitignore_package

        lines = [t.strip() for t in default_dot_gitignore.split(' ')]
        filepath = os.path.join(repo.path, '.gitignore')

        f = open(filepath, 'w')
        for line in lines:
            f.write(line + '\n')
        f.close()
        return False

    def check_dot_gitignore(self, repo, verbose=False):
        if self.is_rtc_repo(repo, verbose):
            default_dot_gitignore = self.default_dot_gitignore_rtc
        else:
            default_dot_gitignore = self.default_dot_gitignore_package

        tokens = [t.strip() for t in default_dot_gitignore.split(' ')]

        filepath = os.path.join(repo.path, '.gitignore')
        if not os.path.isfile(filepath):
            if verbose: sys.stdout.write('## No gitignore file in %s\n'% repo.name)
            return self.add_default_dot_gitignore(repo, verbose)

        if verbose: sys.stdout.write('## .gitignore found.\n')
        f = open(filepath, 'r')
        foundCount = 0
        lines = []
        for line in f:
            lines.append(line)
            if line.strip() in tokens:
                foundCount = foundCount + 1
                tokens.remove(line.strip())
        f.close()
        if len(tokens) == 0:
            if verbose: sys.stdout.write('### .gitignore covers default options.\n')
            return True
        if verbose:
            sys.stdout.write('### WARNING! .gitignore does not cover default options.\n')
            for token in tokens:
                sys.stdout.write(' - %s\n' % token)
                
            sys.stdout.write('### Fixing automatically.\n')
            pass
        
        os.rename(filepath, filepath + wasanbon.timestampstr())
        f = open(filepath, 'w')
        lines = lines + tokens
        for line in lines:
            f.write(line + '\n')

        f.close()
        return False
        
    def is_updated(self, repo, verbose=False):
        output = self.get_status(repo, verbose=verbose)
        return (output.find("modified") > 0) or (output.find("Untracked") > 0)

    def is_modified(self, repo, verbose=False):
        output = self.get_status(repo, verbose=verbose)
        return (output.find("modified") > 0)

    def is_untracked(self, repo, verbose=False):
        output = self.get_status(repo, verbose=verbose)
        return (output.find("Untracked") > 0)

    def is_added(self, repo, verbose=False):
        output = self.get_status(repo, verbose=verbose)
        return (output.find("new file:") > 0)
            
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
            
    def push(self, repo, verbose=False, remote='origin', branch='master'):
        if repo.type == 'git':
            if verbose: sys.stdout.write('## Pushing GIT type repository (%s)\n' % repo.name)
            p = admin.git.git_command(['push', remote, branch], path=repo.path)
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

    def add(self, repo, filelist, verbose=False):
        if  not type(filelist) is types.ListType:
            filelist = [filelist]
        if repo.type == 'git':
            if verbose: sys.stdout.write('## Adding File to GIT type repository (%s)\n' % repo.name)
            for f in filelist:
                p = admin.git.git_command(['add', f], path=repo.path)
                p.wait()
                if verbose: sys.stdout.write(p.stdout.read())
            return p.returncode

        return -1


    def add_files(self, repo, verbose=False, exclude_if_git_repo=True, exclude_path=[], exclude_pattern='^\.|.*\.pyc$|.*~$|.*\.log$'):
        directory = repo.path
    
        def list_filepath_not_under_git(directory, output, verbose=False):
            import re
            if re.compile(exclude_pattern).match(os.path.basename(directory)):
                return

            for p in exclude_path:
                if directory.startswith( p.replace('/', '\\') ):
                    return
            if os.path.isdir(directory):
                dirs = os.listdir(directory)
                if '.git' in dirs and exclude_if_git_repo:
                    return # Do nothing
                for d in dirs:
                    fullpath = os.path.join(directory, d)
                    list_filepath_not_under_git(fullpath, output, verbose=verbose)
            elif os.path.isfile(directory):
                output.append(directory)
                
        filelist = []
        for d in os.listdir(directory):
            fullpath = os.path.join(directory, d)
            if not fullpath in exclude_path:
                list_filepath_not_under_git(fullpath, filelist, verbose=True)
        

        if self.add(repo, filelist, verbose=verbose) != 0:
            sys.stdout.write('## Add File failed.\n')
            return -1
