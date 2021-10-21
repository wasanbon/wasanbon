import sys
import os
import time
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest


class Plugin(PluginFunction):
    """ Github.com repository server management plugin. """

    def __init__(self):
        # PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    def Github(self, user=None, passwd=None, token=None):
        """ Return GithubReference object. Github Reference object can communicate with github.com server """
        return GithubReference(user, passwd, token)

    def Repository(self, url, user, passwd, token, verbose=False):
        """ Return GithubRepository object. """
        return GithubRepository(url, user, passwd, token, verbose=False)


class GithubRepository():

    def __init__(self, url, user, passwd, token, verbose=False):
        self._url = url
        if token:
            self._github_obj = github.Github(token)
        else:
            self._github_obj = github.Github(user, passwd)
        git_user = github_obj.get_user()

    @property
    def url(self):
        return self._url

    def fork(self, user, repo, verbose=False):
        pass


class GithubReference ():
    def __init__(self, user=None, passwd=None, token=None):
        import github
        if token:
            self._github = github.Github(token)
        else:
            self._github = github.Github(user, passwd)
        self._user = user

        if token == None and passwd:
            try:
                self._github.get_user(user).login
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

    def get_repo_url(self, name, user=None, verbose=False):
        repo = self.get_repo(name, user, verbose)
        if repo:
            return repo.html_url

    def get_repo(self, name, user=None, verbose=False):
        try:
            if user:
                if verbose:
                    sys.stdout.write(' - Searching Repository %s/%s\n' % (user, name))
                repo = self._github.get_user(user).get_repo(name)
                pass
            else:
                if verbose:
                    sys.stdout.write(' - Searching Repository %s/%s\n' % (self.user, name))
                repo = self._github.get_user().get_repo(name)

        except Exception as ex:
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
            sys.stdout.write(' - Forking Repositoy %s/%s\n' % (user, name))
        if self.exists_repo(name, verbose):
            raise wasanbon.RepositoryAlreadyExistsException()

        his_repo = self.get_repo(user=user, name=name, verbose=verbose)
        ret = self._github.get_user().create_fork(his_repo)
        time.sleep(5)
        for i in range(0, 5):  # try 5 times
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
        self._github.get_user(owner_user).get_repo(owner_repo).create_pull(title=title, body=body, head=self.user + ':master', base='master')

    def get_file_contents(self, repo_owner, repo_name, file, verbose=False):
        if verbose:
            sys.stdout.write(' - loading %s/%s/%s\n' % (repo_owner, repo_name, file))

        import requests
        url = "https://raw.githubusercontent.com/" + repo_owner + "/" + repo_name + "/master/" + file
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            with open(file, 'wb') as saveFile:
                saveFile.write(response.content)
            return 0

        return -1
