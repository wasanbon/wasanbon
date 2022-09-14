# test for wasanbon/core/plugins/mgr/admin_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import sys
sys.path.append('../../')

import wasanbon


class TestPlugin(unittest.TestCase):

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.mgr.admin_plugin as m
        self.admin_mock = MagicMock(spec=['repository', 'rtc', 'package', 'github', 'git', 'git'])
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()
        self.func = m

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.mgr.admin_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment',
                          'admin.repository',
                          'admin.rtc',
                          'admin.package',
                          'admin.github',
                          'admin.git'],
                         self.plugin.depends())

    @mock.patch('os.getcwd')
    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args', return_value=(None, None))
    def test_setting(self, mock_parse_args, mock_print, mock_getcwd):
        """setting normal case"""
        package = MagicMock()
        setattr(package, 'name', 'name')
        setattr(package, 'path', 'path')
        setattr(package, 'get_rtcpath', lambda fullpath: 'rtcpath')
        setattr(package, 'get_binpath', lambda fullpath: 'binpath')
        setattr(package, 'get_confpath', lambda fullpath: 'confpath')
        setattr(package, 'get_systempath', lambda fullpath: 'systempath')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)
        self.assertEqual(0, self.plugin.setting(['argv']))
        self.assertEqual(8, mock_print.call_count)

    @mock.patch('sys.stdout.write', return_value=True)
    def test_status_1(self, mock_write):
        """status normal case
        is_modified = True
        """
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=True)
        type(self.admin_mock.repository).is_modified = MagicMock(return_value=True)
        self.assertEqual(0, self.plugin.status(['argv']))
        mock_write.assert_any_call('  Modified\n')

    @mock.patch('sys.stdout.write', return_value=True)
    def test_status_2(self, mock_write):
        """status normal case
        is_untracked = True
        """
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=True)
        type(self.admin_mock.repository).is_modified = MagicMock(return_value=False)
        type(self.admin_mock.repository).is_untracked = MagicMock(return_value=True)
        self.assertEqual(0, self.plugin.status(['argv']))
        mock_write.assert_any_call('  Untracked files found\n')

    @mock.patch('sys.stdout.write', return_value=True)
    def test_status_3(self, mock_write):
        """status normal case
        is_added = True
        """
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=True)
        type(self.admin_mock.repository).is_modified = MagicMock(return_value=False)
        type(self.admin_mock.repository).is_untracked = MagicMock(return_value=False)
        type(self.admin_mock.repository).is_added = MagicMock(return_value=True)
        self.assertEqual(0, self.plugin.status(['argv']))
        mock_write.assert_any_call('  Added\n')

    @mock.patch('sys.stdout.write', return_value=True)
    def test_status_4(self, mock_write):
        """status normal case
        is_added = False
        """
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=True)
        type(self.admin_mock.repository).is_modified = MagicMock(return_value=False)
        type(self.admin_mock.repository).is_untracked = MagicMock(return_value=False)
        type(self.admin_mock.repository).is_added = MagicMock(return_value=False)
        self.assertEqual(0, self.plugin.status(['argv']))
        mock_write.assert_any_call('  Up-to-date\n')

    @mock.patch('sys.stdout.write', return_value=True)
    def test_status_exception(self, mock_write):
        """status exception case"""
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=None)
        with self.assertRaises(wasanbon.RepositoryNotFoundException):
            self.assertEqual(0, self.plugin.status(['argv']))
        mock_write.assert_any_call('name :\n')

    @mock.patch('os.path.join', return_value='join')
    @mock.patch('os.getcwd', return_value='getcwd')
    def test_fix_gitignore_1(self, mock_getcwd, mock_join):
        """fix_gitignore normal case
        check_dot_gitignore = True
        """
        p = MagicMock()
        setattr(p, 'path', 'path')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).check_dot_gitignore = MagicMock(return_value=True)
        type(self.admin_mock.repository).add = MagicMock()

        self.assertEqual(0, self.plugin.fix_gitignore(['args']))
        type(self.admin_mock.repository).add.assert_not_called()

    @mock.patch('os.path.join', return_value='join')
    @mock.patch('os.getcwd', return_value='getcwd')
    def test_fix_gitignore_2(self, mock_getcwd, mock_join):
        """fix_gitignore normal case
        check_dot_gitignore = False
        """
        p = MagicMock()
        setattr(p, 'path', 'path')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).check_dot_gitignore = MagicMock(return_value=False)
        type(self.admin_mock.repository).add = MagicMock()

        self.assertEqual(0, self.plugin.fix_gitignore(['args']))
        type(self.admin_mock.repository).add.assert_called_once()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.user_pass', return_value=('username', 'password', 'token'))
    @mock.patch('os.getcwd', return_value='getcwd')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_remote_create_1(self, mock_parse_args, mock_getcwd, mock_user_pass, mock_write):
        """remote_create normal case"""
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        setattr(options, 'username', 'username')
        setattr(options, 'password', 'password')
        setattr(options, 'token', 'token')
        mock_parse_args.return_value = options, None
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value='repo')
        github = MagicMock()
        setattr(github, 'exists_repo', lambda name: False)
        setattr(github, 'create_repo', lambda name: 'github_repo?')
        type(self.admin_mock.github).Github = MagicMock(return_value=github)
        type(self.admin_mock.git).git_command = MagicMock()
        type(self.admin_mock.repository).push = MagicMock(return_value=0)
        self.assertEqual(0, self.plugin.remote_create(['args']))

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.user_pass', return_value=('username', 'password', 'token'))
    @mock.patch('os.getcwd', return_value='getcwd')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_remote_create_2(self, mock_parse_args, mock_getcwd, mock_user_pass, mock_write):
        """remote_create normal case"""
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        setattr(options, 'username', 'username')
        setattr(options, 'password', 'password')
        setattr(options, 'token', 'token')
        mock_parse_args.return_value = options, None
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value='repo')
        github = MagicMock()
        setattr(github, 'exists_repo', lambda name: False)
        setattr(github, 'create_repo', lambda name: 'github_repo?')
        type(self.admin_mock.github).Github = MagicMock(return_value=github)
        type(self.admin_mock.git).git_command = MagicMock()
        type(self.admin_mock.repository).push = MagicMock(return_value=-1)
        self.assertEqual(-1, self.plugin.remote_create(['args']))
        mock_write.assert_any_call('## Failed.\n')

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.user_pass', return_value=('username', 'password', 'token'))
    @mock.patch('os.getcwd', return_value='getcwd')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_remote_create_3(self, mock_parse_args, mock_getcwd, mock_user_pass, mock_write):
        """remote_create normal case"""
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        setattr(options, 'username', 'username')
        setattr(options, 'password', 'password')
        setattr(options, 'token', 'token')
        mock_parse_args.return_value = options, None
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value='repo')
        github = MagicMock()
        setattr(github, 'exists_repo', lambda name: True)
        type(self.admin_mock.github).Github = MagicMock(return_value=github)
        self.assertEqual(-1, self.plugin.remote_create(['args']))
        mock_write.assert_any_call('## Error. Repository name already exists.\n')

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.user_pass', return_value=('username', 'password', 'token'))
    @mock.patch('os.getcwd', return_value='getcwd')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_remote_create_4(self, mock_parse_args, mock_getcwd, mock_user_pass, mock_write):
        """remote_create normal case"""
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        setattr(options, 'username', 'username')
        setattr(options, 'password', 'password')
        setattr(options, 'token', 'token')
        mock_parse_args.return_value = options, None
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=None)
        self.assertEqual(-1, self.plugin.remote_create(['args']))
        mock_write.assert_any_call('# Repository is not found.\n')

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.user_pass', return_value=('username', 'password', 'token'))
    @mock.patch('os.getcwd', return_value='getcwd')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_remote_create_5(self, mock_parse_args, mock_getcwd, mock_user_pass, mock_write):
        """remote_create normal case"""
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        setattr(options, 'username', 'username')
        setattr(options, 'password', 'password')
        setattr(options, 'token', 'token')
        mock_parse_args.return_value = options, None
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(side_effect=[wasanbon.RepositoryNotFoundException()])
        self.assertEqual(-1, self.plugin.remote_create(['args']))
        mock_write.assert_any_call('# Repository is not found.\n')

    @mock.patch('wasanbon.timestampstr')
    @mock.patch('yaml.dump')
    @mock.patch('os.rename')
    @mock.patch('builtins.open', return_value='file')
    @mock.patch('yaml.safe_load')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_sync(self, mock_parse_args, mock_safe_load, mock_open, mock_rename, mock_dump, mock_timestampstr):
        """sync normal case"""
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        mock_parse_args.return_value = options, None
        package = MagicMock()
        setattr(package, 'rtc_repository_file', 'rtc_reposiroty_file')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)
        mock_safe_load.return_value = {'repo_name': {'description': None, 'type': None, 'url': None, 'hash': None},
                                       'repo_name2': {'description': None, 'type': None, 'url': None, 'hash': None, 'repo_type': None}}
        repo = MagicMock()
        setattr(repo, 'name', 'repo_name')
        setattr(repo, 'type', 'repo_type')
        setattr(repo, 'url', 'repo_url')
        repo2 = MagicMock()
        setattr(repo2, 'name', 'repo_name2')
        setattr(repo2, 'type', 'repo_type')
        setattr(repo2, 'url', 'repo_url')
        setattr(repo2, 'repo_type', 'hoge')
        type(self.admin_mock.repository).get_rtc_repositories_from_package = MagicMock(return_value=[repo, repo2])
        rtc = MagicMock()
        setattr(rtc, 'rtcprofile', MagicMock())
        setattr(rtc.rtcprofile, 'basicInfo', MagicMock())
        setattr(rtc.rtcprofile.basicInfo, 'description', 'description')
        type(self.admin_mock.rtc).get_rtc_from_package = MagicMock(return_value=rtc)
        hashcode = MagicMock(spec=['decode'])
        hashcode.decode.return_value = 'hashcode'
        type(self.admin_mock.repository).get_repository_hash = MagicMock(return_value=hashcode)
        repo_dict = {'repo_name': {'description': 'description', 'type': 'repo_type', 'url': 'repo_url', 'hash': 'hashcode', 'name': 'repo_name'}, 
                    'repo_name2': {'description': 'description', 'type': 'repo_type', 'url': 'repo_url', 'hash': 'hashcode', 'name': 'repo_name2'}}
        ### check ###
        self.assertEqual(0, self.plugin.sync(['args']))
        mock_dump.assert_called_once_with(repo_dict, 'file', encoding='utf8', allow_unicode=True, default_flow_style=False)

    @mock.patch('os.getcwd', return_value='')
    @mock.patch('os.path.join', return_value='')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_git_init_1(self, mock_parse_args, mock_write, mock_path_join, mock_getcwd):
        """git_init normal case"""
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        mock_parse_args.return_value = options, None
        p = MagicMock()
        setattr(p, 'name', 'name')
        setattr(p, 'get_binpath', lambda: 'binpath')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=None)
        repo = MagicMock()
        setattr(repo, 'path', 'repo_path')
        type(self.admin_mock.repository).init_git_repository_to_path = MagicMock(return_value=repo)
        type(self.admin_mock.repository).add_files = MagicMock()
        type(self.admin_mock.repository).check_dot_gitignore = MagicMock(return_value=False)
        type(self.admin_mock.repository).add = MagicMock()
        type(self.admin_mock.repository).commit = MagicMock(return_value=0)

        ### check ###
        self.assertEqual(0, self.plugin.git_init(['args']))
        mock_write.assert_any_call('## Success\n')
        type(self.admin_mock.repository).add.assert_called_once()

    @mock.patch('os.getcwd', return_value='')
    @mock.patch('os.path.join', return_value='')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_git_init_2(self, mock_parse_args, mock_write, mock_path_join, mock_getcwd):
        """git_init error case
        repository exists already
        """
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        mock_parse_args.return_value = options, None
        p = MagicMock()
        setattr(p, 'name', 'name')
        setattr(p, 'get_binpath', lambda: 'binpath')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value='hoge')

        ### check ###
        self.assertEqual(-1, self.plugin.git_init(['args']))
        mock_write.assert_any_call('# Repository exists already.\n')

    @mock.patch('os.getcwd', return_value='')
    @mock.patch('os.path.join', return_value='')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_git_init_3(self, mock_parse_args, mock_write, mock_path_join, mock_getcwd):
        """git_init error case
        First commit faild
        """
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        mock_parse_args.return_value = options, None
        p = MagicMock()
        setattr(p, 'name', 'name')
        setattr(p, 'get_binpath', lambda: 'binpath')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value=None)
        repo = MagicMock()
        setattr(repo, 'path', 'repo_path')
        type(self.admin_mock.repository).init_git_repository_to_path = MagicMock(return_value=repo)
        type(self.admin_mock.repository).add_files = MagicMock()
        type(self.admin_mock.repository).check_dot_gitignore = MagicMock(return_value=True)
        type(self.admin_mock.repository).add = MagicMock()
        type(self.admin_mock.repository).commit = MagicMock(return_value=-1)

        ### check ###
        self.assertEqual(-1, self.plugin.git_init(['args']))
        mock_write.assert_any_call('## First Commit failed.\n')
        type(self.admin_mock.repository).add.assert_not_called()

    @mock.patch('os.getcwd', return_value='')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_commit_1(self, mock_parse_args, mock_write, mock_getcwd):
        """commit normal case
        push_flag = False
        """
        options = MagicMock()
        setattr(options, 'verbose_flag', False)
        setattr(options, 'push_flag', False)
        mock_parse_args.return_value = options, ['0', '1', '2', 'comment']
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value='repo')
        type(self.admin_mock.repository).commit = MagicMock(return_value=0)

        ### check ###
        self.assertEqual(0, self.plugin.commit(['args']))
        mock_write.assert_any_call('## Success.\n')

    @mock.patch('os.path.basename', return_value='package_name')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_commit_2(self, mock_parse_args, mock_write, mock_getcwd, mock_basename):
        """commit normal case
        push_flag = True
        """
        options = MagicMock()
        setattr(options, 'verbose_flag', False)
        setattr(options, 'push_flag', True)
        mock_parse_args.return_value = options, ['0', '1', '2', 'comment']
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value='repo')
        type(self.admin_mock.repository).commit = MagicMock(return_value=0)
        type(self.admin_mock.repository).push = MagicMock(return_value=0)
        communicate = MagicMock()
        communicate.return_value = b'output', 'stderr'
        p_branch = MagicMock()
        type(p_branch).communicate = communicate
        type(self.admin_mock.git).git_command = MagicMock(return_value=p_branch)

        ### check ###
        self.assertEqual(0, self.plugin.commit(['args']))
        mock_write.assert_any_call('# Pushing Package package_name\n')
        mock_write.assert_any_call('## Success.\n')

    @mock.patch('os.path.basename', return_value='package_name')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_commit_3(self, mock_parse_args, mock_write, mock_getcwd, mock_basename):
        """commit error case
        push_flag = True
        0 != admin.repository.push
        """
        options = MagicMock()
        setattr(options, 'verbose_flag', False)
        setattr(options, 'push_flag', True)
        mock_parse_args.return_value = options, ['0', '1', '2', 'comment']
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value='repo')
        type(self.admin_mock.repository).commit = MagicMock(return_value=0)
        type(self.admin_mock.repository).push = MagicMock(return_value=-1)
        communicate = MagicMock()
        communicate.return_value = b'output', 'stderr'
        p_branch = MagicMock()
        type(p_branch).communicate = communicate
        type(self.admin_mock.git).git_command = MagicMock(return_value=p_branch)

        ### check ###
        self.assertEqual(-1, self.plugin.commit(['args']))
        mock_write.assert_any_call('# Pushing Package package_name\n')
        mock_write.assert_any_call('## Failed.\n')

    @mock.patch('os.path.basename', return_value='package_name')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_commit_4(self, mock_parse_args, mock_write, mock_getcwd, mock_basename):
        """commit error case
        0 != admin.repository.commit
        """
        options = MagicMock()
        setattr(options, 'verbose_flag', False)
        setattr(options, 'push_flag', True)
        mock_parse_args.return_value = options, ['0', '1', '2', 'comment']
        p = MagicMock()
        setattr(p, 'name', 'name')
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=p)
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value='repo')
        type(self.admin_mock.repository).commit = MagicMock(return_value=-1)
        communicate = MagicMock()
        communicate.return_value = b'output', 'stderr'
        p_branch = MagicMock()
        type(p_branch).communicate = communicate
        type(self.admin_mock.git).git_command = MagicMock(return_value=p_branch)

        ### check ###
        self.assertEqual(-1, self.plugin.commit(['args']))
        mock_write.assert_any_call('## Failed.\n')

    @mock.patch('os.path.basename', return_value='package_name')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_push_1(self, mock_parse_args, mock_write, mock_getcwd, mock_basename):
        """push normal case"""
        options = MagicMock()
        setattr(options, 'verbose_flag', False)
        mock_parse_args.return_value = options, None
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value='repo')
        communicate = MagicMock()
        communicate.return_value = b'output', 'stderr'
        p_branch = MagicMock()
        type(p_branch).communicate = communicate
        type(self.admin_mock.git).git_command = MagicMock(return_value=p_branch)
        type(self.admin_mock.repository).push = MagicMock(return_value=0)

        ### check ###
        self.assertEqual(0, self.plugin.push(['args']))
        mock_write.assert_any_call('## Success.\n')

    @mock.patch('os.path.basename', return_value='package_name')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_push_2(self, mock_parse_args, mock_write, mock_getcwd, mock_basename):
        """push error case"""
        options = MagicMock()
        setattr(options, 'verbose_flag', False)
        mock_parse_args.return_value = options, None
        type(self.admin_mock.repository).get_repository_from_path = MagicMock(return_value='repo')
        communicate = MagicMock()
        communicate.return_value = b'output', 'stderr'
        p_branch = MagicMock()
        type(p_branch).communicate = communicate
        type(self.admin_mock.git).git_command = MagicMock(return_value=p_branch)
        type(self.admin_mock.repository).push = MagicMock(return_value=-1)

        ### check ###
        self.assertEqual(-1, self.plugin.push(['args']))
        mock_write.assert_any_call('## Failed.\n')


if __name__ == '__main__':
    unittest.main()
