import github


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
