import sys, os, time 
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):
    """ Github.com repository server management plugin. """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    def Github(self, user=None, passwd=None):
        """ Return GithubReference object. Github Reference object can communicate with github.com server """
        return GithubReference(user, passwd)

    def Repository(self, url, user, passwd, verbose=False):
        """ Return GithubRepository object. """
        return GithubRepository(url, user, passwd, verbose=False)

class GithubRepository():

    def __init__(self, url, user, passwd, verbose=False):
        self._url = url
        self._github_obj = github.Github(user, passwd)
        git_user = github_obj.get_user()


    @property
    def url(self):
        return self._url

    def fork(self, user, repo, verbose=False):
        pass

class GithubReference ():
    def __init__(self, user=None, passwd=None):
        import github
        self._github = github.Github(user, passwd)
        self._user = user

        if passwd:
            try:
                git_user = self._github.get_user()
                git_user.login
            except:
                raise wasanbon.RemoteLoginException()


    @property
    def user(self):
        return self._user


    def exists_repo(self, name, user=None, verbose=False):
        try:
            repo = self.get_repo(name, user=user, verbose=verbose)
            return True
        except:
            return False

    

    def get_repo(self, name, user=None, verbose=False):
        try :
            if user:
                if verbose:
                    sys.stdout.write(' - Searching Repository %s/%s\n' % (user, name))
                repo = self._github.get_user(user).get_repo(name)
                pass
            else:
                if verbose:
                    sys.stdout.write(' - Searching Repository %s/%s\n' % (self.user, name))
                repo = self._github.get_user().get_repo(name)

        except Exception, ex:
            raise wasanbon.RepositoryNotFoundException()
        return repo

    def create_repo(self, name):
        if self.exists_repo(name):
            raise wasanbon.RepositoryAlreadyExistsException()
        repo = self._github.get_user().create_repo(name)
        return repo

    def delete_repo(self, name):
        if not self.exists_repo(name):
            raise wasanbon.RepositoryAlreadyExistsException()
        self._github.get_user().get_repo(name).delete()

    def fork_repo(self, user, name, newname, verbose=False):
        if verbose:
            sys.stdout.write(' - Forking Repositoy %s/%s\n' %  (user, name))
        if self.exists_repo(name, verbose):
            raise wasanbon.RepositoryAlreadyExistsException()
        
        his_repo = self.get_repo(user=user, name=name, verbose=verbose)
        ret = self._github.get_user().create_fork(his_repo)
        time.sleep(5)
        for i in range(0, 5): # try 5 times
            try:
                if verbose:
                    sys.stdout.write(' - Trying to check your repository %s\n' % name)
                forked_repo = self.get_repo(name)
                forked_repo.edit(newname)
                
                return forked_repo
            except:
                time.sleep(1)
                pass
        if verbose:
            sys.stdout.write(' - Can not find your repository.\n')
        raise wasanbon.RepositoryNotFoundException()


    def pull_request(self, name, title, body, verbose=False):
        repo = self._github.get_user().get_repo(name)
        owner_url = repo.parent.url
        owner_user, owner_repo = owner_url.split('/')[-2:]
        self._github.get_user(owner_user).get_repo(owner_repo).create_pull(title=title, body=body, head=self.user+':master', base='master')

    def get_file_contents(self, repo_owner, repo_name, file, verbose=False):
        if verbose:
            sys.stdout.write(' - loading %s/%s/%s\n' % (repo_owner, repo_name, file))

        import httplib
        host = "raw.githubusercontent.com"
        url = "/"+repo_owner+"/"+repo_name+"/master/"+file
        webservice = httplib.HTTPS(host)
        webservice.putrequest("GET", url)
        webservice.putheader("Host", host)
        webservice.putheader("Content-type", "text/html; charset=\"UTF-8\"")
        webservice.putheader("Content-length", "%d" % 0)
        webservice.endheaders()
        sc, sm, h = webservice.getreply()
        st= webservice.getfile().read()

        return st

    
