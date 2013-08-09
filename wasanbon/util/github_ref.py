import sys, os, time
import github
from . import git

class GithubLogingException(Exception):
    def __init__(self):
        pass

class RepositoryAlreadyExistsException(Exception):
    def __init__(self):
        pass

class RepositoryNotFoundException(Exception):
    def __init__(self):
        pass


class GithubReference ():
    def __init__(self, user, passwd):
        self._github = github.Github(user, passwd)
        self._user = user
        git_user = self._github.get_user()
        try:
            git_user.login
        except:
            raise GithubLoginException()
            return
        

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
                print 'REPO', repo
        except Exception, ex:
            raise RepositoryNotFoundException()
        return repo

    def create_repo(self, name):
        if self.exists_repo(name):
            raise RepositoryAlreadyExistsException()
        repo = self._github.get_user().create_repo(name)
        return repo

    def fork_repo(self, user, name, verbose=False):
        if verbose:
            sys.stdout.write(' - Forking Repositoy %s/%s\n' %  (user, name))

        if self.exists_repo(name, verbose):
            raise RepositoryAlreadyExistsException()
        
        his_repo = self.get_repo(user=user, name=name, verbose=verbose)
        self._github.get_user().create_fork(his_repo)
        time.sleep(5)

        for i in range(0, 5): # try 5 times
            try:
                if verbose:
                    sys.stdout.write(' - Trying to check your repository %s\n' % name)
                return self.get_repo(name)
            except:
                time.sleep(1)
                pass
        if verbose:
            sys.stdout.write(' - Can not find your repository.\n')
        raise RepositoryNotFoundException()


    def pull_request(self, name, title, body, verbose=False):
        repo = self._github.get_user().get_repo(name)
        owner_url = repo.parent.url
        owner_user, owner_repo = owner_url.split('/')[-2:]
        self._github.get_user(owner_user).get_repo(owner_repo).create_pull(title=title, body=body, head=self.user+':master', base='master')
