# test for wasanbon/core/plugins/mgr/rtcprofile_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.mgr.rtcprofile_plugin import Plugin
import importlib
import copy

def mock_join_func( *args ):
    ret = ""
    for val in args:
        ret = ret + str(val) + '/'
    return ret.rstrip('/')

class TestPlugin(unittest.TestCase):

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.mgr.rtcprofile_plugin as m
        self.admin_mock = MagicMock(spec=['package', 'rtc', 'rtcprofile'])
        setattr(m, 'admin', self.admin_mock)
        self.mgr_mock = MagicMock(spec=['imaging'])
        setattr(m, 'mgr', self.mgr_mock)
        self.plugin = m.Plugin()

    def get_rtc(self):
        basicInfo = MagicMock()
        type(basicInfo).name = PropertyMock(return_value='test_name')
        type(basicInfo).description = PropertyMock(return_value='test_description')
        type(basicInfo).category = PropertyMock(return_value='test_category')
        type(basicInfo).vendor = PropertyMock(return_value='test_vendor')
        dataport = MagicMock()
        type(dataport).name = PropertyMock(return_value='dataport_name')
        type(dataport).portType = PropertyMock(return_value='dataport_porttype')
        type(dataport).type = PropertyMock(return_value='dataport_type')
        serviceInterface = MagicMock()
        type(serviceInterface).name = PropertyMock(return_value='serviceInterface_name')
        type(serviceInterface).type = PropertyMock(return_value='serviceInterface_type')
        type(serviceInterface).instanceName = PropertyMock(return_value='serviceInterface_instanceName')
        serviceport = MagicMock()
        type(serviceport).name = PropertyMock(return_value='serviceport_name')
        type(serviceport).serviceInterfaces = PropertyMock(return_value=[serviceInterface])
        language = MagicMock()
        type(language).kind = PropertyMock(return_value='language_kind')
        rtcprofile = MagicMock()
        type(rtcprofile).basicInfo = PropertyMock(return_value=basicInfo)
        type(rtcprofile).dataports = PropertyMock(return_value=[dataport])
        type(rtcprofile).serviceports = PropertyMock(return_value=[serviceport])
        type(rtcprofile).language = PropertyMock(return_value=language)
        rtc = MagicMock()
        type(rtc).rtcprofile = PropertyMock(return_value=rtcprofile)
        type(rtc).path = PropertyMock(return_value='path')
        return rtc

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment',
                          'admin.package',
                          'admin.rtc',
                          'mgr.repository',
                          'admin.rtcprofile',
                          'mgr.imaging',
                          'admin.repository'],
                         self.plugin.depends())

    @mock.patch('builtins.print')
    def test_print_rtcs(self, mock_print):
        """print_rtcs normal case"""
        ### set mock ###
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value='pack')
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = PropertyMock(return_value='rtc_name')
        type(self.admin_mock.rtc).get_rtcs_from_package = MagicMock(return_value=[rtc])
        ### test ###
        self.plugin._print_rtcs(['args'])
        mock_print.assert_any_call('rtc_name')

    @mock.patch('sys.stdout.write')
    def test_dump(self, mock_write):
        """dump normal case"""
        ### set mock ###
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value='pack')
        rtc = MagicMock()
        type(rtc).rtcprofile = PropertyMock(return_value='rtcprofile')
        type(self.admin_mock.rtc).get_rtcs_from_package = MagicMock(return_value=rtc)
        type(self.admin_mock.rtcprofile).tostring = MagicMock(return_value='test_dump')
        ### test ###
        self.assertEqual(0, self.plugin.dump(['0', '1', '2', '3']))
        mock_write.assert_any_call('test_dump')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_html_1(self, mock_write, mock_parse_args):
        """html flag error case"""

        args = ['./mgr.py', 'rtcprofile', 'html', 'all']
        options = MagicMock()
        type(options).image_flag = True
        type(options).save_flag = True
        type(options).css_name = 'test'
        type(options).doc_flag = False
        mock_parse_args.return_value = options, args

        type(self.admin_mock.package).get_package_from_path = MagicMock()

        ### test ###
        self.assertEqual(-1, self.plugin.html(args))
        mock_write.assert_any_call('# Error. -c option must be used with -d option\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.mgr.rtcprofile_plugin.Plugin.get_html')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    def test_html_2(self, mock_mkdir, mock_isdir, mock_open, mock_get_html, mock_write, mock_parse_args):
        """html all case"""

        args = ['./mgr.py', 'rtcprofile', 'html', 'all']
        options = MagicMock()
        type(options).image_flag = True
        type(options).save_flag = True
        type(options).css_name = 'test'
        type(options).doc_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.rtc).get_rtcs_from_package = MagicMock(return_value=[self.get_rtc()])
        type(self.admin_mock.rtc).get_rtc_from_package = MagicMock(self.get_rtc())

        mock_get_html.return_value = 'html'
        mock_isdir.return_value = False

        im = MagicMock()
        save = MagicMock()
        type(im).save = save
        type(self.mgr_mock.imaging).get_image = MagicMock(return_value=im)

        ### test ###
        self.assertEqual(0, self.plugin.html(args))
        mock_open.assert_called_once_with('package_path/test_name.html', 'w')
        mock_isdir.assert_called_once_with('package_path/image')
        mock_mkdir.assert_called_once_with('package_path/image')
        save.assert_called_once_with('package_path/image/test_name.png')
        mock_write.assert_any_call('# Saved HTML File to package_path/test_name.html\n')
        mock_write.assert_any_call('# Saved Image File to package_path/image\n')

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.mgr.rtcprofile_plugin.Plugin.get_html')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    def test_html_2(self, mock_mkdir, mock_isdir, mock_open, mock_get_html, mock_write, mock_parse_args, mock_join):
        """html rtc case"""

        args = ['./mgr.py', 'rtcprofile', 'html', 'rtc_name']
        options = MagicMock()
        type(options).image_flag = True
        type(options).save_flag = True
        type(options).css_name = None
        type(options).doc_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.rtc).get_rtc_from_package = MagicMock(return_value=self.get_rtc())

        mock_get_html.return_value = 'html'
        mock_isdir.return_value = False

        im = MagicMock()
        save = MagicMock()
        type(im).save = save
        type(self.mgr_mock.imaging).get_image = MagicMock(return_value=im)

        ### test ###
        self.assertEqual(0, self.plugin.html(args))
        mock_open.assert_called_once_with('package_path/rtc_name.html', 'w')
        mock_isdir.assert_called_once_with('package_path/image')
        mock_mkdir.assert_called_once_with('package_path/image')
        save.assert_called_once_with('package_path/image/test_name.png')
        mock_write.assert_any_call('# Saved HTML File to package_path/rtc_name.html\n')
        mock_write.assert_any_call('# Saved Image File to package_path/image\n')

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    def test_image(self, mock_mkdir, mock_isdir, mock_write, mock_parse_args, mock_join):
        """image normal case"""

        args = ['./mgr.py', 'rtcprofile', 'image', 'rtc_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)

        mock_isdir.return_value = False

        type(self.admin_mock.rtc).get_rtc_from_package = MagicMock(return_value=self.get_rtc())

        im = MagicMock()
        save = MagicMock()
        type(im).save = save
        type(self.mgr_mock.imaging).get_image = MagicMock(return_value=im)

        ### test ###
        self.assertEqual(0, self.plugin.image(args))
        mock_isdir.assert_called_once_with('package_path/image')
        mock_mkdir.assert_called_once_with('package_path/image')
        save.assert_called_once_with('package_path/image/test_name.png')
        mock_write.assert_any_call('# Saved Image File to package_path/image/test_name.png\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.exists')
    def test_cat_1(self, mock_exists, mock_write, mock_parse_args):
        """cat inputfile and not exists case"""

        args = ['./mgr.py', 'rtcprofile', 'cat', 'rtc_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).filename = 'RTC.xml'
        type(options).inputfile = 'inputfile'
        mock_parse_args.return_value = options, args

        type(self.admin_mock.package).get_package_from_path = MagicMock()
        type(self.admin_mock.rtc).get_rtc_from_package = MagicMock(return_value=self.get_rtc())

        mock_exists.return_value = False

        ### test ###
        self.assertEqual(-1, self.plugin.cat(args))
        mock_exists.assert_any_call('inputfile')
        mock_write.assert_any_call('## Input File is inputfile\n')
        mock_write.assert_any_call('## Input File Not Found.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.util.yes_no')
    @mock.patch('os.path.isfile')
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    def test_cat_2(self, mock_rename, mock_timestampstr, mock_isfile, mock_yes_no, mock_open, mock_write, mock_parse_args):
        """cat inputdata abort case"""

        args = ['./mgr.py', 'rtcprofile', 'cat', 'rtc_name', 'input_data']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).filename = 'RTC.xml'
        type(options).inputfile = None
        mock_parse_args.return_value = options, args

        type(self.admin_mock.package).get_package_from_path = MagicMock()
        type(self.admin_mock.rtc).get_rtc_from_package = MagicMock(return_value=self.get_rtc())

        mock_yes_no.side_effect = ['no']
        mock_isfile.retun_value = True

        ### test ###
        self.assertEqual(-1, self.plugin.cat(args))
        mock_write.assert_any_call('## Input Data is input_data\n')
        mock_write.assert_any_call('## Aborted.\n')

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.util.yes_no')
    @mock.patch('os.path.isfile')
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    def test_cat_3(self, mock_rename, mock_timestampstr, mock_isfile, mock_yes_no, mock_open, mock_write, mock_parse_args, mock_join):
        """cat inputdata normal case"""

        args = ['./mgr.py', 'rtcprofile', 'cat', 'rtc_name', 'input_data']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).filename = 'RTC.xml'
        type(options).inputfile = None
        mock_parse_args.return_value = options, args

        type(self.admin_mock.package).get_package_from_path = MagicMock()
        type(self.admin_mock.rtc).get_rtc_from_package = MagicMock(return_value=self.get_rtc())

        mock_yes_no.side_effect = ['yes']
        mock_isfile.retun_value = True

        ### test ###
        self.assertEqual(0, self.plugin.cat(args))
        mock_write.assert_any_call('## Input Data is input_data\n')
        mock_isfile.assert_called_once_with('path/RTC.xml')
        mock_rename.assert_called_once_with('path/RTC.xml', 'path/RTC.xml20211001000000')
        mock_open.assert_called_once_with('path/RTC.xml', 'w')
        mock_write.assert_any_call('## Success.\n')


if __name__ == '__main__':
    unittest.main()
