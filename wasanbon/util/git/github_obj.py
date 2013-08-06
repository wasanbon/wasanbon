


class GithubRepository():

    def __init__(self, url, user, passwd, verbose=False):
        self._url = url


    @property
    def url(self):
        return self._url
