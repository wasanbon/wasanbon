# test for wasanbon/utils/__init__.py

import unittest
from unittest import mock
from unittest.mock import call, Mock

import os

from wasanbon import util


class TestPlugin(unittest.TestCase):

    @mock.patch('builtins.input')
    @mock.patch('sys.stdout.write')
    def test_choice(self, sys_stdout_write, input_mock):
        """test for choice"""
        # mock settings
        input_mock.side_effect = ('a', 0, 1)  # ValueError, RangeError, Quit
        test_alts = ['test1']
        test_callback = Mock()
        test_callback.callback.return_value = ['ans1', []]
        test_msg = 'test_msg'
        util.choice(test_alts, test_callback, test_msg)
        sys_calls = [
            call(test_msg),
            call('\n'),
            call(' - %s:%s\n' % (1, test_alts[0])),
            call(' - %s:%s\n' % (2, 'Quit(Q)')),
            call(' - ValueError.\n'),
            call(test_msg),
            call('\n'),
            call(' - %s:%s\n' % (1, test_alts[0])),
            call(' - %s:%s\n' % (2, 'Quit(Q)')),
            call(' - RangeError.\n'),
            call(test_msg),
            call('\n'),
            call(' - %s:%s\n' % (1, test_alts[0])),
            call(' - %s:%s\n' % (2, 'Quit(Q)')),
            call(' - Quit.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('builtins.input')
    @mock.patch('sys.stdout.write')
    def test_yes_no(self, sys_stdout_write, input_mock):
        """test for yes_no"""
        # test(len = 0)
        input_mock.return_value = ''
        test_msg = 'test_msg'
        ret = util.yes_no(test_msg)
        self.assertEqual(ret, 'yes')
        # test(y)
        input_mock.return_value = 'y'
        test_msg = 'test_msg'
        ret = util.yes_no(test_msg)
        self.assertEqual(ret, 'yes')
        # test(else)
        input_mock.return_value = 'aaa'
        test_msg = 'test_msg'
        ret = util.yes_no(test_msg)
        self.assertEqual(ret, 'no')
        sys_stdout_write.assert_has_calls([call('%s (Y/n)' % test_msg)])

    @mock.patch('builtins.input')
    @mock.patch('sys.stdout.write')
    def test_no_yes(self, sys_stdout_write, input_mock):
        """test for no_yes"""
        # test(len = 0)
        input_mock.return_value = ''
        test_msg = 'test_msg'
        ret = util.no_yes(test_msg)
        self.assertEqual(ret, 'no')
        # test(y)
        input_mock.return_value = 'y'
        test_msg = 'test_msg'
        ret = util.no_yes(test_msg)
        self.assertEqual(ret, 'yes')
        # test(else)
        input_mock.return_value = 'aaa'
        test_msg = 'test_msg'
        ret = util.no_yes(test_msg)
        self.assertEqual(ret, 'no')
        sys_stdout_write.assert_has_calls([call('%s (y/N)' % test_msg)])

    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    def test_search_file_not_list_no_subdir(self, isdir_mock, listdir_mock):
        """test for search_file filename is not list, no subdirectories"""
        # mock settings
        test_files = 'test1'
        listdir_mock.return_value = [test_files]
        isdir_mock.return_value = False
        # test
        test_rootdir = 'test_dir'
        test_filename = 'test1'
        ret = util.search_file(test_rootdir, test_filename)
        expected_ret = [os.path.join(test_rootdir, test_filename)]
        self.assertEqual(ret, expected_ret)

    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    def test_search_file_not_list_subdir(self, isdir_mock, listdir_mock):
        """test for search_file filename is not list, with subdirectories"""
        # mock settings
        test_files = 'test1'
        listdir_mock.return_value = [test_files]
        isdir_mock.side_effect = (True, False)
        # test
        test_rootdir = 'test_dir'
        test_filename = 'test1'
        ret = util.search_file(test_rootdir, test_filename)
        expected_ret = [os.path.join(test_rootdir, test_files, test_filename)]
        self.assertEqual(ret, expected_ret)

    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    def test_search_file_list(self, isdir_mock, listdir_mock):
        """test for search_file filename is list, no subdirectory"""
        # mock settings
        test_files = 'test1'
        listdir_mock.return_value = [test_files]
        isdir_mock.return_value = False
        # test
        test_rootdir = 'test_dir'
        test_filename = ['test1']
        ret = util.search_file(test_rootdir, test_filename)
        expected_ret = [os.path.join(test_rootdir, test_filename[0])]
        self.assertEqual(ret, expected_ret)


if __name__ == '__main__':
    unittest.main()
