# test for wasanbon/core/plugins/admin/repository_plugin/__init__.py Plugin class

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import io
import os


class TestPlugin(unittest.TestCase):

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.admin.repository_plugin as m
        self.admin_mock = MagicMock(
            spec=['environment', 'git', 'package', 'rtc', 'binder'])
        setattr(m, 'admin', self.admin_mock)

    def __make_plugin_instance(self):
        """make repository_plugin.Plugin instance"""
        from wasanbon.core.plugins.admin import repository_plugin
        return repository_plugin.Plugin()

    def test_init(self):
        """__init__ normal case"""
        self.__make_plugin_instance()

    def test_depends(self):
        """depends normal case"""
        inst = self.__make_plugin_instance()
        expected_ret = ['admin.environment',
                        'admin.package',
                        'admin.rtc',
                        'admin.git',
                        'admin.binder']
        self.assertEqual(expected_ret, inst.depends())

    @mock.patch('builtins.print')
    def test_list_package_repos(self, print_mock):
        """_list_package_repos normal case"""
        inst = self.__make_plugin_instance()
        # admin mock settings
        test_repo = 'test_repo'
        repo_mock = MagicMock()
        repo_mock.name = test_repo
        self.admin_mock.binder.get_package_repos.return_value = [repo_mock]
        # test
        inst._list_package_repos(None)
        print_mock.assert_called_once_with(test_repo)

    def test_list(self):
        """list normal case"""
        inst = self.__make_plugin_instance()
        # test
        test_args = ['a']
        inst.list(test_args)
        self.admin_mock.binder.packages.assert_called_once_with(test_args)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.clone_package')
    def test_clone_clone_success(self, clone_package_mock, sys_stdout_write):
        """clone normal case"""
        # mock patch settings
        clone_package_mock.return_value = 0
        # admin mock settings
        test_repo = 'test_repo'
        repo_mock = MagicMock()
        repo_mock.name = test_repo
        self.admin_mock.binder.get_package_repo.return_value = repo_mock
        # test
        inst = self.__make_plugin_instance()
        test_args = ['a', 'b', 'c', test_repo]
        ret = inst.clone(test_args)
        self.assertEqual(ret, 0)
        sys_calls = [
            call('# Cloning Package %s\n' % repo_mock.name),
            call('## Success.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.clone_package')
    def test_clone_clone_fail(self, clone_package_mock, sys_stdout_write):
        """clone fail to clone"""
        # mock patch settings
        clone_package_mock.return_value = -1
        # admin mock settings
        test_repo = 'test_repo'
        repo_mock = MagicMock()
        repo_mock.name = test_repo
        self.admin_mock.binder.get_package_repo.return_value = repo_mock
        # test
        inst = self.__make_plugin_instance()
        test_args = ['a', 'b', 'c', test_repo]
        ret = inst.clone(test_args)
        self.assertEqual(ret, -1)
        sys_calls = [
            call('# Cloning Package %s\n' % repo_mock.name),
            call('## Failed.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.clone_package')
    def test_clone_clone_execption(self, clone_package_mock, sys_stdout_write):
        """clone raise error while cloning"""
        # mock patch settings
        clone_package_mock.side_effect = Exception('test')
        # admin mock settings
        test_repo = 'test_repo'
        repo_mock = MagicMock()
        repo_mock.name = test_repo
        self.admin_mock.binder.get_package_repo.return_value = repo_mock
        # test
        inst = self.__make_plugin_instance()
        test_args = ['a', 'b', 'c', test_repo]
        ret = inst.clone(test_args)
        self.assertEqual(ret, -1)
        sys_calls = [
            call('# Cloning Package %s\n' % repo_mock.name),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.clone_package')
    def test_clone_clone_url_success(self, clone_package_mock, sys_stdout_write):
        """clone url specified"""
        # mock patch settings
        clone_package_mock.return_value = 0
        # admin mock settings
        test_repo = 'test_repo'
        repo_mock = MagicMock()
        repo_mock.name = test_repo
        self.admin_mock.binder.Repository.return_value = repo_mock
        # test
        inst = self.__make_plugin_instance()
        test_args = ['a', 'b', 'c', test_repo, '--url', 'd']
        ret = inst.clone(test_args)
        self.assertEqual(ret, 0)
        sys_calls = [
            call('# Cloning Package %s\n' % repo_mock.name),
            call('## Success.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.clone_package')
    def test_clone_clone_url_fail(self, clone_package_mock, sys_stdout_write):
        """clone url specified fail to clone"""
        # mock patch settings
        clone_package_mock.return_value = -1
        # admin mock settings
        test_repo = 'test_repo'
        repo_mock = MagicMock()
        repo_mock.name = test_repo
        self.admin_mock.binder.Repository.return_value = repo_mock
        # test
        inst = self.__make_plugin_instance()
        test_args = ['a', 'b', 'c', test_repo, '--url', 'd']
        ret = inst.clone(test_args)
        self.assertEqual(ret, -1)
        sys_calls = [
            call('# Cloning Package %s\n' % repo_mock.name),
            call('## Failed.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.clone_package')
    def test_clone_clone_url_execption(self, clone_package_mock, sys_stdout_write):
        """clone url specified raise error while cloning"""
        # mock patch settings
        clone_package_mock.side_effect = Exception('test')
        # admin mock settings
        test_repo = 'test_repo'
        repo_mock = MagicMock()
        repo_mock.name = test_repo
        self.admin_mock.binder.Repository.return_value = repo_mock
        # test
        inst = self.__make_plugin_instance()
        test_args = ['a', 'b', 'c', test_repo, '--url', 'd']
        ret = inst.clone(test_args)
        self.assertEqual(ret, -1)
        sys_calls = [
            call('# Cloning Package %s\n' % repo_mock.name),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('os.chdir')
    @mock.patch('wasanbon.platform')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_rtc_repositories_from_package')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.clone_rtc')
    def test_clone_package_with_branch(self, clone_rtc_mock, get_rtc_repos_mock, sys_stdout_write, platform_mock, _):
        """clone_package branch specified"""
        # mock patch settings
        clone_rtc_mock.return_value = 0
        get_rtc_repos_mock.return_value = ['test_repo']
        test_platform = 'test_platform'
        platform_mock.return_value = test_platform
        # admin mock settings
        repo_mock = MagicMock()
        test_branch = 'test1'
        repo_mock._platform = {test_platform: test_branch}
        self.admin_mock.package.get_package.return_value = repo_mock
        # test
        inst = self.__make_plugin_instance()
        ret = inst.clone_package(repo_mock, verbose=True)
        self.assertEqual(ret, 0)
        sys_calls = [
            call('# Cloning package %s\n' % repo_mock),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        git_calls = [
            call(['clone', '-b', test_branch, repo_mock.url,
                  repo_mock.basename], verbose=True)
        ]
        self.admin_mock.git.git_command.assert_has_calls(git_calls)

    @mock.patch('os.chdir')
    @mock.patch('wasanbon.platform')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_rtc_repositories_from_package')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.clone_rtc')
    def test_clone_package_without_branch_clone_fail(self, clone_rtc_mock, get_rtc_repos_mock, sys_stdout_write, platform_mock, _):
        """clone_package branch not specified, fail to clone"""
        # mock patch settings
        clone_rtc_mock.return_value = -1
        get_rtc_repos_mock.return_value = ['test_repo']
        test_platform = 'test_platform'
        platform_mock.return_value = test_platform
        # admin mock settings
        repo_mock = MagicMock()
        repo_mock._platform = {}
        self.admin_mock.package.get_package.return_value = repo_mock
        # test
        inst = self.__make_plugin_instance()
        ret = inst.clone_package(repo_mock, verbose=True)
        self.assertEqual(ret, -1)
        sys_calls = [
            call('# Cloning package %s\n' % repo_mock),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        git_calls = [
            call(['clone', repo_mock.url, repo_mock.basename], verbose=True)
        ]
        self.admin_mock.git.git_command.assert_has_calls(git_calls)

    @mock.patch('os.chdir')
    @mock.patch('wasanbon.platform')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_rtc_repositories_from_package')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.clone_rtc')
    def test_clone_package_without_branch_clone_error(self, clone_rtc_mock, get_rtc_repos_mock, sys_stdout_write, platform_mock, _):
        """clone_package branch not specified, raise Exception while cloning"""
        # mock patch settings
        clone_rtc_mock.side_effect = Exception('test')
        get_rtc_repos_mock.return_value = ['test_repo']
        test_platform = 'test_platform'
        platform_mock.return_value = test_platform
        # admin mock settings
        repo_mock = MagicMock()
        repo_mock._platform = {}
        self.admin_mock.package.get_package.return_value = repo_mock
        # test
        inst = self.__make_plugin_instance()
        with self.assertRaises(Exception):
            inst.clone_package(repo_mock, verbose=True)
        sys_calls = [
            call('# Cloning package %s\n' % repo_mock),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        git_calls = [
            call(['clone', repo_mock.url, repo_mock.basename], verbose=True)
        ]
        self.admin_mock.git.git_command.assert_has_calls(git_calls)

    @mock.patch('os.chdir')
    @mock.patch('wasanbon.platform')
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.hasattr')
    def test_clone_rtc_with_branch(self, has_attr_mock, sys_stdout_write, platform_mock, _):
        """clone_rtc branch not specified, fail to clone"""
        # mock patch settings
        has_attr_mock.return_value = True
        test_platform = 'test_platform'
        platform_mock.return_value = test_platform
        # admin mock settings
        repo_mock = MagicMock()
        repo_mock.name = 'repo'
        test_branch = 'test1'
        repo_mock._platform = {test_platform: test_branch}
        self.admin_mock.package.get_package.return_value = repo_mock
        process_mock = MagicMock()
        process_mock.returncode = 0
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        inst = self.__make_plugin_instance()
        ret = inst.clone_rtc(repo_mock, verbose=True)
        self.assertEqual(ret, 0)
        sys_stdout_write.assert_not_called()
        git_calls = [
            call(['clone', '-b', test_branch, repo_mock.url,
                  repo_mock.name], verbose=True),
            call(['checkout', repo_mock._rtc_hash], verbose=True)
        ]
        self.admin_mock.git.git_command.assert_has_calls(git_calls)

    @mock.patch('os.chdir')
    @mock.patch('wasanbon.platform')
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.hasattr')
    def test_clone_rtc_without_branch_clone_fail(self, has_attr_mock, sys_stdout_write, platform_mock, _):
        """clone_rtc branch not specified, fail to clone"""
        # mock patch settings
        has_attr_mock.return_value = True
        test_platform = 'test_platform'
        platform_mock.return_value = test_platform
        # admin mock settings
        repo_mock = MagicMock()
        repo_mock.name = 'repo'
        test_branch = 'test1'
        repo_mock._platform = {}
        self.admin_mock.package.get_package.return_value = repo_mock
        process_mock = MagicMock()
        process_mock.returncode = -1
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        inst = self.__make_plugin_instance()
        ret = inst.clone_rtc(repo_mock, verbose=True)
        self.assertEqual(ret, -1)
        sys_calls = [
            call('### Cloning RTC (%s) failed.\n' % repo_mock.name),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        git_calls = [
            call(['clone', repo_mock.url, repo_mock.name], verbose=True),
        ]
        self.admin_mock.git.git_command.assert_has_calls(git_calls)

    @mock.patch('os.chdir')
    @mock.patch('wasanbon.platform')
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.hasattr')
    def test_clone_rtc_without_branch_hash_error(self, has_attr_mock, sys_stdout_write, platform_mock, _):
        """clone_rtc branch not specified, no hash """
        # mock patch settings
        has_attr_mock.return_value = True
        test_platform = 'test_platform'
        platform_mock.return_value = test_platform
        # admin mock settings
        repo_mock = MagicMock()
        repo_mock.name = 'repo'
        repo_mock._platform = {}
        self.admin_mock.package.get_package.return_value = repo_mock
        process_mock1 = MagicMock()
        process_mock1.returncode = 0
        process_mock2 = MagicMock()
        process_mock2.returncode = -2
        self.admin_mock.git.git_command.side_effect = [
            process_mock1, process_mock2]
        # test
        inst = self.__make_plugin_instance()
        ret = inst.clone_rtc(repo_mock, verbose=True)
        self.assertEqual(ret, -2)
        sys_calls = [
            call('### Checkout hash RTC (%s) failed.\n' % repo_mock.name),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        git_calls = [
            call(['clone', repo_mock.url, repo_mock.name], verbose=True),
        ]
        self.admin_mock.git.git_command.assert_has_calls(git_calls)

    @mock.patch('os.chdir')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.platform')
    @mock.patch('sys.stdout.write')
    @mock.patch('yaml.safe_load')
    def test_get_rtc_repositories_from_package(self, yaml_load_mock, sys_stdout_write, platform_mock, open_mock, _):
        """get_rtc_repositories_from_package """
        # mock patch settings
        test_name1 = 'test_name1'
        test_name2 = 'test_name2'
        test_dict = {'git': 'test_git', 'url': 'test_url',
                     'type': 'test_type', 'hash': 'test_hash', 'description': 'test_desc'}
        yaml_dict = {test_name1: test_dict, test_name2: test_dict}
        yaml_load_mock.return_value = yaml_dict
        test_platform = 'test_platform'
        platform_mock.return_value = test_platform
        # admin mock settings
        repo_mock = MagicMock()
        self.admin_mock.binder.Repository.return_value = repo_mock
        # test
        inst = self.__make_plugin_instance()
        ret = inst.get_rtc_repositories_from_package(repo_mock, verbose=True)
        self.assertEqual(ret, [repo_mock, repo_mock])
        sys_calls = [
            call('# Loading Repository File from package(%s)\n' %
                 (repo_mock.name)),
            call('## Loading Repository (name=%s, url=%s)\n' %
                 (test_name1, test_dict['url'])),
            call('## Loading Repository (name=%s, url=%s)\n' %
                 (test_name2, test_dict['url'])),
        ]
        sys_stdout_write.assery_has_calls(sys_calls)
        get_rtc_calls = [call(repo_mock, test_name1),
                         call(repo_mock, test_name2)]
        self.admin_mock.rtc.get_rtc_from_package.assert_has_calls(
            get_rtc_calls)

    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_git_repository_from_rtc')
    def test_get_repository_from_rtc_git_exist(self, get_git_repository_from_rtc_mock, listdir_mock):
        """get_repository_from_rtc git exist """
        # mock patch settings
        listdir_mock.return_value = ['.git']
        test_repo = 'test_repo'
        get_git_repository_from_rtc_mock.return_value = test_repo
        # test
        rtc_mock = MagicMock()
        inst = self.__make_plugin_instance()
        ret = inst.get_repository_from_rtc(rtc_mock)
        self.assertEqual(ret, test_repo)

    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_git_repository_from_rtc')
    def test_get_repository_from_rtc_git_not_exist(self, get_git_repository_from_rtc_mock, listdir_mock):
        """get_repository_from_rtc git not exist """
        # mock patch settings
        listdir_mock.return_value = []
        # test
        rtc_mock = MagicMock()
        inst = self.__make_plugin_instance()
        ret = inst.get_repository_from_rtc(rtc_mock)
        self.assertEqual(ret, None)
        get_git_repository_from_rtc_mock.assert_not_called()

    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_git_repository_from_path')
    def test_get_repository_from_path_git_exist(self, get_git_repository_from_path_mock, listdir_mock):
        """get_repository_from_path git exist """
        # mock patch settings
        listdir_mock.return_value = ['.git']
        test_repo = 'test_repo'
        get_git_repository_from_path_mock.return_value = test_repo
        # test
        rtc_mock = MagicMock()
        inst = self.__make_plugin_instance()
        ret = inst.get_repository_from_path(rtc_mock)
        self.assertEqual(ret, test_repo)

    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_git_repository_from_path')
    def test_get_repository_from_path_git_not_exist(self, get_git_repository_from_path_mock, listdir_mock):
        """get_repository_from_path git not exist """
        # mock patch settings
        listdir_mock.return_value = []
        # test
        rtc_mock = MagicMock()
        inst = self.__make_plugin_instance()
        ret = inst.get_repository_from_path(rtc_mock)
        self.assertEqual(ret, None)
        get_git_repository_from_path_mock.assert_not_called()

    @mock.patch('wasanbon.platform')
    def test_get_git_repository_from_path(self, platform_mock):
        """get_git_repository_from_path """
        # mock patch settings
        test_platform = 'test_plattform'
        platform_mock.return_value = test_platform
        # admin mock settings
        repo_mock = MagicMock()
        self.admin_mock.binder.Repository.return_value = repo_mock
        process_mock = MagicMock()
        test_output = b'test_output.git'
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        inst = self.__make_plugin_instance()
        test_path = 'test_path'
        ret = inst.get_git_repository_from_path(test_path)
        self.assertEqual(ret, repo_mock)
        self.admin_mock.binder.Repository.assert_called_once_with(
            name=test_output.decode()[:-4],
            type='git',
            url=test_output,
            description='',
            platform=test_platform,
            path=test_path
        )

    @mock.patch('wasanbon.platform')
    def test_get_git_repository_from_rtc(self, platform_mock):
        """get_git_repository_from_rtc """
        # mock patch settings
        test_platform = 'test_plattform'
        platform_mock.return_value = test_platform
        # admin mock settings
        repo_mock = MagicMock()
        self.admin_mock.binder.Repository.return_value = repo_mock
        process_mock = MagicMock()
        test_output = 'test_output.git'
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        test_rtc = MagicMock()
        inst = self.__make_plugin_instance()
        ret = inst.get_git_repository_from_rtc(test_rtc)
        self.assertEqual(ret, repo_mock)
        self.admin_mock.binder.Repository.assert_called_once_with(
            name=test_rtc.rtcprofile.basicInfo.name,
            type='git',
            url=test_output,
            description=test_rtc.rtcprofile.basicInfo.description,
            platform=test_platform,
            path=test_rtc.path
        )

    def test_get_repository_hash(self):
        """get_repository_hash """
        # admin mock settings
        process_mock = MagicMock()
        test_output = 'test_output.git'
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        # test (git)
        test_repo = MagicMock()
        test_repo.type = 'git'
        inst = self.__make_plugin_instance()
        ret = inst.get_repository_hash(test_repo)
        self.assertEqual(ret, test_output)
        # test (not git)
        test_repo = MagicMock()
        test_repo.type = ''
        inst = self.__make_plugin_instance()
        ret = inst.get_repository_hash(test_repo)
        self.assertEqual(ret, None)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_git_repository_from_path')
    def test_init_git_repository_to_path_normal(self, get_git_repository_from_path_mock, sys_stdout_write):
        """init_git_repository_to_path normal"""
        # mock patch settings
        test_repo = 'test_repo'
        get_git_repository_from_path_mock.return_value = test_repo
        # admin mock settings
        process_mock = MagicMock()
        process_mock.returncode = 0
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        test_path = 'test_path'
        inst = self.__make_plugin_instance()
        ret = inst.init_git_repository_to_path(test_path, verbose=True)
        self.assertEqual(ret, test_repo)
        sys_calls = [
            call('# Initializing git repository to %s\n' % test_path),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_git_repository_from_path')
    def test_init_git_repository_to_path_error(self, get_git_repository_from_path_mock, sys_stdout_write):
        """init_git_repository_to_path error"""
        # admin mock settings
        process_mock = MagicMock()
        process_mock.returncode = -1
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        test_path = 'test_path'
        inst = self.__make_plugin_instance()
        ret = inst.init_git_repository_to_path(test_path, verbose=True)
        self.assertEqual(ret, None)
        sys_calls = [
            call('# Initializing git repository to %s\n' % test_path),
            call('## Error git command returns non zero value (%s)\n' %
                 process_mock.returncode)
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        get_git_repository_from_path_mock.assert_not_called()

    @mock.patch('os.path.isfile')
    def test_is_rtc_repo(self, isfile_mock):
        """is_rtc_repo """
        # mock patch settings
        isfile_mock.return_value = True
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        inst = self.__make_plugin_instance()
        ret = inst.is_rtc_repo(test_repo)
        self.assertTrue(ret)
        isfile_mock.assert_called_once_with(os.path.join(test_path, 'RTC.xml'))

    @mock.patch('builtins.open')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.is_rtc_repo')
    def test_add_default_dot_gitignore_is_rtc(self, is_rtc_repo_mock, open_mock):
        """add_default_dot_gitignore rtc """
        # mock patch settings
        is_rtc_repo_mock.return_value = True
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        inst = self.__make_plugin_instance()
        inst.default_dot_gitignore_rtc = 'a b'
        inst.add_default_dot_gitignore(test_repo)
        file_calls = [
            call(os.path.join(test_path, '.gitignore'), 'w'),
            call().write('a\n'),
            call().write('b\n')]
        open_mock.assert_has_calls(file_calls)

    @mock.patch('builtins.open')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.is_rtc_repo')
    def test_add_default_dot_gitignore_is_not_rtc(self, is_rtc_repo_mock, open_mock):
        """add_default_dot_gitignore not rtc """
        # mock patch settings
        is_rtc_repo_mock.return_value = False
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        inst = self.__make_plugin_instance()
        inst.default_dot_gitignore_package = 'a b'
        inst.add_default_dot_gitignore(test_repo)
        file_calls = [
            call(os.path.join(test_path, '.gitignore'), 'w'),
            call().write('a\n'),
            call().write('b\n')]
        open_mock.assert_has_calls(file_calls)

    @mock.patch('os.rename')
    @mock.patch('builtins.open')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.is_rtc_repo')
    def test_check_dot_gitignore_rtc(self, is_rtc_repo_mock, isfile_mock, sys_stdout_write, open_mock, rename_mock):
        """check_dot_gitignore rtc """
        # mock patch settings
        is_rtc_repo_mock.return_value = True
        isfile_mock.return_value = True
        file_mock1 = io.StringIO()
        file_mock1.write('a\n')
        file_mock1.seek(0)
        file_mock2 = MagicMock()
        open_mock.side_effect = [file_mock1, file_mock2]
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        inst = self.__make_plugin_instance()
        inst.default_dot_gitignore_rtc = 'a b'
        inst.check_dot_gitignore(test_repo, verbose=True)
        open_calls = [
            call(os.path.join(test_path, '.gitignore'), 'r'),
            call(os.path.join(test_path, '.gitignore'), 'w'),
        ]
        open_mock.assert_has_calls(open_calls)
        file2_calls = [call.write('a\n\n'), call.write('b\n'), call.close()]
        file_mock2.assert_has_calls(file2_calls)
        sys_calls = [
            call('## .gitignore found.\n'),
            call('### WARNING! .gitignore does not cover default options.\n'),
            call(' - %s\n' % 'b'),
            call('### Fixing automatically.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('os.rename')
    @mock.patch('builtins.open')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.is_rtc_repo')
    def test_check_dot_gitignore_is_not_rtc(self, is_rtc_repo_mock, isfile_mock, sys_stdout_write, open_mock, rename_mock):
        """check_dot_gitignore not rtc """
        # mock patch settings
        is_rtc_repo_mock.return_value = False
        isfile_mock.return_value = True
        file_mock1 = io.StringIO()
        file_mock1.write('a\n')
        file_mock1.seek(0)
        file_mock2 = MagicMock()
        open_mock.side_effect = [file_mock1, file_mock2]
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        inst = self.__make_plugin_instance()
        inst.default_dot_gitignore_package = 'a b'
        inst.check_dot_gitignore(test_repo, verbose=True)
        open_calls = [
            call(os.path.join(test_path, '.gitignore'), 'r'),
            call(os.path.join(test_path, '.gitignore'), 'w'),
        ]
        open_mock.assert_has_calls(open_calls)
        file2_calls = [call.write('a\n\n'), call.write('b\n'), call.close()]
        file_mock2.assert_has_calls(file2_calls)
        sys_calls = [
            call('## .gitignore found.\n'),
            call('### WARNING! .gitignore does not cover default options.\n'),
            call(' - %s\n' % 'b'),
            call('### Fixing automatically.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('os.rename')
    @mock.patch('builtins.open')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.add_default_dot_gitignore')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.is_rtc_repo')
    def test_check_dot_gitignore_no_gitignore(self, is_rtc_repo_mock, add_gitignore_mock, isfile_mock, sys_stdout_write, open_mock, rename_mock):
        """check_dot_gitignore gitignore file not exist """
        # mock patch settings
        is_rtc_repo_mock.return_value = False
        isfile_mock.return_value = False
        file_mock1 = io.StringIO()
        file_mock1.write('a\n')
        file_mock1.seek(0)
        file_mock2 = MagicMock()
        open_mock.side_effect = [file_mock1, file_mock2]
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        inst = self.__make_plugin_instance()
        inst.default_dot_gitignore_package = 'a b'
        inst.check_dot_gitignore(test_repo, verbose=True)
        open_mock.assert_not_called()
        sys_calls = [
            call('## No gitignore file in %s\n' % test_repo.name),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        add_gitignore_mock.assert_called_once_with(test_repo, True)

    @mock.patch('os.rename')
    @mock.patch('builtins.open')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.add_default_dot_gitignore')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.is_rtc_repo')
    def test_check_dot_gitignore_gitignore_check_ok(self, is_rtc_repo_mock, add_gitignore_mock, isfile_mock, sys_stdout_write, open_mock, rename_mock):
        """check_dot_gitignore existing gitignore has all items """
        # mock patch settings
        is_rtc_repo_mock.return_value = False
        isfile_mock.return_value = True
        file_mock1 = io.StringIO()
        file_mock1.write('a\nb\n')
        file_mock1.seek(0)
        file_mock2 = MagicMock()
        open_mock.side_effect = [file_mock1, file_mock2]
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        inst = self.__make_plugin_instance()
        inst.default_dot_gitignore_package = 'a b'
        inst.check_dot_gitignore(test_repo, verbose=True)
        open_calls = [
            call(os.path.join(test_path, '.gitignore'), 'r'),
        ]
        open_mock.assert_has_calls(open_calls)
        sys_calls = [
            call('### .gitignore covers default options.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        add_gitignore_mock.assert_not_called()

    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_status')
    def test_is_updated(self, get_status_mock):
        """is_updated """
        # mock patch settings
        get_status_mock.return_value = 'a modified'
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        inst = self.__make_plugin_instance()
        ret = inst.is_updated(test_repo)
        self.assertTrue(ret)

    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_status')
    def test_is_modified(self, get_status_mock):
        """is_modified """
        # mock patch settings
        get_status_mock.return_value = 'a modified'
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        inst = self.__make_plugin_instance()
        ret = inst.is_modified(test_repo)
        self.assertTrue(ret)

    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_status')
    def test_is_untracked(self, get_status_mock):
        """is_untracked """
        # mock patch settings
        get_status_mock.return_value = 'a Untracked'
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        inst = self.__make_plugin_instance()
        ret = inst.is_untracked(test_repo)
        self.assertTrue(ret)

    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.get_status')
    def test_is_added(self, get_status_mock):
        """is_added """
        # mock patch settings
        get_status_mock.return_value = 'a new file:'
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        inst = self.__make_plugin_instance()
        ret = inst.is_added(test_repo)
        self.assertTrue(ret)

    @mock.patch('sys.stdout.write')
    def test_get_status_local(self, sys_stdout_write):
        """get_status local"""
        # admin mock settings
        process_mock = MagicMock()
        test_output = b'test_output'
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        test_repo.type = 'git'
        test_repo.is_local.return_value = True
        inst = self.__make_plugin_instance()
        ret = inst.get_status(test_repo, verbose=True)
        self.assertEqual(ret, test_output.decode())
        sys_calls = [call(test_output.decode())]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    def test_get_status_not_local(self, sys_stdout_write):
        """get_status not_local"""
        # admin mock settings
        process_mock = MagicMock()
        test_output = b'test_output'
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        test_repo.type = 'git'
        test_repo.is_local.return_value = False
        inst = self.__make_plugin_instance()
        ret = inst.get_status(test_repo, verbose=True)
        self.assertEqual(ret, '')
        sys_calls = [call('# Given Repository is not local repository.\n')]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    def test_commit(self, sys_stdout_write):
        """commit """
        # admin mock settings
        process_mock = MagicMock()
        test_output = b'test_output'
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        test_repo.type = 'git'
        test_repo.is_local.return_value = False
        test_comment = 'test_comment'
        inst = self.__make_plugin_instance()
        ret = inst.commit(test_repo, test_comment, verbose=True)
        self.assertEqual(ret, 0)
        sys_calls = [call('## Committing GIT type repository (%s)\n' %
                          test_repo.name), call(test_output.decode())]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    def test_push(self, sys_stdout_write):
        """push """
        # admin mock settings
        process_mock = MagicMock()
        test_output = b'test_output'
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        test_repo.type = 'git'
        test_repo.is_local.return_value = False
        inst = self.__make_plugin_instance()
        ret = inst.push(test_repo, verbose=True)
        self.assertEqual(ret, process_mock.returncode)
        sys_calls = [call('## Pushing GIT type repository (%s)\n' %
                          test_repo.name), call(test_output.decode())]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    def test_pull(self, sys_stdout_write):
        """pull """
        # admin mock settings
        process_mock = MagicMock()
        test_output = b'test_output'
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        test_repo.type = 'git'
        test_repo.is_local.return_value = False
        inst = self.__make_plugin_instance()
        ret = inst.pull(test_repo, verbose=True)
        self.assertEqual(ret, process_mock.returncode)
        sys_calls = [call('## Pulling GIT type repository (%s)\n' %
                          test_repo.name), call(test_output.decode())]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    def test_add(self, sys_stdout_write):
        """add """
        # admin mock settings
        process_mock = MagicMock()
        test_output = b'test_output'
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        test_repo.type = 'git'
        test_repo.is_local.return_value = False
        test_file_list = 'test_file'
        inst = self.__make_plugin_instance()
        ret = inst.add(test_repo, test_file_list, verbose=True)
        self.assertEqual(ret, process_mock.returncode)
        sys_calls = [call('## Adding File to GIT type repository (%s)\n' %
                          test_repo.name), call(test_output.decode())]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    def test_add(self, sys_stdout_write):
        """add """
        # admin mock settings
        process_mock = MagicMock()
        test_output = b'test_output'
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        test_repo.type = 'git'
        test_repo.is_local.return_value = False
        test_file_list = 'test_file'
        inst = self.__make_plugin_instance()
        ret = inst.add(test_repo, test_file_list, verbose=True)
        self.assertEqual(ret, process_mock.returncode)
        sys_calls = [call('## Adding File to GIT type repository (%s)\n' %
                          test_repo.name), call(test_output.decode())]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isdir')
    @mock.patch('re.compile')
    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.add')
    def test_add_files_normal(self, add_mock, listdir_mock, re_compile_mock, isdir_mock, sys_stdout_write):
        """add_files normal """
        # mock patch settings
        listdir_mock.side_effect = [['test_dir1'], ['test_dir2'], []]
        re_compile_mock.match.return_value = False
        isdir_mock.return_value = True
        add_mock.return_value = 0
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        test_exclude_path = 'test_exclude'
        inst = self.__make_plugin_instance()
        ret = inst.add_files(
            test_repo, exclude_path=test_exclude_path, verbose=True)
        self.assertEqual(ret, None)
        sys_stdout_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isdir')
    @mock.patch('re.compile')
    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.admin.repository_plugin.Plugin.add')
    def test_add_files_fail(self, add_mock, listdir_mock, re_compile_mock, isdir_mock, sys_stdout_write):
        """add_files fail to add """
        # mock patch settings
        listdir_mock.side_effect = [['test_dir1'], ['test_dir2'], []]
        re_compile_mock.match.return_value = False
        isdir_mock.return_value = True
        add_mock.return_value = -1
        # test
        test_repo = MagicMock()
        test_path = 'test_path'
        test_repo.path = test_path
        test_exclude_path = 'test_exclude'
        inst = self.__make_plugin_instance()
        ret = inst.add_files(
            test_repo, exclude_path=test_exclude_path, verbose=True)
        self.assertEqual(ret, -1)
        sys_stdout_write.assert_called_once_with('## Add File failed.\n')


if __name__ == '__main__':
    unittest.main()
