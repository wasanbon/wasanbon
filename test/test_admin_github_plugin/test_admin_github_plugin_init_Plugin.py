# test for wasanbon/core/plugins/admin/github_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.admin.github_plugin import Plugin


class TestPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = Plugin()

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment'], self.plugin.depends())

    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubReference')
    def test_Github(self, mock_GithubReference):
        """Github normal case"""
        mock_GithubReference.return_value = 'test'
        self.assertEqual('test', self.plugin.Github())
        mock_GithubReference.assert_called_once()

    @mock.patch('wasanbon.core.plugins.admin.github_plugin.GithubRepository')
    def test_Repository(self, mock_GithubRepository):
        """Repository normal case"""
        mock_GithubRepository.return_value = 'test'
        self.assertEqual('test', self.plugin.Repository('url', 'user', 'passwd', 'token'))
        mock_GithubRepository.assert_called_once()


if __name__ == '__main__':
    unittest.main()
