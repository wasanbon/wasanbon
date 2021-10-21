# test for wasanbon/core/plugins/admin/rtc_plugin/__init__.py RTCPackage

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.admin.rtc_plugin import RTCPackage


class TestRTCPackage(unittest.TestCase):

    @mock.patch('os.path.isfile')
    @mock.patch('os.path.join')
    def setUp(self, mock_join, mock_isfile):
        ### setting ###
        import wasanbon.core.plugins.admin.rtc_plugin as m
        self.admin_mock = MagicMock(spec=['rtcprofile'])
        setattr(m, 'admin', self.admin_mock)
        mock_join.return_value = 'rtcprofile_path'
        mock_isfile.return_value = True
        self.test = RTCPackage('path')

    @mock.patch('os.path.isfile')
    @mock.patch('os.path.join')
    def test_init_1(self, mock_join, mock_isfile):
        """__init__ normal case
        isfile = True
        """
        ### setting ###
        mock_join.return_value = 'rtcprofile_path'
        mock_isfile.return_value = True
        ### test ###
        test = RTCPackage('path')
        self.assertEqual('path', test._path)
        self.assertEqual('rtcprofile_path', test._rtcprofile_path)

    @mock.patch('os.path.isfile')
    @mock.patch('os.path.join')
    def test_init_2(self, mock_join, mock_isfile):
        """__init__ normal case
        isfile = False
        """
        ### setting ###
        mock_join.return_value = 'rtcprofile_path'
        mock_isfile.return_value = False
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.RTCProfileNotFoundException):
            test = RTCPackage('path')
            self.assertEqual('path', test._path)
            self.assertEqual('rtcprofile_path', test._rtcprofile_path)

    def test_path(self):
        """path normal case"""
        self.assertEqual('path', self.test.path)

    def test_rtcprofile(self):
        """rtcprofile normal case"""
        ### setting ###
        rtcprofile = MagicMock(spec=['RTCProfile'])
        rtcprofile.RTCProfile.return_value = 'test_rtcprofile'
        type(self.admin_mock.rtcprofile).rtcprofile = PropertyMock(return_value=rtcprofile)
        ### test ###
        self.assertEqual('test_rtcprofile', self.test.rtcprofile)
        self.assertEqual(1, rtcprofile.RTCProfile.call_count)
        self.assertEqual('test_rtcprofile', self.test.rtcprofile)
        self.assertEqual(1, rtcprofile.RTCProfile.call_count)

    def test_get_rtc_profile_path(self):
        """get_rtc_profile_path normal case"""
        self.assertEqual('rtcprofile_path', self.test.get_rtc_profile_path())

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.find_rtc_bin', return_value='test')
    def test_get_rtc_file_path(self, mock_find_rtc_bin):
        """get_rtc_file_path normal case"""
        self.assertEqual('test', self.test.get_rtc_file_path())

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.find_rtc_exec', return_value='test')
    def test_get_rtc_executable_file_path(self, mock_find_rtc_exec):
        """get_rtc_executable_file_path normal case"""
        self.assertEqual('test', self.test.get_rtc_executable_file_path())

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.find_rtc_conf', return_value='test')
    def test_get_rtc_conf_path(self, mock_find_rtc_conf):
        """get_rtc_conf_path normal case"""
        self.assertEqual('test', self.test.get_rtc_conf_path())


if __name__ == '__main__':
    unittest.main()
