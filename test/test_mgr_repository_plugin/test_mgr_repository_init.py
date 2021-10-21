# test for wasanbon/core/plugins/mgr/admin_plugin/__init__.py

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
        import wasanbon.core.plugins.mgr.repository_plugin as m
        self.admin_mock = MagicMock(spec=['binder', 'package', 'rtc', 'repository', 'git', 'github'])
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()
        self.func = m

    def get_rtc(self):
        basicInfo = MagicMock()
        type(basicInfo).name = PropertyMock(return_value='test_name')
        rtcprofile = MagicMock()
        type(rtcprofile).basicInfo = PropertyMock(return_value=basicInfo)
        rtc = MagicMock()
        type(rtc).rtcprofile = PropertyMock(return_value=rtcprofile)
        type(rtc).path = PropertyMock(return_value='path')
        return rtc

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.mgr.repository_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.binder', 'admin.repository', 'admin.package',
                         'admin.git', 'admin.github', 'admin.rtc'], self.plugin.depends())

    def test_list(self):
        """list normal case"""
        type(self.admin_mock.binder).rtcs = MagicMock()
        ### test ###
        self.plugin.list({1, 2, 3})
        self.admin_mock.binder.rtcs.assert_called_once_with({1, 2, 3})

    @mock.patch('builtins.print')
    def test_print_alternative_rtcs_1(self, mock_print):
        """_print_alternative_rtcs in rtc_command case"""
        rtcs = [self.get_rtc()]

        get_package_from_path = MagicMock()
        get_package_from_path.return_value = 'test_package'
        type(self.admin_mock.package).get_package_from_path = get_package_from_path
        get_rtcs_from_package = MagicMock()
        get_rtcs_from_package.return_value = rtcs
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package
        ### test ###
        self.plugin._print_alternative_rtcs(['hoge', 'fuga', 'git_init'])
        import os
        cwd = os.getcwd()
        self.admin_mock.package.get_package_from_path.assert_called_once_with(cwd)
        self.admin_mock.rtc.get_rtcs_from_package.assert_called_once_with('test_package')
        mock_print.assert_called_once_with('test_name')

    @mock.patch('builtins.print')
    def test_print_alternative_rtcs_2(self, mock_print):
        """_print_alternative_rtcs NOT in rtc_command case"""
        rtcs = []
        rtc = MagicMock()
        type(rtc).name = PropertyMock(return_value='test_name')
        rtcs.append(rtc)

        get_rtc_repos = MagicMock(return_value=rtcs)
        type(self.admin_mock.binder).get_rtc_repos = get_rtc_repos
        ### test ###
        self.plugin._print_alternative_rtcs(['hoge', 'fuga', 'fuga2'])
        self.admin_mock.binder.get_rtc_repos.assert_called_once()
        mock_print.assert_called_once_with('test_name')

    @mock.patch('wasanbon.arg_check')
    @mock.patch('os.chdir')
    def test_clone_1(self, mock_chdir, mock_arg_check):
        """clone url is None case"""
        type(self.admin_mock.package).get_package_from_path = MagicMock()
        type(self.admin_mock.binder).get_rtc_repos = MagicMock()

        ### test ###
        args = []
        with self.assertRaises(wasanbon.RepositoryNotFoundException):
            self.plugin.clone(args)

    @mock.patch('wasanbon.arg_check')
    @mock.patch('os.chdir')
    def test_clone_2(self, mock_chdir, mock_arg_check):
        """clone url is None and NOT founded RTC case"""
        type(self.admin_mock.package).get_package_from_path = MagicMock()
        repo = MagicMock()
        type(repo).name = PropertyMock(return_value='no_test_rtc')
        repos = [repo]
        get_rtc_repos = MagicMock(return_value=repos)
        type(self.admin_mock.binder).get_rtc_repos = get_rtc_repos

        ### test ###
        args = ['', '', '', 'test_rtc']
        with self.assertRaises(wasanbon.RepositoryNotFoundException):
            self.plugin.clone(args)

    @mock.patch('wasanbon.arg_check')
    @mock.patch('os.chdir')
    @mock.patch('sys.stdout.write')
    def test_clone_3(self, mock_write, mock_chdir, mock_arg_check):
        """clone url is None and founded RTC and Clone ERROR case"""
        type(self.admin_mock.package).get_package_from_path = MagicMock()
        repo = MagicMock()
        type(repo).name = PropertyMock(return_value='test_rtc')
        repos = [repo]
        get_rtc_repos = MagicMock(return_value=repos)
        type(self.admin_mock.binder).get_rtc_repos = get_rtc_repos
        clone_rtc = MagicMock(return_value=-1)
        type(self.admin_mock.repository).clone_rtc = clone_rtc

        ### test ###
        args = ['', '', '', 'test_rtc']
        self.assertEqual(-1, self.plugin.clone(args))
        mock_write.assert_any_call('# Cloning RTC (test_rtc)\n')
        mock_write.assert_any_call('## Failed. Return Code = -1\n')

    @mock.patch('wasanbon.arg_check')
    @mock.patch('os.chdir')
    @mock.patch('sys.stdout.write')
    def test_clone_4(self, mock_write, mock_chdir, mock_arg_check):
        """clone url is None and founded RTC and Clone SUCCESS case"""
        type(self.admin_mock.package).get_package_from_path = MagicMock()
        repo = MagicMock()
        type(repo).name = PropertyMock(return_value='test_rtc')
        repos = [repo]
        get_rtc_repos = MagicMock(return_value=repos)
        type(self.admin_mock.binder).get_rtc_repos = get_rtc_repos
        clone_rtc = MagicMock(return_value=0)
        type(self.admin_mock.repository).clone_rtc = clone_rtc

        ### test ###
        args = ['', '', '', 'test_rtc']
        self.assertEqual(0, self.plugin.clone(args))
        mock_write.assert_any_call('# Cloning RTC (test_rtc)\n')
        mock_write.assert_any_call('## Success.\n')

    @mock.patch('wasanbon.arg_check')
    @mock.patch('os.chdir')
    @mock.patch('sys.stdout.write')
    def test_clone_5(self, mock_write, mock_chdir, mock_arg_check):
        """clone url and founded RTC and Clone ERROR case"""
        type(self.admin_mock.package).get_package_from_path = MagicMock()
        repo = MagicMock()
        type(repo).name = PropertyMock(return_value='test_rtc')
        repos = [repo]
        get_rtc_repos = MagicMock(return_value=repos)
        type(self.admin_mock.binder).get_rtc_repos = get_rtc_repos
        clone_rtc = MagicMock(return_value=-1)
        type(self.admin_mock.repository).clone_rtc = clone_rtc

        ### test ###
        args = ['', '', '', '-u', 'http://github.com/test_rtc.git']
        self.assertEqual(-1, self.plugin.clone(args))
        mock_write.assert_any_call('# Cloning RTC (test_rtc)\n')
        mock_write.assert_any_call('## Failed. Return Code = -1\n')

    @mock.patch('wasanbon.arg_check')
    @mock.patch('os.chdir')
    @mock.patch('sys.stdout.write')
    def test_clone_6(self, mock_write, mock_chdir, mock_arg_check):
        """clone url and founded RTC and Clone SUCCESS case"""
        type(self.admin_mock.package).get_package_from_path = MagicMock()
        repo = MagicMock()
        type(repo).name = PropertyMock(return_value='test_rtc')
        repos = [repo]
        get_rtc_repos = MagicMock(return_value=repos)
        type(self.admin_mock.binder).get_rtc_repos = get_rtc_repos
        clone_rtc = MagicMock(return_value=0)
        type(self.admin_mock.repository).clone_rtc = clone_rtc

        ### test ###
        args = ['', '', '', '-u', 'http://github.com/test_rtc.git']
        self.assertEqual(0, self.plugin.clone(args))
        mock_write.assert_any_call('# Cloning RTC (test_rtc)\n')
        mock_write.assert_any_call('## Success.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_fix_gitignore_1(self, mock_parse_args):
        """fix_gitignore all and NOT founded rtcs case"""
        rtcs = []

        args = ['./mgr.py', 'repository', 'fix_gitignore']
        options = MagicMock()
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock()
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        ### test ###
        self.assertEqual(0, self.plugin.fix_gitignore(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_fix_gitignore_2(self, mock_write, mock_parse_args):
        """fix_gitignore all and founded rtcs case"""
        rtc = self.get_rtc()
        rtcs = [rtc]

        args = ['./mgr.py', 'repository', 'fix_gitignore']
        options = MagicMock()
        type(options).verbose_flag = False
        type(options).long_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock()
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        check_dot_gitignore = MagicMock(return_value=True)
        type(self.admin_mock.repository).check_dot_gitignore = check_dot_gitignore

        ### test ###
        self.assertEqual(0, self.plugin.fix_gitignore(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once_with(rtc, verbose=False)
        mock_write.assert_any_call('test_name : \n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_fix_gitignore_3(self, mock_write, mock_parse_args):
        """fix_gitignore all and founded rtcs and check error case"""
        rtc = self.get_rtc()
        rtcs = [rtc]

        args = ['./mgr.py', 'repository', 'fix_gitignore']
        options = MagicMock()
        type(options).verbose_flag = False
        type(options).long_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock()
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        check_dot_gitignore = MagicMock(return_value=False)
        type(self.admin_mock.repository).check_dot_gitignore = check_dot_gitignore

        add = MagicMock()
        type(self.admin_mock.repository).add = add

        ### test ###
        self.assertEqual(0, self.plugin.fix_gitignore(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once_with(rtc, verbose=False)
        mock_write.assert_any_call('test_name : \n')
        add.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_fix_gitignore_4(self, mock_write, mock_parse_args):
        """fix_gitignore all and founded rtcs and long flag case"""
        rtc = self.get_rtc()
        rtcs = [rtc]

        args = ['./mgr.py', 'repository', 'fix_gitignore']
        options = MagicMock()
        type(options).verbose_flag = False
        type(options).long_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock()
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        get_status = MagicMock(return_value='get_status_result')
        type(self.admin_mock.repository).get_status = get_status

        check_dot_gitignore = MagicMock(return_value=False)
        type(self.admin_mock.repository).check_dot_gitignore = check_dot_gitignore

        ### test ###
        self.assertEqual(0, self.plugin.fix_gitignore(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once_with(rtc, verbose=False)
        mock_write.assert_any_call('get_status_result')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_fix_gitignore_5(self, mock_write, mock_parse_args):
        """fix_gitignore select rtc case"""
        rtc = self.get_rtc()
        rtcs = [rtc]

        args = ['./mgr.py', 'repository', 'fix_gitignore', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = False
        type(options).long_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock()
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        get_status = MagicMock(return_value='get_status_result')
        type(self.admin_mock.repository).get_status = get_status

        check_dot_gitignore = MagicMock(return_value=False)
        type(self.admin_mock.repository).check_dot_gitignore = check_dot_gitignore

        ### test ###
        self.assertEqual(0, self.plugin.fix_gitignore(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once_with(rtc, verbose=False)
        mock_write.assert_any_call('get_status_result')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_fix_gitignore_6(self, mock_write, mock_parse_args):
        """fix_gitignore select rtc and NOT founded RTC case"""
        rtc = self.get_rtc()
        rtcs = [rtc]

        args = ['./mgr.py', 'repository', 'fix_gitignore', 'test_name_dummy']
        options = MagicMock()
        type(options).verbose_flag = False
        type(options).long_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock()
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        ### test ###
        self.assertEqual(0, self.plugin.fix_gitignore(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_status_1(self, mock_write, mock_parse_args):
        """status all and NOT founded RTC case"""
        rtcs = []

        args = ['./mgr.py', 'repository', 'status']
        options = MagicMock()
        type(options).verbose_flag = False
        type(options).long_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock()
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        ### test ###
        self.assertEqual(0, self.plugin.status(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_status_2(self, mock_write, mock_parse_args):
        """status all and founded RTC case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'status']
        options = MagicMock()
        type(options).verbose_flag = False
        type(options).long_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock(return_value='')
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        get_status = MagicMock(return_value='get_status_result')
        type(self.admin_mock.repository).get_status = get_status

        ### test ###
        self.assertEqual(0, self.plugin.status(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        get_status.assert_called_once()
        mock_write.assert_any_call('get_status_result')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_status_3(self, mock_write, mock_parse_args):
        """status all and founded RTC and long flag is False case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'status']
        options = MagicMock()
        type(options).verbose_flag = False
        type(options).long_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock(return_value='')
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        check_dot_gitignore = MagicMock(return_value=False)
        type(self.admin_mock.repository).check_dot_gitignore = check_dot_gitignore

        is_modified = MagicMock(return_value=False)
        is_untracked = MagicMock(return_value=False)
        is_added = MagicMock(return_value=False)
        type(self.admin_mock.repository).is_modified = is_modified
        type(self.admin_mock.repository).is_untracked = is_untracked
        type(self.admin_mock.repository).is_added = is_added

        ### test ###
        self.assertEqual(0, self.plugin.status(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        mock_write.assert_any_call('## Warning! .gitignore seems to have some problems.\n')
        mock_write.assert_any_call('test_name : \n')
        mock_write.assert_any_call('  Up-to-date\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_status_4(self, mock_write, mock_parse_args):
        """status all and founded RTC and RTC is modified case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'status']
        options = MagicMock()
        type(options).verbose_flag = False
        type(options).long_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock(return_value='')
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        check_dot_gitignore = MagicMock(return_value=False)
        type(self.admin_mock.repository).check_dot_gitignore = check_dot_gitignore

        is_modified = MagicMock(return_value=True)
        is_untracked = MagicMock(return_value=False)
        is_added = MagicMock(return_value=False)
        type(self.admin_mock.repository).is_modified = is_modified
        type(self.admin_mock.repository).is_untracked = is_untracked
        type(self.admin_mock.repository).is_added = is_added

        ### test ###
        self.assertEqual(0, self.plugin.status(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        mock_write.assert_any_call('## Warning! .gitignore seems to have some problems.\n')
        mock_write.assert_any_call('test_name : \n')
        mock_write.assert_any_call('  Modified\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_status_5(self, mock_write, mock_parse_args):
        """status all and founded RTC and RTC is untracked case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'status']
        options = MagicMock()
        type(options).verbose_flag = False
        type(options).long_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock(return_value='')
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        check_dot_gitignore = MagicMock(return_value=False)
        type(self.admin_mock.repository).check_dot_gitignore = check_dot_gitignore

        is_modified = MagicMock(return_value=False)
        is_untracked = MagicMock(return_value=True)
        is_added = MagicMock(return_value=False)
        type(self.admin_mock.repository).is_modified = is_modified
        type(self.admin_mock.repository).is_untracked = is_untracked
        type(self.admin_mock.repository).is_added = is_added

        ### test ###
        self.assertEqual(0, self.plugin.status(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        mock_write.assert_any_call('## Warning! .gitignore seems to have some problems.\n')
        mock_write.assert_any_call('test_name : \n')
        mock_write.assert_any_call('  Untracked\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_status_6(self, mock_write, mock_parse_args):
        """status all and founded RTC and RTC is added case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'status']
        options = MagicMock()
        type(options).verbose_flag = False
        type(options).long_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock(return_value='')
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        check_dot_gitignore = MagicMock(return_value=False)
        type(self.admin_mock.repository).check_dot_gitignore = check_dot_gitignore

        is_modified = MagicMock(return_value=False)
        is_untracked = MagicMock(return_value=False)
        is_added = MagicMock(return_value=True)
        type(self.admin_mock.repository).is_modified = is_modified
        type(self.admin_mock.repository).is_untracked = is_untracked
        type(self.admin_mock.repository).is_added = is_added

        ### test ###
        self.assertEqual(0, self.plugin.status(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        mock_write.assert_any_call('## Warning! .gitignore seems to have some problems.\n')
        mock_write.assert_any_call('test_name : \n')
        mock_write.assert_any_call('  Added\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_commit_1(self, mock_write, mock_parse_args):
        """commit all and NOT founded RTC case"""
        rtcs = []

        args = ['./mgr.py', 'repository', 'commit', 'all', 'comment']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock(return_value='')
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        ### test ###
        self.assertEqual(0, self.plugin.commit(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_not_called()
        mock_write.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_commit_2(self, mock_write, mock_parse_args):
        """commit all and founded RTC and commit SUCCESS case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'commit', 'all', 'comment']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).push_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock(return_value='')
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        commit = MagicMock(return_value=0)
        type(self.admin_mock.repository).commit = commit

        ### test ###
        self.assertEqual(0, self.plugin.commit(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        mock_write.assert_any_call('# Committing RTC (test_name) \n')
        mock_write.assert_any_call('## Success\n')
        mock_write.assert_any_call('# RTC (test_name) Commit :                 Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_commit_3(self, mock_write, mock_parse_args):
        """commit all and founded RTC and commit FAILED case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'commit', 'all', 'comment']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).push_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock(return_value='')
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        commit = MagicMock(return_value=-1)
        type(self.admin_mock.repository).commit = commit

        ### test ###
        self.assertEqual(-1, self.plugin.commit(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        mock_write.assert_any_call('# Committing RTC (test_name) \n')
        mock_write.assert_any_call('## Failed.\n')
        mock_write.assert_any_call('# RTC (test_name) Commit :                 Failed\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('sys.stdout.flush')
    def test_commit_4(self, mock_flush, mock_write, mock_parse_args):
        """commit all and founded RTC and push SUCCESS case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'commit', 'all', 'comment']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).push_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        repo = MagicMock()
        type(repo)._path = "path"
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        commit = MagicMock(return_value=0)
        type(self.admin_mock.repository).commit = commit

        p_branch = MagicMock()
        communicate = MagicMock(return_value=(b"branch", "stderr"))
        type(p_branch).communicate = communicate

        git_command = MagicMock(return_value=p_branch)
        type(self.admin_mock.git).git_command = git_command

        push = MagicMock(return_value=0)
        type(self.admin_mock.repository).push = push

        ### test ###
        self.assertEqual(0, self.plugin.commit(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        git_command.assert_called_once()
        mock_write.assert_any_call('# Committing RTC (test_name) \n')
        mock_write.assert_any_call('## Success\n')
        mock_write.assert_any_call('# Pushing RTC (test_name) \n')
        mock_write.assert_any_call('Set Username:"your_username" and Password:"your_token"\n')
        mock_write.assert_any_call('## Success\n')
        mock_write.assert_any_call('# RTC (test_name) Commit :                 Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('sys.stdout.flush')
    def test_commit_5(self, mock_flush, mock_write, mock_parse_args):
        """commit all and founded RTC and push FAILED case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'commit', 'all', 'comment']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).push_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        repo = MagicMock()
        type(repo)._path = "path"
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        commit = MagicMock(return_value=0)
        type(self.admin_mock.repository).commit = commit

        p_branch = MagicMock()
        communicate = MagicMock(return_value=(b"branch", "stderr"))
        type(p_branch).communicate = communicate

        git_command = MagicMock(return_value=p_branch)
        type(self.admin_mock.git).git_command = git_command

        push = MagicMock(return_value=-1)
        type(self.admin_mock.repository).push = push

        ### test ###
        self.assertEqual(0, self.plugin.commit(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        git_command.assert_called_once()
        mock_write.assert_any_call('# Committing RTC (test_name) \n')
        mock_write.assert_any_call('## Success\n')
        mock_write.assert_any_call('# Pushing RTC (test_name) \n')
        mock_write.assert_any_call('Set Username:"your_username" and Password:"your_token"\n')
        mock_write.assert_any_call('## Failed.\n')
        mock_write.assert_any_call('# RTC (test_name) Commit :                 Failed\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('sys.stdout.flush')
    def test_commit_6(self, mock_flush, mock_write, mock_parse_args):
        """commit select RTC and push SUCCESS case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'commit', 'test_name', 'comment']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).push_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        repo = MagicMock()
        type(repo)._path = "path"
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        commit = MagicMock(return_value=0)
        type(self.admin_mock.repository).commit = commit

        p_branch = MagicMock()
        communicate = MagicMock(return_value=(b"branch", "stderr"))
        type(p_branch).communicate = communicate

        git_command = MagicMock(return_value=p_branch)
        type(self.admin_mock.git).git_command = git_command

        push = MagicMock(return_value=0)
        type(self.admin_mock.repository).push = push

        ### test ###
        self.assertEqual(0, self.plugin.commit(args))
        get_rtc_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        git_command.assert_called_once()
        mock_write.assert_any_call('# Committing RTC (test_name) \n')
        mock_write.assert_any_call('## Success\n')
        mock_write.assert_any_call('# Pushing RTC (test_name) \n')
        mock_write.assert_any_call('Set Username:"your_username" and Password:"your_token"\n')
        mock_write.assert_any_call('## Success\n')
        mock_write.assert_any_call('# RTC (test_name) Commit :                 Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_push_1(self, mock_write, mock_parse_args):
        """push all and NOT founded RTC case"""
        rtcs = []

        args = ['./mgr.py', 'repository', 'push', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock(return_value='')
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        ### test ###
        self.assertEqual(0, self.plugin.push(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_not_called()
        mock_write.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('sys.stdout.flush')
    def test_push_2(self, mock_flush, mock_write, mock_parse_args):
        """push all and push SUCCESS case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'push', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        repo = MagicMock()
        type(repo)._path = "path"
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        p_branch = MagicMock()
        communicate = MagicMock(return_value=(b"branch", "stderr"))
        type(p_branch).communicate = communicate

        git_command = MagicMock(return_value=p_branch)
        type(self.admin_mock.git).git_command = git_command

        push = MagicMock(return_value=0)
        type(self.admin_mock.repository).push = push

        ### test ###
        self.assertEqual(0, self.plugin.push(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        git_command.assert_called_once()
        mock_write.assert_any_call('# Pushing RTC (test_name) \n')
        mock_write.assert_any_call('Set Username:"your_username" and Password:"your_token"\n')
        mock_write.assert_any_call('## Success\n')
        mock_write.assert_any_call('# RTC (test_name) Push :                 Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('sys.stdout.flush')
    def test_push_3(self, mock_flush, mock_write, mock_parse_args):
        """push all and push FAILED case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'push', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        repo = MagicMock()
        type(repo)._path = "path"
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        p_branch = MagicMock()
        communicate = MagicMock(return_value=(b"branch", "stderr"))
        type(p_branch).communicate = communicate

        git_command = MagicMock(return_value=p_branch)
        type(self.admin_mock.git).git_command = git_command

        push = MagicMock(return_value=-1)
        type(self.admin_mock.repository).push = push

        ### test ###
        self.assertEqual(0, self.plugin.push(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        git_command.assert_called_once()
        mock_write.assert_any_call('# Pushing RTC (test_name) \n')
        mock_write.assert_any_call('Set Username:"your_username" and Password:"your_token"\n')
        mock_write.assert_any_call('## Failed\n')
        mock_write.assert_any_call('# RTC (test_name) Push :                 Failed\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('sys.stdout.flush')
    def test_push_4(self, mock_flush, mock_write, mock_parse_args):
        """push select RTC and push SUCCESS case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'push', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).push_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        repo = MagicMock()
        type(repo)._path = "path"
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        p_branch = MagicMock()
        communicate = MagicMock(return_value=(b"branch", "stderr"))
        type(p_branch).communicate = communicate

        git_command = MagicMock(return_value=p_branch)
        type(self.admin_mock.git).git_command = git_command

        push = MagicMock(return_value=0)
        type(self.admin_mock.repository).push = push

        ### test ###
        self.assertEqual(0, self.plugin.push(args))
        get_rtc_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        git_command.assert_called_once()
        mock_write.assert_any_call('# Pushing RTC (test_name) \n')
        mock_write.assert_any_call('Set Username:"your_username" and Password:"your_token"\n')
        mock_write.assert_any_call('## Success\n')
        mock_write.assert_any_call('# RTC (test_name) Push :                 Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_pull_5(self, mock_write, mock_parse_args):
        """pull all and NOT founded RTC case"""
        rtcs = []

        args = ['./mgr.py', 'repository', 'pull', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.pull(args))
        get_rtcs_from_package.assert_called_once()
        mock_write.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_pull_6(self, mock_write, mock_parse_args):
        """pull all and founded RTC and pull SUCCESS case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'pull', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock()
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        pull = MagicMock(return_value=0)
        type(self.admin_mock.repository).pull = pull

        ### test ###
        self.assertEqual(0, self.plugin.pull(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        mock_write.assert_any_call('# Pulling RTC (test_name) \n')
        mock_write.assert_any_call('## Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_pull_1(self, mock_write, mock_parse_args):
        """pull all and founded RTC and pull FAILED case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'pull', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock()
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        pull = MagicMock(return_value=-1)
        type(self.admin_mock.repository).pull = pull

        ### test ###
        self.assertEqual(-1, self.plugin.pull(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        mock_write.assert_any_call('# Pulling RTC (test_name) \n')
        mock_write.assert_any_call('## Failed\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('os.remove')
    @mock.patch('shutil.copy')
    @mock.patch('yaml.safe_load', return_value='')
    @mock.patch('builtins.open')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.timestampstr', return_value='2021100100000000')
    @mock.patch('sys.stdout.write')
    def test_sync_1(self, mock_write, mock_timestampstr, mock_dump, mock_open, mock_safe_load, mock_copy, mock_remove, mock_isfile, mock_parse_args):
        """sunc no rtc case"""
        rtcs = []

        args = ['./mgr.py', 'repository', 'sync']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_rtcpath = MagicMock(return_value='.')
        type(package).get_rtcpath = get_rtcpath

        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.sync(args))
        mock_copy.assert_called_once_with('./repository.yaml', './repository.yaml2021100100000000')
        mock_dump.assert_called_once()
        mock_write.assert_any_call('# Writing repository.yaml for package distribution\n')
        mock_write.assert_any_call('## Parsing RTC directory\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('os.remove')
    @mock.patch('shutil.copy')
    @mock.patch('yaml.safe_load', return_value='')
    @mock.patch('builtins.open')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.timestampstr', return_value='2021100100000000')
    @mock.patch('sys.stdout.write')
    def test_sync_2(self, mock_write, mock_timestampstr, mock_dump, mock_open, mock_safe_load, mock_copy, mock_remove, mock_isfile, mock_parse_args):
        """sunc founded rtc case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'sync']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_rtcpath = MagicMock()
        get_rtcpath.return_value = '.'
        type(package).get_rtcpath = get_rtcpath

        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        repo = MagicMock()
        type(repo).name = 'name'
        type(repo).description = 'description'
        type(repo).hash = b'hash'
        get_repository_from_path = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_path = get_repository_from_path

        ### test ###
        self.assertEqual(0, self.plugin.sync(args))
        mock_copy.assert_called_once_with('./repository.yaml', './repository.yaml2021100100000000')
        mock_dump.assert_called_once()
        mock_write.assert_any_call('# Writing repository.yaml for package distribution\n')
        mock_write.assert_any_call('## Parsing RTC directory\n')
        mock_write.assert_any_call('### RTC test_name\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('os.remove')
    @mock.patch('shutil.copy')
    @mock.patch('yaml.safe_load', return_value='')
    @mock.patch('builtins.open')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.timestampstr', return_value='2021100100000000')
    @mock.patch('sys.stdout.write')
    def test_sync_3(self, mock_write, mock_timestampstr, mock_dump, mock_open, mock_safe_load, mock_copy, mock_remove, mock_isfile, mock_parse_args):
        """sunc founded rtc with url case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'sync']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_rtcpath = MagicMock(return_value='.')
        type(package).get_rtcpath = get_rtcpath

        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        repo = MagicMock()
        type(repo).name = 'name'
        type(repo).description = 'description'
        type(repo).hash = b'hash'
        type(repo).url = b'url\n'
        get_repository_from_path = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_path = get_repository_from_path

        ### test ###
        self.assertEqual(0, self.plugin.sync(args))
        mock_copy.assert_called_once_with('./repository.yaml', './repository.yaml2021100100000000')
        mock_dump.assert_called_once()
        mock_write.assert_any_call('# Writing repository.yaml for package distribution\n')
        mock_write.assert_any_call('## Parsing RTC directory\n')
        mock_write.assert_any_call('### RTC test_name\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.print')
    @mock.patch('sys.stdout.write')
    def test_url_1(self, mock_write, mock_print, mock_parse_args):
        """url repo is founded case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'url', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        repo = MagicMock()
        type(repo).url = 'url'
        get_rtc_repo = MagicMock(return_value=repo)
        type(self.admin_mock.binder).get_rtc_repo = get_rtc_repo

        ### test ###
        self.assertEqual(0, self.plugin.url(args))
        mock_print.assert_any_call('url')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.print')
    @mock.patch('sys.stdout.write')
    def test_url_2(self, mock_write, mock_print, mock_parse_args):
        """url repo is NOT founded case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'url', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        repo = MagicMock()
        type(repo).url = 'url'
        get_rtc_repo = MagicMock(return_value=None)
        type(self.admin_mock.binder).get_rtc_repo = get_rtc_repo

        ### test ###
        self.assertEqual(-1, self.plugin.url(args))
        mock_write.assert_any_call('# Repository Not Found.\n')
        mock_print.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.print')
    @mock.patch('sys.stdout.write')
    def test_name_1(self, mock_write, mock_print, mock_parse_args):
        """name repo is founded case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'name', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        repo = MagicMock()
        type(repo).name = 'name'
        get_rtc_repo = MagicMock(return_value=repo)
        type(self.admin_mock.binder).get_rtc_repo = get_rtc_repo

        ### test ###
        self.assertEqual(0, self.plugin.name(args))
        mock_print.assert_any_call('name')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.print')
    @mock.patch('sys.stdout.write')
    def test_name_2(self, mock_write, mock_print, mock_parse_args):
        """name repo is NOT founded case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'name', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_rtc_repo = MagicMock(return_value=None)
        type(self.admin_mock.binder).get_rtc_repo = get_rtc_repo

        ### test ###
        self.assertEqual(-1, self.plugin.name(args))
        mock_write.assert_any_call('# Repository Not Found.\n')
        mock_print.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_git_init_1(self, mock_write, mock_parse_args):
        """git_init all and NOT founded RTC case"""
        rtcs = []

        args = ['./mgr.py', 'repository', 'git_init', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.git_init(args))
        get_rtcs_from_package.assert_called_once()
        mock_write.assert_any_call('### Success.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_git_init_2(self, mock_write, mock_parse_args):
        """git_init all and founded RTC and git_init allready inited case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'git_init', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        repo = MagicMock()
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        ### test ###
        self.assertEqual(-1, self.plugin.git_init(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        mock_write.assert_any_call('# Initializing git local repository on RTC (test_name) \n')
        mock_write.assert_any_call('## RTC already has local repository.\n')
        mock_write.assert_any_call('## Failed.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_git_init_3(self, mock_write, mock_parse_args):
        """git_init all and founded RTC and git_init_success case"""
        rtcs = [self.get_rtc()]

        args = ['./mgr.py', 'repository', 'git_init', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        get_repository_from_rtc = MagicMock(return_value=None)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        init_git_repository_to_path = MagicMock()
        type(self.admin_mock.repository).init_git_repository_to_path = init_git_repository_to_path

        add_files = MagicMock()
        type(self.admin_mock.repository).add_files = add_files

        commit = MagicMock(return_value=-1)
        type(self.admin_mock.repository).commit = commit

        ### test ###
        self.assertEqual(0, self.plugin.git_init(args))
        get_rtcs_from_package.assert_called_once()
        get_repository_from_rtc.assert_called_once()
        init_git_repository_to_path.assert_called_once()
        add_files.assert_called_once()
        mock_write.assert_any_call('# Initializing git local repository on RTC (test_name) \n')
        mock_write.assert_any_call('## Creating git repository in path\n')
        mock_write.assert_any_call('## Adding Files to repository\n')
        mock_write.assert_any_call('## Commiting ...\n')
        mock_write.assert_any_call('## First Commit failed.')
        mock_write.assert_any_call('## Success\n')
        mock_write.assert_any_call('### Success.\n')

    def test_get_registered_repository_from_rtc_1(self):
        """get_registered_repository_from_rtc target_repo is None case"""

        get_repository_from_rtc = MagicMock(return_value=None)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        ### test ###
        self.assertEqual(None, self.plugin.get_registered_repository_from_rtc(None))

    def test_get_registered_repository_from_rtc_2(self):
        """get_registered_repository_from_rtc result_repo is None case"""

        repo = MagicMock()
        type(repo).url = b'target_url'
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        get_rtc_repos = MagicMock(return_value=[])
        type(self.admin_mock.binder).get_rtc_repos = get_rtc_repos

        ### test ###
        self.assertEqual(None, self.plugin.get_registered_repository_from_rtc(None))

    def test_get_registered_repository_from_rtc_3(self):
        """get_registered_repository_from_rtc normal case"""

        repo = MagicMock()
        type(repo).url = b'target_url'
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        repo_2 = MagicMock()
        type(repo_2).url = 'target_url'
        get_rtc_repos = MagicMock(return_value=[repo_2])
        type(self.admin_mock.binder).get_rtc_repos = get_rtc_repos

        ### test ###
        self.assertEqual(repo_2, self.plugin.get_registered_repository_from_rtc(None))

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.user_pass')
    @mock.patch('os.chdir')
    def test_get_rtcprofile_1(self, mock_chdir, mock_user_pass, mock_write, mock_parse_args):
        """get_rtcprofile not match case"""

        args = ['./mgr.py', 'repository', 'get_rtcprofile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).url = "None"
        mock_parse_args.return_value = options, args

        mock_user_pass.return_value = 'username', 'password', 'token'

        github = MagicMock()
        type(github).get_file_contents = MagicMock()
        Github = MagicMock(return_value=github)
        type(self.admin_mock.github).Github = Github

        pack = MagicMock()
        type(pack).get_rtcpath = MagicMock()
        get_package_from_path = MagicMock(return_value=pack)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtc_repos = MagicMock(return_value=[])
        type(self.admin_mock.binder).get_rtc_repos = get_rtc_repos

        with self.assertRaises(wasanbon.RepositoryNotFoundException):
            self.plugin.get_rtcprofile(args)

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.user_pass')
    @mock.patch('os.chdir')
    @mock.patch('os.path.exists')
    @mock.patch('os.mkdir')
    @mock.patch('sys.stdout.write')
    def test_get_rtcprofile_2(self, mock_write, mock_mkdir, mock_exists, mock_chdir, mock_user_pass, mock_parse_args):
        """get_rtcprofile match case"""

        args = ['./mgr.py', 'repository', 'get_rtcprofile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).url = "None"
        mock_parse_args.return_value = options, args

        mock_user_pass.return_value = 'username', 'password', 'token'

        github = MagicMock()
        type(github).get_file_contents = MagicMock(return_value=-1)
        Github = MagicMock(return_value=github)
        type(self.admin_mock.github).Github = Github

        pack = MagicMock()
        type(pack).get_rtcpath = MagicMock()
        get_package_from_path = MagicMock(return_value=pack)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        repo = MagicMock()
        type(repo).name = 'test_name'
        type(repo).url = 'http://git-no-hub.com/owner/target.git'
        get_rtc_repos = MagicMock(return_value=[repo])
        type(self.admin_mock.binder).get_rtc_repos = get_rtc_repos

        ### test ###
        self.assertEqual(-1, self.plugin.get_rtcprofile(args))
        mock_write.assert_any_call('# Accessing Remote repository named test_name\n')
        mock_write.assert_any_call('## Repository Service is git-no-hub.com\n')
        mock_write.assert_any_call('## Error Service (git-no-hub.com) is not available\n')
        mock_write.assert_any_call('# Collectiong RTC.xml (target)\n')
        mock_write.assert_any_call('## Failed. Return Code = -1\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.user_pass')
    @mock.patch('os.chdir')
    @mock.patch('os.path.exists')
    @mock.patch('os.mkdir')
    @mock.patch('sys.stdout.write')
    def test_get_rtcprofile_3(self, mock_write, mock_mkdir, mock_exists, mock_chdir, mock_user_pass, mock_parse_args):
        """get_rtcprofile match case"""

        args = ['./mgr.py', 'repository', 'get_rtcprofile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).url = "None"
        mock_parse_args.return_value = options, args

        mock_user_pass.return_value = 'username', 'password', 'token'

        github = MagicMock()
        type(github).get_file_contents = MagicMock(return_value=0)
        Github = MagicMock()
        Github.return_value = github
        type(self.admin_mock.github).Github = Github

        pack = MagicMock()
        type(pack).get_rtcpath = MagicMock()
        get_package_from_path = MagicMock(return_value=pack)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        repo = MagicMock()
        type(repo).name = 'test_name'
        type(repo).url = 'http://git-no-hub.com/owner/target.git'
        get_rtc_repos = MagicMock(return_value=[repo])
        type(self.admin_mock.binder).get_rtc_repos = get_rtc_repos

        ### test ###
        self.assertEqual(0, self.plugin.get_rtcprofile(args))
        mock_write.assert_any_call('# Accessing Remote repository named test_name\n')
        mock_write.assert_any_call('## Repository Service is git-no-hub.com\n')
        mock_write.assert_any_call('## Error Service (git-no-hub.com) is not available\n')
        mock_write.assert_any_call('# Collectiong RTC.xml (target)\n')
        mock_write.assert_any_call('## Success.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_remote_create_1(self, mock_write, mock_parse_args):
        """remote_create repository NOT founded case"""

        args = ['./mgr.py', 'repository', 'remote_create', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_rtc_from_package = MagicMock()
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        get_repository_from_rtc = MagicMock(return_value=None)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        ### test ###
        self.assertEqual(-1, self.plugin.remote_create(args))
        mock_write.assert_any_call('# Repository is not found.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_remote_create_2(self, mock_write, mock_parse_args):
        """remote_create repository NOT founded case"""

        args = ['./mgr.py', 'repository', 'remote_create', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_rtc_from_package = MagicMock()
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        get_repository_from_rtc = MagicMock(side_effect=wasanbon.RepositoryNotFoundException(), return_value=None)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        ### test ###
        self.assertEqual(-1, self.plugin.remote_create(args))
        mock_write.assert_any_call('# Repository is not found.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.user_pass')
    def test_remote_create_1(self, mock_user_pass, mock_write, mock_parse_args):
        """remote_create repository Already Exists Repo case"""
        rtc = self.get_rtc()

        args = ['./mgr.py', 'repository', 'remote_create', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_rtc_from_package = MagicMock(return_value=rtc)
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        repo = MagicMock()
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        mock_user_pass.return_value = 'username', 'password', 'token'

        github = MagicMock()
        type(github).exists_repo = MagicMock(return_value=True)
        Github = MagicMock(return_value=github)
        type(self.admin_mock.github).Github = Github

        ### test ###
        self.assertEqual(-1, self.plugin.remote_create(args))
        mock_write.assert_any_call('# Creating Remote repository named test_name\n')
        mock_write.assert_any_call('## Error. Repository test_name already exists.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.user_pass')
    @mock.patch('sys.stdout.flush')
    def test_remote_create_2(self, mock_flush, mock_user_pass, mock_write, mock_parse_args):
        """remote_create repository failed case"""
        rtc = self.get_rtc()

        args = ['./mgr.py', 'repository', 'remote_create', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_rtc_from_package = MagicMock(return_value=rtc)
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        repo = MagicMock()
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        mock_user_pass.return_value = 'username', 'password', 'token'

        github = MagicMock()
        type(github).exists_repo = MagicMock(return_value=False)
        type(github).create_repo = MagicMock()
        Github = MagicMock(return_value=github)
        type(self.admin_mock.github).Github = Github

        git_command = MagicMock()
        type(self.admin_mock.git).git_command = git_command

        push = MagicMock(return_value=-1)
        type(self.admin_mock.repository).push = push

        ### test ###
        self.assertEqual(-1, self.plugin.remote_create(args))
        mock_write.assert_any_call('# Creating Remote repository named test_name\n')
        mock_write.assert_any_call('## Set Username:"your_username" and Password:"your_token"\n')
        mock_write.assert_any_call('## Failed.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.user_pass')
    @mock.patch('sys.stdout.flush')
    def test_remote_create_3(self, mock_flush, mock_user_pass, mock_write, mock_parse_args):
        """remote_create repository success case"""
        rtc = self.get_rtc()

        args = ['./mgr.py', 'repository', 'remote_create', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_rtc_from_package = MagicMock(return_value=rtc)
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        repo = MagicMock()
        get_repository_from_rtc = MagicMock(return_value=repo)
        type(self.admin_mock.repository).get_repository_from_rtc = get_repository_from_rtc

        mock_user_pass.return_value = 'username', 'password', 'token'

        github = MagicMock()
        type(github).exists_repo = MagicMock(return_value=False)
        type(github).create_repo = MagicMock()
        Github = MagicMock(return_value=github)
        type(self.admin_mock.github).Github = Github

        git_command = MagicMock()
        type(self.admin_mock.git).git_command = git_command

        push = MagicMock(return_value=0)
        type(self.admin_mock.repository).push = push

        ### test ###
        self.assertEqual(0, self.plugin.remote_create(args))
        mock_write.assert_any_call('# Creating Remote repository named test_name\n')
        mock_write.assert_any_call('## Set Username:"your_username" and Password:"your_token"\n')
        mock_write.assert_any_call('## Success.\n')


if __name__ == '__main__':
    unittest.main()
