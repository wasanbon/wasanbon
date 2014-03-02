import os, sys, time
from bitbucket.bitbucket import Bitbucket



class BitbucketRepository():
    
    def __init__(self, url, user, passwd, verbose=False):
        self._url = url
        self._bb = Bitbucket(user, passwd)
        

class BitbucketReference():

    def __init__(self, user, passwd):
        self._bb = Bitbucket(user, passwd)
        self._user = user
        try:
            res, cmt = self._bb.get_privileges()
            if not res:
                raise wasanbon.RemoteLoginException()
        except:
            raise wasanbon.RemoteLoginException()
        
    def create_repo(self, name, verbose=False):
        ret, cmt = self._bb.repository.create(name)

        if not ret:
            if verbose:
                sys.stdout.write(' Create Repository in bitbucket Failed.\n')
                sys.stdout.write(' -- %s\n' % cmt)
            return None

        return True
        
