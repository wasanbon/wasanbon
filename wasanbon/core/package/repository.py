import sys
import wasanbon
import wasanbon.core
from wasanbon.core.package import *
from wasanbon.util import git

class PackageAlreadyExistsException(Exception):
    def __init__(self):
        pass


class PackageDirectoryExistsException(Exception):
    def __init__(self):
        pass

class PackageRepository():

    def __init__(self, name, desc, url):
        self._name = name
        self._url = url
        self._desc = desc
        pass


    def clone(self, verbose=False):
        try:
            _package = wasanbon.core.package.get_package(self.name, verbose)
            if verbose:
                print ' - There is %s package in workspace.yaml\n' % self.name
                print ' - Please unregister the package\n' 
            raise PackageAlreadyExistsException()
        except wasanbon.PackageNotFoundException, ex:
            pass
        
        appdir = os.path.join(os.getcwd(), self.name)
        if os.path.isdir(appdir) or os.path.isfile(appdir):
            if verbose:
                print ' - There seems to be %s here. Please change application name.' % appdir
            raise PackageDirectoryExistsException()
            #return False

        git.git_command(['clone', self.url, appdir], verbose=verbose)
        _package = wasanbon.core.package.create_package(self.name, verbose=verbose, force_create=True, overwrite=False)
        
        # Change ext to OS respondable type
        _package.validate(verbose=verbose, autofix=True, ext_only=True)

        for repo in _package.rtc_repositories:
            sys.stdout.write(' - Cloning RTC %s\n' % repo.name)
            rtc = repo.clone(path=os.path.join(appdir, _package.setting['RTC_DIR']), verbose=verbose)
            sys.stdout.write(' - Building RTC %s\n' % repo.name)
            rtc.build(verbose=verbose)
            _package.install(rtc, precreate=False, preload=True, verbose=verbose)
        return Package(appdir)


    def fork(self, user, passwd, verbose=False):
        _package = wasanbon.core.package.get_package(self.name, verbose)
        if _package:
            if verbose:
                print ' - There is %s package in workspace.yaml\n' % prjname
                print ' - Please unregister the package\n' 
            #return None
            raise PackageAlreadyExistsException()
        
        appdir = os.path.join(os.getcwd(), self.name)
        if os.path.isdir(appdir) or os.path.isfile(appdir):
            if verbose:
                print ' - There seems to be %s here. Please change application name.' % prjname
            raise PackageDirectoryExistsException()

            #return False
        sys.stdout.write(' - Forking URL:: %s\n' % url)
        github_obj = wasanbon.util.github.GithubReference(user, passwd)
        repo = github_obj.fork(self.user, self.repo_name, verbose=verbose)
        
        url = 'https://github.com/%s/%s.git' % (user, self.repo_name)
        return PackageRepository(user=user, name=self.name, url=url, desc=self.description)
        

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._desc

    @property
    def url(self):
        return self._url

    @property
    def user(self):
        return os.path.split('/')[-2]

    @property
    def repo_name(self):
        repo_name = os.path.basename(self._url)
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        return repo_name
        

