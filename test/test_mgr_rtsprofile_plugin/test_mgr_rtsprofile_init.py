# test for wasanbon/core/plugins/mgr/admin_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import time
import threading

import sys
sys.path.append('../../')

import wasanbon


class TestPlugin(unittest.TestCase):

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.mgr.rtsprofile_plugin as m
        self.admin_mock = MagicMock(spec=['package', 'rtc'])
        self.mgr_mock = MagicMock(spec=['imaging'])
        setattr(m, 'admin', self.admin_mock)
        setattr(m, 'mgr', self.mgr_mock)
        self.plugin = m.Plugin()
        self.func = m

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.mgr.rtsprofile_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.package', 'admin.rtc', 'mgr.imaging'], self.plugin.depends())

    @mock.patch('sys.stdout.write')
    @mock.patch('os.listdir', return_value=['DefaultSystem.xml', 'noxml'])
    def test_print_system_profiles(self, mock_listdir, mock_write):
        """print_system_profiles normal case"""

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        args = []
        self.plugin._print_system_profiles(args)
        mock_listdir.assert_called_once_with('./system')
        mock_write.assert_called_once_with('DefaultSystem.xml\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile')
    @mock.patch('builtins.print')
    def test_dump_1(self, mock_print, mock_isfile, mock_write, mock_parse_args):
        """dump file not found case"""

        args = ['./mgr.py', 'system', 'dump']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = "systemfile"
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).default_system_filepath = 'default_system_filepath'
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        mock_isfile.return_value = False

        ### test ###
        self.assertEqual(-1, self.plugin.dump(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_called_once_with('./system/systemfile')
        mock_print.assert_called_once_with('# File Not Found.')
        mock_write.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('builtins.print')
    @mock.patch('builtins.open', return_value=['open_line_data'])
    def test_dump_2(self, mock_open, mock_print, mock_isfile, mock_write, mock_parse_args):
        """dump file not found case"""

        args = ['./mgr.py', 'system', 'dump']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = None
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).default_system_filepath = 'default_system_filepath'
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.dump(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_called_once_with('default_system_filepath')
        mock_print.assert_not_called()
        mock_open.assert_called_once_with('default_system_filepath', 'r')
        mock_write.assert_called_once_with('open_line_data')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('builtins.print')
    @mock.patch('builtins.open', return_value=['open_line_data'])
    @mock.patch('wasanbon.util.yes_no', side_effect=['no'])
    def test_cat_1(self, mock_yes_no, mock_open, mock_print, mock_isfile, mock_write, mock_parse_args):
        """cat abort case"""

        args = ['./mgr.py', 'system', 'cat', 'input_data']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = 'systemfile'
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).default_system_filepath = 'default_system_filepath'
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.cat(args))
        mock_write.assert_any_call('## Input Data is input_data\n')
        get_package_from_path.assert_called_once()
        mock_yes_no.assert_called_once_with('## Write Input Data to ./system/systemfile?')
        mock_write.assert_any_call('## Aborted.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('builtins.print')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.util.yes_no', side_effect=['yes'])
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    def test_cat_2(self, mock_rename, mock_timestampstr, mock_yes_no, mock_open, mock_print, mock_isfile, mock_write, mock_parse_args):
        """cat success case"""

        args = ['./mgr.py', 'system', 'cat', 'input_data']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = None
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).default_system_filepath = 'default_system_filepath'
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.cat(args))
        mock_write.assert_any_call('## Input Data is input_data\n')
        get_package_from_path.assert_called_once()
        mock_yes_no.assert_called_once_with('## Write Input Data to default_system_filepath?')
        mock_rename.assert_called_once_with('default_system_filepath', 'default_system_filepath20211001000000')
        mock_open.assert_called_once_with('default_system_filepath', 'w')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=False)
    def test_copy_1(self, mock_isfile, mock_write, mock_parse_args):
        """copy file not founded case"""

        args = ['./mgr.py', 'system', 'copy', 'src_file_name', 'dest_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(-1, self.plugin.copy(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_called_once_with('./system/src_file_name')
        mock_write.assert_any_call('## No System File exists.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.util.no_yes', side_effect=['no'])
    def test_copy_2(self, mock_no_yes, mock_isfile, mock_write, mock_parse_args):
        """copy abort case"""

        args = ['./mgr.py', 'system', 'copy', 'src_file_name', 'dest_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.copy(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_has_calls([call('./system/src_file_name'), call('./system/dest_file_name')])
        mock_no_yes.assert_called_once_with('# Overwrite? (./system/dest_file_name):')
        mock_write.assert_any_call('## Aborted.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.util.no_yes', side_effect=['yes'])
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    @mock.patch('shutil.copyfile')
    def test_copy_3(self, mock_copyfile, mock_rename, mock_timestampstr, mock_no_yes, mock_isfile, mock_write, mock_parse_args):
        """copy normal case"""

        args = ['./mgr.py', 'system', 'copy', 'src_file_name', 'dest_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.copy(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_has_calls([call('./system/src_file_name'), call('./system/dest_file_name')])
        mock_no_yes.assert_called_once_with('# Overwrite? (./system/dest_file_name):')
        mock_rename.assert_called_once_with('./system/dest_file_name', './system/dest_file_name20211001000000')
        mock_copyfile.assert_called_once_with('./system/src_file_name', './system/dest_file_name')
        mock_write.assert_any_call('## Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=False)
    def test_delete_1(self, mock_isfile, mock_write, mock_parse_args):
        """delete file not founded case"""

        args = ['./mgr.py', 'system', 'delete', 'src_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(-1, self.plugin.delete(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_called_once_with('./system/src_file_name')
        mock_write.assert_any_call('## No System File exists.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.util.no_yes', side_effect=['no'])
    def test_delete_2(self, mock_no_yes, mock_isfile, mock_write, mock_parse_args):
        """delete abort case"""

        args = ['./mgr.py', 'system', 'delete', 'src_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.delete(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_has_calls([call('./system/src_file_name')])
        mock_no_yes.assert_called_once_with('# Delete? (./system/src_file_name):')
        mock_write.assert_any_call('## Aborted.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.util.no_yes', side_effect=['yes'])
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    def test_delete_3(self, mock_rename, mock_timestampstr, mock_no_yes, mock_isfile, mock_write, mock_parse_args):
        """delete normal case"""

        args = ['./mgr.py', 'system', 'delete', 'src_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.delete(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_has_calls([call('./system/src_file_name')])
        mock_no_yes.assert_called_once_with('# Delete? (./system/src_file_name):')
        mock_rename.assert_called_once_with('./system/src_file_name', './system/src_file_name20211001000000')
        mock_write.assert_any_call('## Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=False)
    def test_image_1(self, mock_isfile, mock_write, mock_parse_args):
        """image file not founded case"""

        args = ['./mgr.py', 'system', 'image', 'src_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(-1, self.plugin.image(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_called_once_with('./system/src_file_name')
        mock_write.assert_any_call('## No System File exists.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('os.path.isdir', return_value=False)
    @mock.patch('os.mkdir')
    @mock.patch('wasanbon.util.no_yes', side_effect=['yes'])
    @mock.patch('rtsprofile.rts_profile.RtsProfile')
    @mock.patch('builtins.open')
    def test_image_2(self, mock_open, mock_RtsProfile, mock_no_yes, mock_mkdir, mock_isdir, mock_isfile, mock_write, mock_parse_args):
        """image normal case"""

        args = ['./mgr.py', 'system', 'image', 'src_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        type(package).path = './package_path'
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtsp = None
        mock_RtsProfile.return_value = rtsp

        im = MagicMock()
        save = MagicMock()
        type(im).save = save
        get_rtsp_image = MagicMock(return_value=im)
        type(self.mgr_mock.imaging).get_rtsp_image = get_rtsp_image

        ### test ###
        self.assertEqual(0, self.plugin.image(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_has_calls([call('./system/src_file_name')])
        mock_isdir.assert_called_once_with('./package_path/image')
        mock_mkdir.assert_called_once_with('./package_path/image')
        mock_open.assert_called_once_with('./system/src_file_name', 'r')
        mock_RtsProfile.assert_called_once()
        get_rtsp_image.assert_called_once_with(package, rtsp, port_height=10, port_text_font=10, verbose=True)
        save.assert_called_once_with('./package_path/image/src_file_name.png')
        mock_write.assert_any_call('# Saved Image File to ./package_path/image/src_file_name.png\n')


if __name__ == '__main__':
    unittest.main()
