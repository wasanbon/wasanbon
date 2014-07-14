import os, sys, time, traceback, types
from bitbucket.bitbucket import Bitbucket
import wasanbon


class BitbucketRepository():
    
    def __init__(self, url, user, passwd, verbose=False, repo_dic=''):
        if type(url) == types.DictType:
            self._url = 'https://bitbucket.org/' + user + '/' + url['name'] + '.git'
        else:
            self._url = url
        self._bb = Bitbucket(user, passwd)
        

class BitbucketReference():

    def __init__(self, user, passwd):
        self._bb = Bitbucket(user, passwd)
        self._user = user
        self.__pass = passwd
        try:
            res, cmt = self._bb.get_privileges()
            if not res:
                raise wasanbon.RemoteLoginException()
        except:
            raise wasanbon.RemoteLoginException()

    def get_repo(self, name, user=None, verbose=False):
        try :
            if user:
                if verbose:
                    sys.stdout.write(' - Searching Repository %s/%s\n' % (user, name))
                bb = Bitbucket(user)
                ret, repos = bb.repository.all()
                if ret:
                    for repo in repos:
                        if repo[u'name'] == name:
                            return BitbucketRepository(repos, user, '')

            else:
                if verbose:
                    sys.stdout.write(' - Searching Repository %s/%s\n' % (self._user, name))
                bb = Bitbucket(self._user, self.__pass)
                ret, repos = bb.repository.all()
                if ret:
                    for repo in repos:
                        if repo[u'name'] == name:
                            return BitbucketRepository(repos, self._user, self.__pass)
        except Exception, ex:
            if verbose:
                traceback.print_exc()
            raise wasanbon.RepositoryNotFoundException()

        raise wasanbon.RepositoryNotFoundException()



    def exists_repo(self, name, user=None, verbose=False):
        try:
            repo = self.get_repo(name, user=user, verbose=verbose)
            return True
        except:
            return False
        
    def create_repo(self, name, verbose=False):
        ret, cmt = self._bb.repository.create(name)

        if not ret:
            if verbose:
                sys.stdout.write(' Create Repository in bitbucket Failed.\n')
                sys.stdout.write(' -- %s\n' % cmt)
            return None
        return True
        
    def fork_repo(self, user, name, newname, verbose=False):
        if verbose:
            sys.stdout.write(' - Forking Repositoy %s/%s\n' %  (user, name))
        if self.exists_repo(name, verbose):
            raise wasanbon.RepositoryAlreadyExistsException()

        import bitbucket
        import bitbucket.bitbucket
        URLS = {'POST_FORK' : 'repositories/%(accountname)s/%(repo_slug)s/fork/',}
        bitbucket.bitbucket.URLS.update(URLS)
        url = self._bb.url('POST_FORK', accountname=user, repo_slug=name)
        self._bb.dispatch('POST', url, auth=self._bb.auth, accountname=user, repo_slug=name, name=newname)
        
        time.sleep(5)
        for i in range(0, 5):
            try:
                if verbose:
                    sys.stdout.write(' - Trying to check your repository %s\n' % name)
                forked_repo = self.get_repo(newname, verbose=verbose)
                print forked_repo
                return forked_repo
            except:
                if verbose:
                    traceback.print_exc()
                time.sleep(1)
                pass

        if verbose:
            sys.stdout.write(' - Can not find your repository.\n')
        raise wasanbon.RepositoryNotFoundException()
            
