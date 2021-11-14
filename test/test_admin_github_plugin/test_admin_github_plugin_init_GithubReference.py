# test for wasanbon/core/plugins/admin/github_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.admin.github_plugin import GithubReference


class TestGithubReference(unittest.TestCase):

    def setUp(self):
        self.test = GithubReference(user='user', passwd='passwd', token='token')

    @mock.patch('github.Github', return_value='test_github')
    def test_init_1(self, mock_github):
        """__init__ normal case
        token = 'token'
        """
        ### test ###
        test = GithubReference(user='user', passwd='passwd', token='token')
        self.assertEqual('test_github', test._github)
        self.assertEqual('user', test._user)
        mock_github.assert_called_once_with('token')

    @mock.patch('github.Github.get_user.login')
    @mock.patch('github.Github', return_value='test_github')
    def test_init_2(self, mock_github, mock_get_user):
        """__init__ normal case
        token = None
        """
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.RemoteLoginException):
            test = GithubReference(user='user', passwd='passwd')
            self.assertEqual('test_github', test._github)
            self.assertEqual('user', test._user)
            mock_github.assert_called_once_with('user', 'passwd')
            mock_git_user.assert_called_once_with('user')

    def test_user(self):
        """user normal case"""
        ### test ###
        self.assertEqual('user', self.test.user)

    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.get_repo', return_value='repo')
    def test_exists_repo(self, mock_get_repo):
        """exists_repo normal case"""
        ### test ###
        self.assertEqual(True, self.test.exists_repo('name'))
        mock_get_repo.assert_called_once_with('name', user=None, verbose=False)

    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.get_repo', side_effect=Exception())
    def test_exists_repo_except(self, mock_get_repo):
        """exists_repo except case"""
        ### test ###
        self.assertEqual(False, self.test.exists_repo('name'))

    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.get_repo')
    def test_get_repo_url(self, mock_get_repo):
        """get_repo_url normal case"""
        ### setting ###
        repo = MagicMock(return_value=True)
        type(repo).html_url = PropertyMock(return_value='test_html_url')
        mock_get_repo.return_value = repo
        ### test ###
        self.assertEqual('test_html_url', self.test.get_repo_url('name'))

    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.get_repo')
    def test_get_repo_url_error(self, mock_get_repo):
        """get_repo_url error case
        repo not exists
        """
        ### setting ###
        mock_get_repo.return_value = None
        ### test ###
        self.assertEqual(None, self.test.get_repo_url('name'))

    @mock.patch('sys.stdout.write')
    def test_get_repo_1(self, mock_write):
        """get_repo normal case
        user != None
        """
        ### setting ###
        test = GithubReference(user='user', passwd='passwd', token='token')
        test._github = MagicMock(spec=['get_user'])
        get_user = MagicMock(spec=['get_repo'])
        get_user.get_repo.return_value = 'repo'
        test._github.get_user.return_value = get_user
        ### test ###
        self.assertEqual('repo', test.get_repo('test_name', user='test_user'))

    @mock.patch('sys.stdout.write')
    def test_get_repo_2(self, mock_write):
        """get_repo normal case
        user != None
        verbose = True
        """
        ### setting ###
        test = GithubReference(user='user', passwd='passwd', token='token')
        test._github = MagicMock(spec=['get_user'])
        get_user = MagicMock(spec=['get_repo'])
        get_user.get_repo.return_value = 'repo'
        test._github.get_user.return_value = get_user
        ### test ###
        self.assertEqual('repo', test.get_repo('test_name', user='test_user', verbose=True))
        mock_write.assert_called_once()

    @mock.patch('sys.stdout.write')
    def test_get_repo_3(self, mock_write):
        """get_repo normal case
        user = None
        """
        ### setting ###
        test = GithubReference(user='user', passwd='passwd', token='token')
        test._github = MagicMock(spec=['get_user'])
        get_user = MagicMock(spec=['get_repo'])
        get_user.get_repo.return_value = 'repo'
        test._github.get_user.return_value = get_user
        ### test ###
        self.assertEqual('repo', test.get_repo('test_name'))

    @mock.patch('sys.stdout.write')
    def test_get_repo_4(self, mock_write):
        """get_repo normal case
        user = None
        verbose = True
        """
        ### setting ###
        test = GithubReference(user='user', passwd='passwd', token='token')
        test._github = MagicMock(spec=['get_user'])
        get_user = MagicMock(spec=['get_repo'])
        get_user.get_repo.return_value = 'repo'
        test._github.get_user.return_value = get_user
        ### test ###
        self.assertEqual('repo', test.get_repo('test_name', verbose=True))
        mock_write.assert_called_once()

    @mock.patch('sys.stdout.write')
    def test_get_repo_except(self, mock_write):
        """get_repo except case
        """
        ### setting ###
        test = GithubReference(user='user', passwd='passwd', token='token')
        test._github = MagicMock(spec=['get_user'])
        get_user = MagicMock(spec=['get_repo'])
        get_user.get_repo.return_value = 'repo'
        test._github.get_user.side_effect = Exception()
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.RepositoryNotFoundException):
            test.get_repo('test_name', verbose=True)
            mock_write.assert_called_once()

    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.exists_repo')
    def test_create_repo(self, mock_exists_repo):
        """create_repo normal case"""
        ### setting ###
        mock_exists_repo.return_value = False
        test = GithubReference(user='user', passwd='passwd', token='token')
        test._github = MagicMock(spec=['get_user'])
        get_user = MagicMock(spec=['create_repo'])
        get_user.create_repo.return_value = 'repo'
        test._github.get_user.return_value = get_user
        ### test ###
        self.assertEqual('repo', test.create_repo('name'))

    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.exists_repo')
    def test_create_repo_except(self, mock_exists_repo):
        """create_repo except case"""
        ### setting ###
        mock_exists_repo.return_value = True
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.RepositoryAlreadyExistsException):
            self.test.create_repo('name')

    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.exists_repo')
    def test_delete_repo(self, mock_exists_repo):
        """delete_repo normal case"""
        ### setting ###
        mock_exists_repo.return_value = True
        test = GithubReference(user='user', passwd='passwd', token='token')
        test._github = MagicMock(spec=['get_user'])
        get_user = MagicMock(spec=['get_repo'])
        get_repo = MagicMock(spec=['delete'])
        get_user.get_repo.return_value = get_repo
        test._github.get_user.return_value = get_user
        ### test ###
        test.delete_repo('name')
        test._github.get_user.assert_called_once_with()
        get_user.get_repo.assert_called_once_with('name')
        get_repo.delete.assert_called_once()

    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.exists_repo')
    def test_delete_repo_except(self, mock_exists_repo):
        """create_repo except case"""
        ### setting ###
        mock_exists_repo.return_value = False
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.RepositoryAlreadyExistsException):
            self.test.delete_repo('name')

    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.get_repo')
    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.exists_repo')
    @mock.patch('time.sleep')
    def test_fork_repo(self, mock_sleep, mock_exists_repo, mock_get_repo):
        """fork_repo normal case"""
        ### setting ###
        mock_exists_repo.return_value = False
        forked_repo = MagicMock(spec=['edit'])
        mock_get_repo.side_effect = ['his_repo', forked_repo]
        test = GithubReference(user='user', passwd='passwd', token='token')
        test._github = MagicMock(spec=['get_user'])
        get_user = MagicMock(spec=['create_fork'])
        get_user.create_fork.return_value = 'ret'
        test._github.get_user.return_value = get_user
        ### test ###
        self.assertEqual(forked_repo, test.fork_repo('user', 'name', 'newname'))

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.get_repo')
    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.exists_repo')
    @mock.patch('time.sleep')
    def test_fork_repo_v(self, mock_sleep, mock_exists_repo, mock_get_repo, mock_write):
        """fork_repo normal case with verbose"""
        ### setting ###
        mock_exists_repo.return_value = False
        forked_repo = MagicMock(spec=['edit'])
        mock_get_repo.side_effect = ['his_repo', forked_repo]
        test = GithubReference(user='user', passwd='passwd', token='token')
        test._github = MagicMock(spec=['get_user'])
        get_user = MagicMock(spec=['create_fork'])
        get_user.create_fork.return_value = 'ret'
        test._github.get_user.return_value = get_user
        ### test ###
        self.assertEqual(forked_repo, test.fork_repo('user', 'name', 'newname', verbose=True))
        self.assertEqual(2, mock_write.call_count)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.get_repo')
    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.exists_repo')
    @mock.patch('time.sleep')
    def test_fork_repo_except_v(self, mock_sleep, mock_exists_repo, mock_get_repo, mock_write):
        """fork_repo normal case with verbose
        cannot find repository
        """
        ### setting ###
        mock_exists_repo.return_value = False
        forked_repo = MagicMock(spec=['edit'])
        forked_repo.edit.side_effect = Exception()
        mock_get_repo.side_effect = ['his_repo', forked_repo]
        test = GithubReference(user='user', passwd='passwd', token='token')
        test._github = MagicMock(spec=['get_user'])
        get_user = MagicMock(spec=['create_fork'])
        get_user.create_fork.return_value = 'ret'
        test._github.get_user.return_value = get_user
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.RepositoryNotFoundException):
            test.fork_repo('user', 'name', 'newname', verbose=True)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.get_repo')
    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference.exists_repo')
    @mock.patch('time.sleep')
    def test_fork_repo_except(self, mock_sleep, mock_exists_repo, mock_get_repo, mock_write):
        """fork_repo except case
        exists_repo = True
        """
        ### setting ###
        mock_exists_repo.return_value = True
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.RepositoryAlreadyExistsException):
            self.test.fork_repo('user', 'name', 'newname', verbose=False)

    @mock.patch('builtins.open')
    @mock.patch('requests.get')
    def test_get_file_contents(self, mock_req_get, mock_open):
        """get_file_contents normal case"""
        ### setting ###
        response = MagicMock()
        type(response).status_code = PropertyMock(return_value=200)
        type(response).encoding = PropertyMock(return_value='')
        type(response).content = PropertyMock(return_value='content')
        mock_req_get.return_value = response
        mock_open(spec=['write'])
        ### test ###
        self.assertEqual(0, self.test.get_file_contents('repo_owner', 'repo_name', 'file'))

    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open')
    @mock.patch('requests.get')
    def test_get_file_contents_v(self, mock_req_get, mock_open, mock_write):
        """get_file_contents normal case with verbose"""
        ### setting ###
        response = MagicMock()
        type(response).status_code = PropertyMock(return_value=200)
        type(response).encoding = PropertyMock(return_value='')
        type(response).content = PropertyMock(return_value='content')
        mock_req_get.return_value = response
        mock_open(spec=['write'])
        ### test ###
        self.assertEqual(0, self.test.get_file_contents('repo_owner', 'repo_name', 'file', verbose=True))
        mock_write.assert_called_once()

    @mock.patch('builtins.open')
    @mock.patch('requests.get')
    def test_get_file_contents_error(self, mock_req_get, mock_open):
        """get_file_contents error case"""
        ### setting ###
        response = MagicMock()
        type(response).status_code = PropertyMock(return_value=199)
        type(response).encoding = PropertyMock(return_value='')
        type(response).content = PropertyMock(return_value='content')
        mock_req_get.return_value = response
        mock_open(spec=['write'])
        ### test ###
        self.assertEqual(-1, self.test.get_file_contents('repo_owner', 'repo_name', 'file'))


if __name__ == '__main__':
    unittest.main()
