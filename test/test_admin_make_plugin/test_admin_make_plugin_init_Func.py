# test for wasanbon/core/plugins/admin/make_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.admin.make_plugin import isparent


class Test(unittest.TestCase):

    @mock.patch('os.getcwd')
    def test_isparent_1(self, mock_getcwd):
        """isparent normal case
        q='/'
        """
        ### setting ###
        mock_getcwd.return_value = '/'
        ### test ###
        self.assertEqual(False, isparent('path'))

    @mock.patch('os.getcwd')
    @mock.patch('os.stat')
    @mock.patch('sys.stdout.write')
    def test_isparent_2(self, mock_write, mock_stat, mock_getcwd):
        """isparent normal case
        verbose=False
        os.stat=os.stat
        """
        ### setting ###
        mock_getcwd.return_value = 'path'
        mock_stat.side_effect = [1, 1]
        ### test ###
        self.assertEqual(True, isparent('path'))

    @mock.patch('os.getcwd')
    @mock.patch('os.path.dirname')
    @mock.patch('os.stat')
    @mock.patch('sys.stdout.write')
    def test_isparent_3(self, mock_write, mock_stat, mock_dirname, mock_getcwd):
        """isparent normal case
        verbose = True
        os.stat != os.stat
        q == parent
        """
        ### setting ###
        mock_getcwd.return_value = 'path'
        mock_stat.side_effect = [1, 0]
        mock_dirname.return_value = 'path'
        ### test ###
        self.assertEqual(False, isparent('path', verbose=True))
        mock_write.assert_called_once()

    @mock.patch('os.getcwd')
    @mock.patch('os.path.dirname')
    @mock.patch('os.stat')
    @mock.patch('sys.stdout.write')
    def test_isparent_4(self, mock_write, mock_stat, mock_dirname, mock_getcwd):
        """isparent normal case
        verbose = True
        os.stat != os.stat
        q != parent
        """
        ### setting ###
        mock_getcwd.return_value = 'path'
        mock_stat.side_effect = [1, 0, 1, 1]
        mock_dirname.return_value = 'parent'
        ### test ###
        self.assertEqual(True, isparent('parent', verbose=True))
        self.assertEqual(2, mock_write.call_count)


if __name__ == '__main__':
    unittest.main()
