# test for wasanbon/core/plugins/admin/systemlauncher_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.admin.systemlauncher_plugin import start_rtcd


class Test(unittest.TestCase):

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_python_rtcd', return_value='python')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_java_rtcd', return_value='java')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_cpp_rtcd', return_value='cpp')
    def test_start_rtcd_1(self, mock_start_cpp_rtcd, mock_start_java_rtcd, mock_start_python_rtcd):
        """start_rtcd normal case
        language = 'C++'
        """
        ### test ###
        self.assertEqual('cpp', start_rtcd('pkg', 'C++', 'filepath'))

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_python_rtcd', return_value='python')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_java_rtcd', return_value='java')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_cpp_rtcd', return_value='cpp')
    def test_start_rtcd_2(self, mock_start_cpp_rtcd, mock_start_java_rtcd, mock_start_python_rtcd):
        """start_rtcd normal case
        language = 'Java'
        """
        ### setting ###
        import wasanbon.core.plugins.admin.systemlauncher_plugin as m
        admin_mock = MagicMock(spec=['rtc', 'environment'])
        setattr(m, 'admin', admin_mock)
        ### test ###
        self.assertEqual('java', start_rtcd('pkg', 'Java', 'filepath'))

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_python_rtcd', return_value='python')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_java_rtcd', return_value='java')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_cpp_rtcd', return_value='cpp')
    def test_start_rtcd_3(self, mock_start_cpp_rtcd, mock_start_java_rtcd, mock_start_python_rtcd):
        """start_rtcd normal case
        language = 'Python'
        """
        ### test ###
        self.assertEqual('python', start_rtcd('pkg', 'Python', 'filepath'))

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_python_rtcd', return_value='python')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_java_rtcd', return_value='java')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.run.start_cpp_rtcd', return_value='cpp')
    def test_start_rtcd_4(self, mock_start_cpp_rtcd, mock_start_java_rtcd, mock_start_python_rtcd):
        """start_rtcd normal case
        language = 'hoge'
        """
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.UnsupportedPlatformException):
            start_rtcd('pkg', 'hoge', 'filepath')


if __name__ == '__main__':
    unittest.main()
