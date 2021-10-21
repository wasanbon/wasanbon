# test for wasanbon/core/plugins/mgr/binder_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

import wasanbon


class TestPlugin(unittest.TestCase):

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.mgr.binder_plugin as m
        self.admin_mock = MagicMock(spec=['binder', 'package', 'rtc', 'repository', 'git'])
        setattr(m, 'admin', self.admin_mock)

        def choice_func(one, two, three):
            global filename
            m.filename = 'filename'
        util = MagicMock()
        setattr(util, 'choice', choice_func)
        setattr(m, 'util', util)

        self.plugin = m.Plugin()

        ### setting parse_args return option ###
        self.options = MagicMock()
        flags = ['verbose_flag']
        for flag in flags:
            ## default: False ##
            setattr(self.options, flag, False)

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.mgr.binder_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment',
                          'admin.binder',
                          'admin.package',
                          'admin.rtc',
                          'admin.repository',
                          'admin.git'],
                         self.plugin.depends())

    """print_alt later"""

    def test_list(self):
        """list normal case"""
        ### set mock ###
        type(self.admin_mock.binder).list = MagicMock(return_value='test_list')
        ### test ###
        self.assertEqual('test_list', self.plugin.list(['argv']))

    @mock.patch('wasanbon.platform', return_value='platform')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.rename')
    def test_add_rtc_1(self, mock_rename, mock_parse_args, mock_write, mock_getcwd, mock_choice, mock_open, mock_platform):
        """add_rtc normal case"""
        ### set mock ###
        mock_parse_args.return_value = self.options, ['0', '1', '2', 'binder_name', 'hoge']
        binder = MagicMock()
        rtc = MagicMock()
        setattr(rtc, 'name', 'rtc')
        setattr(rtc, '_path', '_path')
        setattr(binder, 'rtcs', [rtc])
        setattr(binder, 'rtc_files', 'rtc_files')
        type(self.admin_mock.binder).get_binder = MagicMock(return_value=binder)
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value='package')
        rtc = MagicMock()
        setattr(rtc, 'rtcprofile', MagicMock())
        setattr(rtc.rtcprofile, 'basicInfo', MagicMock())
        setattr(rtc.rtcprofile.basicInfo, 'doc', MagicMock())
        setattr(rtc.rtcprofile.basicInfo.doc, 'description', 'rtcinfo')
        type(self.admin_mock.rtc).get_rtc_from_package = MagicMock(return_value=rtc)
        repo = MagicMock()
        setattr(repo, 'name', 'repo_name')
        setattr(repo, 'url', b'url')
        type(self.admin_mock.repository).get_repository_from_rtc = MagicMock(return_value=repo)
        p_branch = MagicMock()
        setattr(p_branch, 'communicate', lambda: (b'output', None))
        type(self.admin_mock.git).git_command = MagicMock(return_value=p_branch)
        open_ret_val = MagicMock(spec=['read', 'write'])
        open_ret_val.read.return_value = 'text:'
        mock_open.return_value = open_ret_val

        ### test ###
        self.assertEqual(0, self.plugin.add_rtc(['argv']))
        mock_write.assert_any_call('## Success. \n')

    @mock.patch('wasanbon.platform', return_value='platform')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_add_rtc_2(self, mock_parse_args, mock_write, mock_getcwd, mock_choice, mock_open, mock_platform):
        """add_rtc binder is None case"""
        ### set mock ###
        mock_parse_args.return_value = self.options, ['0', '1', '2', 'binder_name', 'rtc1']
        binder = MagicMock()
        rtc1 = MagicMock()
        setattr(rtc1, 'name', 'rtc1')
        rtc2 = MagicMock()
        setattr(rtc2, 'name', 'rtc2')
        setattr(binder, 'rtcs', [rtc1, rtc2])
        type(self.admin_mock.binder).get_binder = MagicMock(return_value=None)
        ### test ###
        self.assertEqual(-1, self.plugin.add_rtc(['argv']))

    @mock.patch('builtins.open')
    @mock.patch('wasanbon.timestampstr', return_value='')
    @mock.patch('os.path.join')
    @mock.patch('wasanbon.platform')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.rename')
    def test_add_package_1(self, mock_rename, mock_parse_args, mock_write, mock_platform, mock_join, mock_timestampstr, mock_open):
        """add_package normal case"""
        ### set mock ###
        mock_parse_args.return_value = self.options, ['0', '1', '2', 'binder_name']
        package = MagicMock()
        type(package).name = PropertyMock(return_value='package_name')
        type(package).description = PropertyMock(return_value='package_description')
        type(package).path = PropertyMock(return_value='package_path')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)
        package2 = MagicMock()
        type(package2).name = PropertyMock(return_value='package_name2')
        type(package2).description = PropertyMock(return_value='package_description')
        type(package2).path = PropertyMock(return_value='package_path')
        binder = MagicMock()
        type(binder).packages = PropertyMock(return_value=[package2, ])
        type(self.admin_mock.binder).get_binder = MagicMock(return_value=binder)
        repo = MagicMock()
        type(repo).name = PropertyMock(return_value='repo_name')
        type(repo).url = PropertyMock(return_value=b'repo_url')
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=repo)
        mock_join.return_value = 'filename'
        p_branch = MagicMock(spec=['communicate'])
        p_branch.communicate.return_value = b'output', None
        type(self.admin_mock.git).git_command = MagicMock(return_value=p_branch)
        open_ret_val = MagicMock(spec=['read', 'write'])
        open_ret_val.read.return_value = 'text:'
        mock_open.return_value = open_ret_val
        ### test ###
        self.assertEqual(0, self.plugin.add_package(['argv']))

    @mock.patch('builtins.open')
    @mock.patch('wasanbon.timestampstr', return_value='')
    @mock.patch('os.path.join')
    @mock.patch('wasanbon.platform')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.rename')
    def test_add_package_2(self, mock_rename, mock_parse_args, mock_write, mock_platform, mock_join, mock_timestampstr, mock_open):
        """add_package binder is None case"""
        ### set mock ###
        mock_parse_args.return_value = self.options, ['0', '1', '2', 'binder_name']
        package = MagicMock()
        type(package).name = PropertyMock(return_value='package_name')
        type(package).description = PropertyMock(return_value='package_description')
        type(package).path = PropertyMock(return_value='package_path')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)
        package2 = MagicMock()
        type(package2).name = PropertyMock(return_value='package_name2')
        type(package2).description = PropertyMock(return_value='package_description')
        type(package2).path = PropertyMock(return_value='package_path')
        binder = MagicMock()
        type(binder).packages = PropertyMock(return_value=[package2, ])
        type(self.admin_mock.binder).get_binder = MagicMock(return_value=None)
        repo = MagicMock()
        type(repo).name = PropertyMock(return_value='repo_name')
        type(repo).url = PropertyMock(return_value=b'repo_url')
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=repo)
        mock_join.return_value = 'filename'
        p_branch = MagicMock(spec=['communicate'])
        p_branch.communicate.return_value = b'output', None
        type(self.admin_mock.git).git_command = MagicMock(return_value=p_branch)
        open_ret_val = MagicMock(spec=['read', 'write'])
        open_ret_val.read.return_value = 'text:'
        mock_open.return_value = open_ret_val
        ### test ###
        self.assertEqual(-1, self.plugin.add_package(['argv']))

    @mock.patch('builtins.open')
    @mock.patch('wasanbon.timestampstr', return_value='')
    @mock.patch('os.path.join')
    @mock.patch('wasanbon.platform')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.rename')
    def test_add_package_3(self, mock_rename, mock_parse_args, mock_write, mock_platform, mock_join, mock_timestampstr, mock_open):
        """add_package repo is None case"""
        ### set mock ###
        mock_parse_args.return_value = self.options, ['0', '1', '2', 'binder_name']
        package = MagicMock()
        type(package).name = PropertyMock(return_value='package_name')
        type(package).description = PropertyMock(return_value='package_description')
        type(package).path = PropertyMock(return_value='package_path')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)
        package2 = MagicMock()
        type(package2).name = PropertyMock(return_value='package_name2')
        type(package2).description = PropertyMock(return_value='package_description')
        type(package2).path = PropertyMock(return_value='package_path')
        binder = MagicMock()
        type(binder).packages = PropertyMock(return_value=[package2, ])
        type(self.admin_mock.binder).get_binder = MagicMock(return_value=binder)
        repo = MagicMock()
        type(repo).name = PropertyMock(return_value='repo_name')
        type(repo).url = PropertyMock(return_value=b'repo_url')
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=None)
        mock_join.return_value = 'filename'
        p_branch = MagicMock(spec=['communicate'])
        p_branch.communicate.return_value = b'output', None
        type(self.admin_mock.git).git_command = MagicMock(return_value=p_branch)
        open_ret_val = MagicMock(spec=['read', 'write'])
        open_ret_val.read.return_value = 'text:'
        mock_open.return_value = open_ret_val
        ### test ###
        self.assertEqual(-1, self.plugin.add_package(['argv']))

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_update_rtc_1(self, mock_write, mock_parse_args):
        """update_rtc binder is None case"""

        args = ['./mgr.py', 'binder', 'update_rtc', 'binder_name', 'rtc_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_binder = MagicMock(return_value=None)
        type(self.admin_mock.binder).get_binder = get_binder

        ### test ###
        self.assertEqual(-1, self.plugin.update_rtc(args))
        mock_write.assert_any_call('# Binder(binder_name) is not found. Use wasanbon-admin.py binder create command. \n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('sys.stdout.write')
    def test_update_rtc_2(self, mock_write, mock_safe_load, mock_open, mock_parse_args):
        """update_rtc rtc_filepath is not found case"""

        args = ['./mgr.py', 'binder', 'update_rtc', 'binder_name', 'rtc_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        binder = MagicMock()
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(binder).rtcs = [rtc]
        type(binder).rtc_files = []
        type(self.admin_mock.binder).get_binder = MagicMock(return_value=binder)
        type(self.admin_mock.rtc).get_rtc_from_package = MagicMock()
        repo = MagicMock()
        type(repo).url = b'repo_url'
        type(self.admin_mock.repository).get_repository_from_rtc = MagicMock()

        ### test ###
        self.assertEqual(-1, self.plugin.update_rtc(args))
        mock_write.assert_any_call('# Binder is not found. \n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('yaml.safe_dump')
    @mock.patch('sys.stdout.write')
    def test_update_rtc_3(self, mock_write, mock_safe_dump, mock_safe_load, mock_open, mock_parse_args):
        """update_rtc success case"""

        args = ['./mgr.py', 'binder', 'update_rtc', 'binder_name', 'rtc_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        binder = MagicMock()
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(binder).rtcs = [rtc]
        type(binder).rtc_files = ['rtc_file']
        type(self.admin_mock.binder).get_binder = MagicMock(return_value=binder)
        type(self.admin_mock.rtc).get_rtc_from_package = MagicMock()
        repo = MagicMock()
        type(repo).url = b'repo_url'
        type(self.admin_mock.repository).get_repository_from_rtc = MagicMock()

        rtc_yaml = MagicMock()
        type(rtc_yaml).platform = []
        type(rtc_yaml).description = ''
        type(rtc_yaml).type = ''
        type(rtc_yaml).url = ''
        rtc_yamls = {'rtc_name': rtc_yaml}
        mock_safe_load.return_value = rtc_yamls

        p_branch = MagicMock(spec=['communicate'])
        p_branch.communicate.return_value = b'output', None
        type(self.admin_mock.git).git_command = MagicMock(return_value=p_branch)

        ### test ###
        self.assertEqual(0, self.plugin.update_rtc(args))
        mock_write.assert_any_call('## Success. \n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_update_package_1(self, mock_write, mock_parse_args):
        """update_package binder is None case"""

        args = ['./mgr.py', 'binder', 'update_package', 'package_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)

        get_binder = MagicMock(return_value=None)
        type(self.admin_mock.binder).get_binder = get_binder

        ### test ###
        self.assertEqual(-1, self.plugin.update_package(args))
        mock_write.assert_any_call('# Binder(package_name) is not found. Use wasanbon-admin.py binder create command. \n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_update_package_2(self, mock_write, mock_parse_args):
        """update_package binder is None case"""

        args = ['./mgr.py', 'binder', 'update_package', 'package_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)

        binder = MagicMock()
        b_packages = MagicMock()
        type(b_packages).name = 'package_name'
        type(binder).packages = [b_packages]
        type(binder).package_files = []
        type(self.admin_mock.binder).get_binder = MagicMock(return_value=binder)

        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=None)

        ### test ###
        self.assertEqual(-1, self.plugin.update_package(args))
        mock_write.assert_any_call('# Repository(package_path) is not found. Use mgr.py admin git_init/remote_create command. \n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('sys.stdout.write')
    def test_update_package_3(self, mock_write, mock_safe_load, mock_open, mock_parse_args):
        """update_package rtc_filepath is not found case"""

        args = ['./mgr.py', 'binder', 'update_package', 'package_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)

        binder = MagicMock()
        b_packages = MagicMock()
        type(b_packages).name = 'package_name'
        type(binder).packages = [b_packages]
        type(binder).package_files = []
        type(self.admin_mock.binder).get_binder = MagicMock(return_value=binder)

        repo = MagicMock()
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=repo)

        repo = MagicMock()
        type(repo).url = b'repo_url'
        type(self.admin_mock.repository).get_repository_from_rtc = MagicMock()

        ### test ###
        self.assertEqual(-1, self.plugin.update_package(['argv']))
        mock_write.assert_any_call('# Binder is not found. \n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('yaml.safe_dump')
    @mock.patch('sys.stdout.write')
    def test_update_package_4(self, mock_write, mock_safe_dump, mock_safe_load, mock_open, mock_parse_args):
        """update_package success case"""

        args = ['./mgr.py', 'binder', 'update_package', 'binder_name', 'rtc_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)

        binder = MagicMock()
        b_packages = MagicMock()
        type(b_packages).name = 'package_name'
        type(binder).packages = [b_packages]
        type(binder).package_files = ['package_file']
        type(self.admin_mock.binder).get_binder = MagicMock(return_value=binder)

        repo = MagicMock()
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=repo)

        package_yaml = MagicMock()
        type(package_yaml).platform = []
        type(package_yaml).description = ''
        type(package_yaml).type = ''
        type(package_yaml).url = ''
        package_yamls = {'package_name': package_yaml}
        mock_safe_load.return_value = package_yamls

        p_branch = MagicMock(spec=['communicate'])
        p_branch.communicate.return_value = b'output', None
        type(self.admin_mock.git).git_command = MagicMock(return_value=p_branch)

        ### test ###
        self.assertEqual(0, self.plugin.update_package(['argv']))
        mock_write.assert_any_call('## Success. \n')


if __name__ == '__main__':
    unittest.main()
