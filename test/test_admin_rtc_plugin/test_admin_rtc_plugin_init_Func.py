# test for wasanbon/core/plugins/admin/rtc_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.admin.rtc_plugin import *


class Test(unittest.TestCase):

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.RTCPackage')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    @mock.patch('os.listdir')
    def test_get_rtcs_from_package_1(self, mock_listdir, mock_join, mock_isdir, mock_RTCPackage):
        """get_rtcs_from_package normal case
        os.path.isdir = False
        """
        ### setting ###
        mock_listdir.return_value = ['rtc_dir']
        mock_isdir.return_value = False
        package = MagicMock()
        ### test ###
        self.assertEqual([], get_rtcs_from_package(package))
        self.assertEqual(0, mock_RTCPackage.call_count)

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.RTCPackage')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    @mock.patch('os.listdir')
    def test_get_rtcs_from_package_2(self, mock_listdir, mock_join, mock_isdir, mock_RTCPackage):
        """get_rtcs_from_package normal case
        os.path.isdir = True
        """
        ### setting ###
        mock_listdir.return_value = ['rtc_dir']
        mock_isdir.return_value = True
        package = MagicMock()
        mock_RTCPackage.return_value = 'rtc'
        ### test ###
        self.assertEqual(['rtc'], get_rtcs_from_package(package))
        self.assertEqual(1, mock_RTCPackage.call_count)

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.RTCPackage')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    @mock.patch('os.listdir')
    def test_get_rtcs_from_package_3(self, mock_listdir, mock_join, mock_isdir, mock_RTCPackage):
        """get_rtcs_from_package normal case
        os.path.isdir = True
        raise exception
        """
        ### setting ###
        mock_listdir.return_value = ['rtc_dir']
        mock_isdir.return_value = True
        package = MagicMock()
        import wasanbon
        mock_RTCPackage.side_effect = wasanbon.RTCProfileNotFoundException('')
        ### test ###
        self.assertEqual([], get_rtcs_from_package(package))
        self.assertEqual(1, mock_RTCPackage.call_count)

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    def test_find_rtc_srcs_python(self, mock_split, mock_search_file):
        """find_rtc_srcs normal case
        rtcp language.kind = 'Python'
        """
        ### setting ###
        mock_split.return_value = 'path', None
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'Python'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_search_file.side_effect = ['python_file']
        ### test ###
        self.assertEqual('python_file', find_rtc_srcs(rtcp))
        mock_search_file.assert_called_once_with('path', 'rtcp_name' + '.py')

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    def test_find_rtc_srcs_java(self, mock_split, mock_search_file):
        """find_rtc_srcs normal case
        rtcp language.kind = 'Java'
        """
        ### setting ###
        mock_split.return_value = 'path', None
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'Java'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_search_file.side_effect = ['java_file']
        ### test ###
        self.assertEqual('java_file', find_rtc_srcs(rtcp))
        mock_search_file.assert_called_once_with('path', 'rtcp_name' + 'Impl.java')

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    def test_find_rtc_srcs_cpp(self, mock_split, mock_search_file):
        """find_rtc_srcs normal case
        rtcp language.kind = 'C++'
        """
        ### setting ###
        mock_split.return_value = 'path', None
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'C++'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_search_file.side_effect = ['hdrs', 'srcs']
        ### test ###
        self.assertEqual('hdrs' + 'srcs', find_rtc_srcs(rtcp))
        mock_search_file.assert_has_calls([call('path', 'rtcp_name' + '.h'), call('path', 'rtcp_name' + '.cpp')])

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.path.split')
    def test_find_rtc_exec_cpp_1(self, mock_split, mock_platform, mock_search_file):
        """find_rtc_exec normal case
        rtcp language.kind = 'C++'
        sys.platform = 'win32'
        len(files) = 0
        """
        ### setting ###
        mock_split.return_value = 'path', None
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'C++'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_search_file.return_value = []
        ### test ###
        self.assertEqual('', find_rtc_exec(rtcp))
        mock_search_file.assert_called_once_with('path', 'rtcp_nameComp.exe')

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux or darwin'))
    @mock.patch('os.path.split')
    def test_find_rtc_exec_cpp_2(self, mock_split, mock_platform, mock_search_file):
        """find_rtc_exec normal case
        rtcp language.kind = 'C++'
        sys.platform != 'win32'
        len(files) != 0
        """
        ### setting ###
        mock_split.return_value = 'path', None
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'C++'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_search_file.return_value = ['hoge', 'hogehoge']
        ### test ###
        self.assertEqual('hoge', find_rtc_exec(rtcp))
        mock_search_file.assert_called_once_with('path', 'rtcp_nameComp')

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.find_rtc_bin', return_value='test')
    def test_find_rtc_exec_python(self, mock_find_rtc_bin):
        """find_rtc_exec normal case
        rtcp language.kind = 'Python'
        """
        ### setting ###
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp.language).kind = 'Python'
        ### test ###
        self.assertEqual('test', find_rtc_exec(rtcp))

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.find_rtc_bin', return_value='test')
    def test_find_rtc_exec_java(self, mock_find_rtc_bin):
        """find_rtc_exec normal case
        rtcp language.kind = 'Java'
        """
        ### setting ###
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp.language).kind = 'Java'
        ### test ###
        self.assertEqual('test', find_rtc_exec(rtcp))

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    def test_get_rtc_bin_filename_cpp_win32(self, mock_platform):
        """get_rtc_bin_filename normal case
        rtcp language.kind = 'C++'
        """
        ### setting ###
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'C++'
        type(rtcp.basicInfo).name = 'rtcp_name'
        ### test ###
        self.assertEqual('rtcp_name.dll', get_rtc_bin_filename(rtcp))

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    def test_get_rtc_bin_filename_cpp_linux(self, mock_platform):
        """get_rtc_bin_filename normal case
        rtcp language.kind = 'C++'
        """
        ### setting ###
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'C++'
        type(rtcp.basicInfo).name = 'rtcp_name'
        ### test ###
        self.assertEqual('rtcp_name.so', get_rtc_bin_filename(rtcp))

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    def test_get_rtc_bin_filename_cpp_darwin(self, mock_platform):
        """get_rtc_bin_filename normal case
        rtcp language.kind = 'C++'
        """
        ### setting ###
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'C++'
        type(rtcp.basicInfo).name = 'rtcp_name'
        ### test ###
        self.assertEqual('rtcp_name.dylib', get_rtc_bin_filename(rtcp))

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='hoge'))
    def test_get_rtc_bin_filename_cpp_unspport(self, mock_platform):
        """get_rtc_bin_filename normal case
        rtcp language.kind = 'C++'
        """
        ### setting ###
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'C++'
        type(rtcp.basicInfo).name = 'rtcp_name'
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.UnsupportedPlatformException):
            self.assertEqual(None, get_rtc_bin_filename(rtcp))

    def test_get_rtc_bin_filename_python(self):
        """get_rtc_bin_filename normal case
        rtcp language.kind = 'Python'
        """
        ### setting ###
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'Python'
        type(rtcp.basicInfo).name = 'rtcp_name'
        ### test ###
        self.assertEqual('rtcp_name.py', get_rtc_bin_filename(rtcp))

    def test_get_rtc_bin_filename_java(self):
        """get_rtc_bin_filename normal case
        rtcp language.kind = 'Java'
        """
        ### setting ###
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'Java'
        type(rtcp.basicInfo).name = 'rtcp_name'
        ### test ###
        self.assertEqual('rtcp_name.jar', get_rtc_bin_filename(rtcp))

    def test_get_rtc_bin_filename_exception(self):
        """get_rtc_bin_filename normal case
        rtcp language.kind = 'hoge'
        """
        ### setting ###
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'hoge'
        type(rtcp.basicInfo).name = 'rtcp_name'
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.InvalidRTCProfileException):
            self.assertEqual(None, get_rtc_bin_filename(rtcp))

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.get_rtc_bin_filename', return_value='rtc_file_name_list')
    def test_find_rtc_bin_1(self, mock_rtc_bin_filename, mock_split, mock_search_file):
        """find_rtc_bin normal case
        util.search_file raise OSError
        """
        ### setting ###
        rtcp = MagicMock()
        type(rtcp).filename = 'filename'
        mock_split.return_value = 'path', None
        mock_search_file.side_value = OSError('')
        ### test ###
        self.assertEqual('', find_rtc_bin(rtcp))

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.get_rtc_bin_filename', return_value='rtc_file_name_list')
    def test_find_rtc_bin_2(self, mock_rtc_bin_filename, mock_split, mock_search_file, mock_write):
        """find_rtc_bin normal case
        file.count > 0
        """
        ### setting ###
        rtcp = MagicMock()
        type(rtcp).filename = 'filename'
        mock_split.return_value = 'path', None
        rtcs_file = MagicMock(spec=['count'])
        rtcs_file.count.return_value = 1
        mock_search_file.return_value = [rtcs_file]
        ### test ###
        self.assertEqual('', find_rtc_bin(rtcp))
        self.assertEqual(2, mock_write.call_count)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.get_rtc_bin_filename', return_value='rtc_file_name_list')
    def test_find_rtc_bin_3(self, mock_rtc_bin_filename, mock_split, mock_search_file, mock_write):
        """find_rtc_bin normal case
        file.count = 0
        """
        ### setting ###
        rtcp = MagicMock()
        type(rtcp).filename = 'filename'
        mock_split.return_value = 'path', None
        rtcs_file = MagicMock(spec=['count'])
        rtcs_file.count.return_value = 0
        mock_search_file.return_value = [rtcs_file]
        ### test ###
        self.assertEqual(rtcs_file, find_rtc_bin(rtcp))
        self.assertEqual(0, mock_write.call_count)

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.on_multiple_rtcfile', return_value='test')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.get_rtc_bin_filename', return_value='rtc_file_name_list')
    def test_find_rtc_bin_3(self, mock_rtc_bin_filename, mock_split, mock_search_file, mock_write, mock_on_multiple_rtcfile):
        """find_rtc_bin normal case
        file.count = 0
        """
        ### setting ###
        rtcp = MagicMock()
        type(rtcp).filename = 'filename'
        mock_split.return_value = 'path', None
        rtcs_file = MagicMock(spec=['count'])
        rtcs_file.count.return_value = 0
        mock_search_file.return_value = [rtcs_file, rtcs_file]
        ### test ###
        self.assertEqual('test', find_rtc_bin(rtcp))
        self.assertEqual(0, mock_write.call_count)

    @mock.patch('builtins.print')
    def test_on_multiple_rtcfile(self, mock_print):
        """on_multiple_rtcfile normal case"""
        ### setting ###
        ### test ###
        self.assertEqual('test', on_multiple_rtcfile(['test']))

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    def test_find_rtc_conf_1(self, mock_split, mock_search_file):
        """find_rtc_conf normal case
        mock_search_file raise OSError
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_split.return_value = 'path', None
        mock_search_file.side_effect = OSError('')
        ### test ###
        self.assertEqual('', find_rtc_conf(rtcp))

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    def test_find_rtc_conf_2(self, mock_split, mock_search_file):
        """find_rtc_conf normal case
        len(conf_files) == 1
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_split.return_value = 'path', None
        mock_search_file.return_value = ['test']
        ### test ###
        self.assertEqual('test', find_rtc_conf(rtcp))

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    def test_find_rtc_conf_3(self, mock_split, mock_search_file):
        """find_rtc_conf normal case
        len(conf_files) == 0
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_split.return_value = 'path', None
        mock_search_file.return_value = []
        ### test ###
        self.assertEqual('', find_rtc_conf(rtcp))

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.on_multiple_conffile', return_value='test')
    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    def test_find_rtc_conf_4(self, mock_split, mock_search_file, mock_on_multiple_conffile):
        """find_rtc_conf normal case
        len(conf_files) > 1
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_split.return_value = 'path', None
        mock_search_file.return_value = ['hoge', 'hoge']
        ### test ###
        self.assertEqual('test', find_rtc_conf(rtcp))

    @mock.patch('builtins.print')
    def test_on_multiple_conffile(self, mock_print):
        """on_multiple_rtcfile normal case"""
        ### setting ###
        ### test ###
        self.assertEqual('test', on_multiple_conffile(['test']))


if __name__ == '__main__':
    unittest.main()
