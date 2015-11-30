import os, sys, types, subprocess
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

owner_sign = '_owner'

class Plugin(PluginFunction):
    """ Binder (Collection of repositories) management """

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.git', 'admin.github']

    def _print_binders(self, argv):
        binders = self.get_binders()
        for b in binders:
            print b.owner

    def _print_alternatives(self, argv):
        argv = [arg for arg in argv if not arg.startswith('-')]
        if len(argv) == 4:
            self._print_binders(argv)
        else:
            print ""

    @manifest 
    def create(self, argv):
        """ Create Binder. 
        $ wasanbon-admin.py binder create"""
        self.parser.add_option('-s', '--service', help='set upstream service',  default='github', metavar='SERVICE', dest='service')
        self.parser.add_option('-u', '--user', help='set username',  default=None, metavar='USER', dest='user')
        self.parser.add_option('-p', '--password', help='set password',  default=None, metavar='PASSWD', dest='password')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        service = options.service
        
        user, passwd = wasanbon.user_pass(user=options.user, passwd=options.password)
        sys.stdout.write('# Creating wasanbon binder in your %s\n' % service)
        repo_name = 'wasanbon_binder'
        target_path = os.path.join(wasanbon.rtm_home(), 'binder', user + owner_sign, repo_name + '.git')
        if service=='github':
            github = admin.github.Github(user, passwd)
            if github.exists_repo(repo_name):
                sys.stdout.write(' @ You have already created your own repository.\n')
                sys.stdout.write(' @ wasanbon just clone it.\n')
                download_repository(url=url, target_path=target_path, verbose=verbose)
                return True
            repo_obj = github.fork_repo('sugarsweetrobotics', 
                                        'wasanbon_binder_template',
                                        repo_name, verbose=verbose)
        else:
            sys.stdout.write('## Unknown serviec name.\n')
            return -1
        return 0


    @manifest
    def delete(self, argv):
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        self.parser.add_option('-u', '--user', help='set username',  default=None, metavar='USER', dest='user')
        self.parser.add_option('-p', '--password', help='set password',  default=None, metavar='PASSWD', dest='password')
        self.parser.add_option('-s', '--service', help='set upstream service',  default='github', metavar='SERVICE', dest='service')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        force = options.force_flag
        service = options.service

        user, passwd = wasanbon.user_pass(user=options.user, passwd=options.password)
        sys.stdout.write('# Creating wasanbon binder in your %s\n' % service)
        repo_name = 'wasanbon_binder'
        target_path = os.path.join(wasanbon.rtm_home(), 'binder', user + owner_sign, repo_name + '.git')
        if service=='github':
            github = admin.github.Github(user, passwd)
            if github.exists_repo(repo_name):
                if not force:
                    from wasanbon import util
                    if util.yes_no('## Really delete?') == 'no':
                        sys.stdout.write('## Aborted.\n')
                        return 0
                
                github.delete_repo(repo_name)
                return 0
        else:
            sys.stdout.write('# Unknown service name %s\n' % service)
            return -1
        return 0
        
    @manifest
    def update(self, argv):
        """ Update Binder. Download Binder from repository """
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        #import binder
        path = os.path.join(admin.environment.setting_path, '..', 'repository.yaml')
        download_repositories(path, verbose=verbose)

    @manifest
    def list(self, args):
        """ List Installed Binders. """
        options, argv = self.parse_args(args)
        verbose = options.verbose_flag
        binders = self.get_binders(verbose=verbose)
        for b in binders:
            print b.owner, ' :'
            print '  url : ', b.path
        return 0
    
    @manifest
    def rtcs(self, args):
        """ Show RTC Repositories in your binders. """
        self.parser.add_option('-l', '--long', help='Long Format (default=False)', default=False, action='store_true', dest='long_flag')
        options, argv = self.parse_args(args)
        verbose = options.verbose_flag
        long = options.long_flag

        binders = self.get_binders(verbose=verbose)
        rtcs  =[]
        for binder in binders:
            rtcs = rtcs + binder.rtcs

        rtcs = sorted(rtcs, key=lambda rtc : rtc.name)

        for rtc in rtcs:
            if not long:
                print ' - %s' % rtc.name
            else:
                print '%s :' % rtc.name
                print '  %s : %s' % ('url', rtc.url)
                print '  %s : %s' % ('type', rtc.type)
                print '  %s : "%s"' % ('description', rtc.description)
                print '  %s : %s' % ('platform', rtc.platform)
                
        return 0
    
    @manifest
    def packages(self, args):
        """ List Package repositories in your binders. """
        self.parser.add_option('-l', '--long', help='Long Format (default=False)', default=False, action='store_true', dest='long_flag')
        options, argv = self.parse_args(args)
        verbose = options.verbose_flag
        long = options.long_flag


        binders = self.get_binders(verbose=verbose)
        for binder in binders:
            for package in binder.packages:
                if not long:
                    print ' - %s' % package.name
                else:
                    print '%s :' % package.name
                    print '  %s : %s' % ('url', package.url)
                    print '  %s : %s' % ('type', package.type)
                    print '  %s : %s' % ('description', package.description)
                    print '  %s : %s' % ('platform', package.platform)

        return 0


    @manifest
    def commit(self, args):
        """ Commit changes of binder file (.yaml) to local repository.
        $ wasanbon-admin.py binder commit [binder_owner_name] (comment)
        """
        self.parser.add_option('-p', '--push', help='Push simultaneously', default=False, dest='push_flag', action='store_true')
        options, argv = self.parse_args(args[:], self._print_alternatives)
        verbose = options.verbose_flag
        push = options.push_flag

        wasanbon.arg_check(argv, 5)
        binder_name = argv[3]
        comment = argv[4]
        binder = self.get_binder(binder_name, verbose=verbose)
        sys.stdout.write('# Committing binder %s to local repository\n' % binder_name)        

        p = admin.git.git_command(['commit', '-am', comment], path=binder.path)
        output, stderr = p.communicate()
        #output = p.stdout.read()
        if verbose: sys.stdout.write(output)
        if True:
            sys.stdout.write('## Success.\n')
            if push:
                sys.stdout.write('# Pushing binder %s\n' % binder_name)
                remote = 'origin'
                branch = 'master'
                p = admin.git.git_command(['push', remote, branch], path=binder.path)
                output, stderr = p.communicate()
                #output = p.stdout.read()
                if verbose: sys.stdout.write(output)
                if p.returncode != 0:
                    sys.stdout.write('## Failed.\n')
                    return -1
                sys.stdout.write('## Success.\n')
            return 0
        sys.stdout.write('## Failed.\n')
        return -1

    def get_binders(self, verbose=False):
        return get_binders(verbose=verbose)

    def get_binder(self, binder_name, verbose=False):
        binders = self.get_binders(verbose=verbose)
        for b in binders:
            if b.owner == binder_name:
                return b
        return None

    def get_package_repos(self, verbose=False):    
        return get_package_repos(verbose=verbose)
            
    def get_rtc_repos(self, verbose=False):
        binders = self.get_binders(verbose=verbose)
        return [r for b in binders for r in b.rtcs]
            
        
    def get_package_repo(self, name, verbose=False):
        return get_package_repo(name, verbose=verbose)

    def Repository(self, name, type, platform, url, description, path=None):
        return Repository(name=name, 
                          type=type,
                          platform=platform,
                          url=url,
                          description=description,
                          path=path)

        
_owner_sign = '_owner'

#plugin_obj = None

class Repository(object):
    def __init__(self, name, type, platform, url, description, path=None):

        self._name = name
        self._url  = url
        self._type = type
        self._platform = platform
        self._description = description
        self._path = path
        pass

    @property
    def path(self):
        return self._path

    def is_local(self):
        return (not self.path is None)
    
    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def hash(self):
        if self.type == 'git':
            popen = admin.git.git_command(['log', '--pretty=format:"%H"', '-1'], pipe=True, path=self.path)
            popen.wait()
            return popen.stdout.readline().strip()[1:-1]
        return ""

    @property
    def basename(self):
        b = os.path.basename(self.url)
        if b.endswith('.git'):
            b = b[:-4]
        return b

    @property
    def type(self):
        return self._type

    @property
    def platform(self):
        return self._platform
    
    @property
    def description(self):
        return self._description

    @property
    def service(self):
        service = self._url.split('/')[3].split('.')[0]
        if service.find('@') >= 0:
            return service.split('@')[1]
        return service

    
    

class Binder(object):
    def __init__(self, owner, path):
        self._owner = owner
        self._path = path
        self._rtcs = None
        self._packages = None

    @property
    def rtcs(self):
        if self._rtcs is None:
            import yaml
                     
            self._rtcs = []
            path_ = os.path.join(self.path, 'rtcs')
            for f in os.listdir(path_):

                filepath = os.path.join(path_, f)
                if not filepath.endswith('yaml'):
                    continue
                d = yaml.load(open(filepath, 'r'))
                if type(d) is types.DictType:
                    for name, v in d.items():
                        self._rtcs.append(Repository(name = name,
                                                     description = v['description'],
                                                     type = v['type'],
                                                     platform = v['platform'],
                                                     url = v['url']))


        return self._rtcs

    @property
    def packages(self):
        if self._packages is None:
            import yaml
                     
            self._packages = []
            path_ = os.path.join(self.path, 'packages')
            for f in os.listdir(path_):
                filepath = os.path.join(path_, f)
                if not filepath.endswith('yaml'):
                    continue
                d = yaml.load(open(filepath, 'r'))
                if type(d) is types.DictType:
                    for name, v in d.items():
                        self._packages.append(Repository(name = name,
                                                     description = v['description'],
                                                     type = v['type'],
                                                     platform = v['platform'],
                                                     url = v['url']))


        return self._packages

    @property
    def owner(self):
        return self._owner

    @property
    def path(self):
        return self._path

    @property
    def rtcs_path(self):
        return os.path.join(self.path, 'rtcs')
    @property
    def packages_path(self):
        return os.path.join(self.path, 'packages')
    @property
    def rtc_files(self):
        return [f for f in os.listdir(self.rtcs_path) if f.endswith('yaml')]

    @property
    def package_files(self):
        return [f for f in os.listdir(self.packages_path) if f.endswith('yaml')]
    

def get_package_repos(verbose=False):
    binders = get_binders(verbose=verbose)
    package_repos = []
    for binder in binders:
        package_repos = package_repos + binder.packages
        
    return package_repos

def get_package_repo(name, verbose=False):
    for package_repo in get_package_repos(verbose=verbose):
        if package_repo.name == name:
            return package_repo

    import wasanbon
    raise wasanbon.RepositoryNotFoundException()


def get_binders(verbose=False):
    path_ = repository_path()    
    binders = []
    for name in os.listdir(path_):
        namep = os.path.join(path_, name)
        for b in os.listdir(namep):
            bp = os.path.join(namep, b)
            if 'setting.yaml' in os.listdir(bp):
                binders.append(Binder(name, bp))
    return binders

def get_default_repo_directory():
    import wasanbon
    _default_repo_directory = os.path.join(wasanbon.home_path, 'binder')
    if not os.path.isdir(_default_repo_directory):
        os.mkdir(_default_repo_directory)

    return _default_repo_directory

def download_repositories(setting_filepath, verbose=False, force=False):
    if verbose:
        sys.stdout.write(' - Downloading Repositories....\n')
        sys.stdout.write('    - Opening setting file in %s\n' % setting_filepath)

    with open(setting_filepath, 'r') as repo_setting:
        import yaml
        for name, value in yaml.load(repo_setting).items():
            if verbose: sys.stdout.write('    - Repository : %s\n' % name)
            urls = value['url']
            if type(urls) is not types.ListType:
                urls = [urls]
            for url in urls:
                download_repository(url, verbose=verbose, force=force)
    return True

def repository_path(url=None):
    root = get_default_repo_directory()
    if url:
        root = os.path.join(root, url.split('/')[-2])
    return root
                
def download_repository(url, target_path='',verbose=False, force=False):
    _repository_path = repository_path(url)
    if not target_path:
        target_path = os.path.join(_repository_path, url.split('/')[-1])
    if verbose:
        sys.stdout.write('    - Downloading repository %s\n' % url)
        sys.stdout.write('        into %s\n' % target_path)
    
    git_command = admin.git.git_command
    if os.path.isdir(target_path):
        if os.path.isdir(os.path.join(target_path, '.git')):
            git_command(['pull'], verbose=True, path=target_path)
        else: # Directory exists but not git repository dir
            git_command(['clone', url, target_path], verbose=verbose)
        pass
    else:
        if not os.path.isdir(target_path):
            os.makedirs(target_path)
            pass
        git_command(['clone', url, target_path], verbose=verbose)
        pass

    if verbose:
        sys.stdout.write('    - Parsing child Binder\n')
    setting_file_path = os.path.join(target_path, 'setting.yaml')
    if os.path.isfile(setting_file_path):
        with open(setting_file_path, 'r') as setting_file:
            import yaml
            setting = yaml.load(setting_file)
            if type(setting) is types.DictType:
                child_repos = setting.get('child_binder', [])
                for repo in child_repos:
                    download_repository(repo, verbose=verbose, force=force)
    pass

