import sys, traceback
import wasanbon
import wasanbon.core
from wasanbon.core.package import *
from wasanbon.util import git
import package_obj

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
                sys.stdout.write(' - There is %s package in workspace.yaml\n' % self.name)
                sys.stdout.write(' - Please unregister the package\n')
            raise wasanbon.PackageAlreadyExistsException()
        except wasanbon.PackageNotFoundException, ex:
            #traceback.print_exc()
            pass
        
        appdir = os.path.join(os.getcwd(), self.name)
        if os.path.isdir(appdir) or os.path.isfile(appdir):
            if verbose:
                print ' - There seems to be %s here. Please change application name.' % appdir
            raise wasanbon.DirectoryAlreadyExistsException()
            #return False

        git.git_command(['clone', self.url, appdir], verbose=verbose)
        _package = wasanbon.core.package.create_package(self.name, verbose=verbose, force_create=True, overwrite=False)
        
        # Change ext to OS respondable type
        _package.validate(verbose=verbose, autofix=True, ext_only=True)

        #for repo in _package.rtc_repositories:
        #    if verbose:
        #        sys.stdout.write(' - Cloning RTC %s\n' % repo.name)
        #    rtc = repo.clone(path=os.path.join(appdir, _package.setting['RTC_DIR']), verbose=verbose)
        #    #sys.stdout.write(' - Building RTC %s\n' % repo.name)
        #    #rtc.build(verbose=verbose)
        #    #_package.install(rtc, precreate=False, preload=True, verbose=verbose)
        return package_obj.Package(appdir)


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

    def get_repository_yaml(self, user, passwd, verbose=False, service='github'):
        pass
    """
    def get_rtcprofile(self, user, passwd, verbose=False, service='github'):
        from wasanbon.core.repositories import github_api
        if service == 'github':
            github_obj = github_api.GithubReference(user, passwd)
            prof_text = github_obj.get_file_contents(self.user, self.repo_name, 'RTC.xml', verbose=verbose)
            from wasanbon.core.rtc import rtcprofile
            return rtcprofile.RTCProfile(str=prof_text)
        return None
    """ 

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
    def protocol(self):
        return 'git'

    @property
    def repo_name(self):
        repo_name = os.path.basename(self._url)
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        return repo_name
        
    @property
    def user(self):
        return self.url.split('/')[-2]

    def get_rtcrepositories(self, verbose=False, service='github'):
        from wasanbon.core.repositories import github_api
        if service == 'github':
            github_obj = github_api.GithubReference() # user, passwd)
            prof_text = github_obj.get_file_contents(self.user, self.repo_name, 'rtc/repository.yaml', verbose=verbose)
            dic = yaml.load(prof_text)
            rtcs_ = {}
            from wasanbon.core import rtc
            for rtc_name in dic.keys():
                repo = rtc.get_repository(rtc_name)
                if repo:
                    rtcs_[rtc_name] = repo
                else:
                    rtcs_[rtc_name] = rtc.RtcRepository(rtc_name, url=dic[rtc_name]['git'], desc=dic[rtc_name]['description'])
            return rtcs_
        return None
