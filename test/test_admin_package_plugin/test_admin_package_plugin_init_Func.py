# test for wasanbon/core/plugins/admin/rtcprofile_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

import wasanbon


class TestPlugin(unittest.TestCase):

    class TestClass():
        def __len__(self):
            return 1

        def __getitem__(self, i):
            if i < 0 or self.__len__() <= i:
                raise IndexError
            return b'key1, key2'

        def close(self):
            return

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.admin.package_plugin as m
        self.admin_mock = MagicMock(spec=['rtcconf'])
        setattr(m, 'admin', self.admin_mock)
        self.test = m

    @mock.patch('builtins.open')
    def test_parse_and_copy(self, mock_open):
        """parse_and_copy normal case"""

        fin = self.TestClass()
        fout = MagicMock()
        write = MagicMock()
        type(fout).write = write

        mock_open.side_effect = [fin, fout]

        ### test ###
        self.test.parse_and_copy('src_path', 'dist_path', {'key1': 'new1'})
        write.assert_called_once_with(b'new1, key2')

    @mock.patch('os.path.isfile', return_value=False)
    @mock.patch('builtins.open')
    @mock.patch('sys.stdout.write')
    def test_load_workspace_1(self, mock_write, mock_open, mock_isfile):
        """load_workspace not file case"""

        ### test ###
        wasanbon.home_path = '~/.wasanbon'
        self.test.load_workspace(True)
        mock_write.assert_any_call(' - Can not find workspace.yaml: ~/.wasanbon/workspace.yaml\n')
        mock_open.assert_called_once_with('~/.wasanbon/workspace.yaml', 'w')

    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load', return_value='load_result')
    @mock.patch('sys.stdout.write')
    def test_load_workspace_2(self, mock_write, mock_safe_load, mock_open, mock_isfile):
        """load_workspace exists file case"""

        ### test ###
        wasanbon.home_path = '~/.wasanbon'
        self.assertEqual('load_result', self.test.load_workspace(True))
        mock_open.assert_called_once_with('~/.wasanbon/workspace.yaml', 'r')

    @mock.patch('builtins.open')
    @mock.patch('yaml.dump')
    @mock.patch('sys.stdout.write')
    def test_save_workspace_1(self, mock_write, mock_dump, mock_open):
        """save_workspace not file case"""

        ### test ###
        wasanbon.home_path = '~/.wasanbon'
        self.test.save_workspace('dict')
        mock_open.assert_called_once_with('~/.wasanbon/workspace.yaml', 'w')

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_packages')
    @mock.patch('os.getcwd', return_value='.')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('sys.stdout.write')
    def test_create_package_2(self, mock_write, mock_isdir, mock_getcwd, mock_get_packages):
        """create_package same package case"""

        prj = MagicMock()
        type(prj).name = 'test_project01'
        mock_get_packages.return_value = [prj]

        ### test ###
        with self.assertRaises(wasanbon.DirectoryAlreadyExistsException):
            self.test.create_package('test_project02', verbose=True)
        mock_write.assert_any_call(' - There seems to be test_project02 here. Please change application name.\n')
        mock_isdir.assert_called_once_with('./test_project02')

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_packages')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.parse_and_copy')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.register_package')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    @mock.patch('os.getcwd', return_value='.')
    @mock.patch('os.path.isdir', return_value=False)
    @mock.patch('os.path.isfile', return_value=False)
    @mock.patch('os.mkdir')
    @mock.patch('os.walk', return_value=[('wasanbon/temlate', ['dir'], ['file'])])
    @mock.patch('subprocess.call')
    @mock.patch('sys.stdout.write')
    def test_create_package_3(self, mock_write, mock_call, mock_walk, mock_mkdir, mock_isfile, mock_isdir, mock_getcwd, mock_platform, mock_register_package, mock_parse_and_copy, mock_get_packages):
        """create_package normal case"""

        prj = MagicMock()
        type(prj).name = 'test_project01'
        mock_get_packages.return_value = [prj]

        ### test ###
        self.assertEqual(0, self.test.create_package('test_project02', verbose=True))
        mock_parse_and_copy.assert_called_once_with('wasanbon/temlate/file', './test_project02/file', {'$APP': 'test_project02'})
        mock_call.assert_called_once_with(['chmod', '755', 'test_project02/mgr.py'])
        mock_register_package.assert_called_once_with('test_project02', './test_project02')

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_packages')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.parse_and_copy')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.register_package')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.getcwd', return_value='.')
    @mock.patch('os.path.isdir', return_value=False)
    @mock.patch('os.path.isfile', return_value=False)
    @mock.patch('os.mkdir')
    @mock.patch('os.walk', return_value=[('wasanbon/temlate', ['dir'], ['file'])])
    @mock.patch('subprocess.call')
    @mock.patch('sys.stdout.write')
    def test_create_package_4(self, mock_write, mock_call, mock_walk, mock_mkdir, mock_isfile, mock_isdir, mock_getcwd, mock_platform, mock_register_package, mock_parse_and_copy, mock_get_packages):
        """create_package win32 normal case"""

        prj = MagicMock()
        type(prj).name = 'test_project01'
        mock_get_packages.return_value = [prj]

        ### test ###
        self.assertEqual(0, self.test.create_package('test_project02', verbose=True))
        mock_parse_and_copy.assert_called_once_with('wasanbon/temlate/file', './test_project02/file', {'$APP': 'test_project02'})
        mock_call.assert_not_called()
        mock_register_package.assert_called_once_with('test_project02', './test_project02')

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.load_workspace')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.save_workspace')
    def test_register_package(self, mock_save_workspace, mock_load_workspace):
        """register_package normal class"""

        mock_load_workspace.return_value = {'test_project01': '/path/to/test_project01'}

        ### test ###
        self.assertEqual(0, self.test.register_package('test_project02', '/path/to/test_project02'))
        mock_save_workspace.assert_called_once_with({'test_project01': '/path/to/test_project01', 'test_project02': '/path/to/test_project02'})

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_package')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.load_workspace')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.save_workspace')
    @mock.patch('os.chmod')
    @mock.patch('os.remove')
    def test_delete_package(self, mock_remove, mock_chmod, mock_save_workspace, mock_load_workspace, mock_get_package):
        """delete_package normal case"""

        prj = MagicMock()
        type(prj).name = 'test_project02'
        type(prj).path = '/path/to/test_project02'
        mock_get_package.return_value = prj
        mock_load_workspace.return_value = {'test_project01': '/path/to/test_project01', 'test_project02': '/path/to/test_project02'}

        ### test ###
        self.assertEqual(0, self.test.delete_package('test_project02', deletepath=True))
        mock_save_workspace.assert_called_once_with({'test_project01': '/path/to/test_project01'})
        mock_remove.assert_called_once_with('/path/to/test_project02')

    def test_validate_package(self):
        """validate_package normal case"""

        package = MagicMock()
        rtcc = MagicMock()
        type(rtcc).ext_check = MagicMock()
        type(rtcc).validate = MagicMock()
        type(rtcc).sync = MagicMock()
        type(self.admin_mock.rtcconf).RTCConf = MagicMock(return_value=rtcc)

        ### test ###
        self.test.validate_package(package, verbose=True, autofix=True, interactive=True, ext_only=False)
        rtcc.ext_check.assert_called_once_with(verbose=True, autofix=True, interactive=True)
        rtcc.validate.assert_has_calls([call(verbose=True, autofix=True, interactive=True),
                                        call(verbose=True, autofix=True, interactive=True),
                                        call(verbose=True, autofix=True, interactive=True)])

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.load_workspace')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.PackageObject')
    def test_get_packages_1(self, mock_PackageObject, mock_load_workspace):
        """ get_packages normal test"""

        proj = MagicMock()
        mock_PackageObject.return_value = proj
        mock_load_workspace.return_value = {'test_project01': '/path/to/test_project01'}

        ### test ###
        self.assertEqual([proj], self.test.get_packages(verbose=True, force=True))

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.load_workspace')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.PackageObject')
    @mock.patch('sys.stdout.write')
    def test_get_packages_2(self, mock_write, mock_PackageObject, mock_load_workspace):
        """ get_packages exception test"""

        proj = MagicMock()
        mock_PackageObject.side_effect = wasanbon.InvalidPackagePathError
        mock_load_workspace.return_value = {'test_project01': '/path/to/test_project01'}

        ### test ###
        self.assertEqual([], self.test.get_packages(verbose=True, force=True))
        mock_write.assert_called_once_with(' - Invalid Package Path (test_project01:/path/to/test_project01)\n')

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.load_workspace')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.PackageObject')
    @mock.patch('sys.stdout.write')
    def test_get_packages_3(self, mock_write, mock_PackageObject, mock_load_workspace):
        """ get_packages exception test"""

        proj = MagicMock()
        mock_PackageObject.side_effect = wasanbon.InvalidPackagePathError
        mock_load_workspace.return_value = {'test_project01': '/path/to/test_project01'}

        ### test ###
        with self.assertRaises(wasanbon.PackageNotFoundException):
            self.assertEqual([], self.test.get_packages(verbose=True, force=False))

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.load_workspace')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.PackageObject')
    def test_get_package_1(self, mock_PackageObject, mock_load_workspace):
        """get_package normal case"""

        mock_load_workspace.return_value = {'test_project01': '/path/to/test_project01'}

        ### test ###
        self.test.get_package('test_project01', verbose=True)
        mock_PackageObject.assert_called_once_with(name='test_project01', path='/path/to/test_project01')

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.load_workspace')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.PackageObject')
    def test_get_package_2(self, mock_PackageObject, mock_load_workspace):
        """get_package exception case"""

        mock_load_workspace.return_value = {'test_project01': '/path/to/test_project01'}

        ### test ###
        with self.assertRaises(wasanbon.PackageNotFoundException):
            self.test.get_package('test_project02', verbose=True)

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.load_workspace')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.PackageObject')
    @mock.patch('sys.stdout.write')
    def test_get_package_from_path_1(self, mock_write, mock_PackageObject, mock_load_workspace):
        """get_package_from_path normal case"""

        mock_load_workspace.return_value = {'test_project01': '/path/to/test_project01'}

        ### test ###
        self.test.get_package_from_path('/path/to/test_project01', verbose=True)
        mock_PackageObject.assert_called_once_with(name='test_project01', path='/path/to/test_project01')

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.load_workspace')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.PackageObject')
    @mock.patch('sys.stdout.write')
    def test_get_package_from_path_2(self, mock_write, mock_PackageObject, mock_load_workspace):
        """get_package_from_path exception case"""

        mock_load_workspace.return_value = {'test_project01': '/path/to/test_project01'}

        ### test ###
        with self.assertRaises(wasanbon.PackageNotFoundException):
            self.test.get_package('/path/to/test_project02', verbose=True)


if __name__ == '__main__':
    unittest.main()
