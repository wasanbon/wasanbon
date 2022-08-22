# test for wasanbon/core/plugins/admin/binder_plugin/__init__.py Plugin class

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import os


class TestPlugin(unittest.TestCase):

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.admin.binder_plugin as m
        self.admin_mock = MagicMock(spec=['environment', 'git', 'github'])
        setattr(m, 'admin', self.admin_mock)

    def __make_plugin_instance(self):
        """make binder_plugin.Plugin instance"""
        from wasanbon.core.plugins.admin import binder_plugin
        return binder_plugin.Plugin()

    def test_init(self):
        """__init__ normal case"""
        self.__make_plugin_instance()

    def test_depends(self):
        """depends normal case"""
        inst = self.__make_plugin_instance()
        expected_ret = ['admin.environment', 'admin.git', 'admin.github']
        self.assertEqual(expected_ret, inst.depends())

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.owner_sign', new='test_owner')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.get_wasanbon_home')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.download_repository')
    @mock.patch('wasanbon.user_pass')
    def test_create_github_exist_repo(self, user_pass_mock, download_mock, wasanbon_home_mock, sys_stdout_write):
        """create normal [github] repository exist already"""
        # mock path settings
        test_home = 'test_home'
        wasanbon_home_mock.return_value = test_home
        test_user = 'test1'
        test_pass = 'test2'
        test_token = 'test3'
        user_pass_mock.return_value = (test_user, test_pass, test_token)
        # admin mock settings
        test_repo_url = 'test_url'
        Github_mock = MagicMock()
        Github_mock.exists_repo.return_value = True
        Github_mock.get_repo_url.return_value = test_repo_url
        self.admin_mock.github.Github.return_value = Github_mock
        inst = self.__make_plugin_instance()
        # test
        test_service = 'github'
        test_argv = ['-s', test_service, '-v']
        ret = inst.create(test_argv)
        self.assertEqual(ret, True)
        sys_calls = [
            call('# Creating wasanbon binder in your %s\n' % test_service),
            call(' @ You have already created your own repository.\n'),
            call(' @ wasanbon just clone it.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        target_path = os.path.join(
            test_home, 'binder', test_user + 'test_owner', 'wasanbon_binder.git')
        download_mock.assert_called_once_with(
            url=test_repo_url, target_path=target_path, verbose=True)

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.owner_sign', new='test_owner')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.get_wasanbon_home')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.download_repository')
    @mock.patch('wasanbon.user_pass')
    def test_create_github_not_exist_repo(self, user_pass_mock, download_mock, wasanbon_home_mock, sys_stdout_write):
        """create normal [github] repository not exist"""
        # mock path settings
        test_home = 'test_home'
        wasanbon_home_mock.return_value = test_home
        test_user = 'test1'
        test_pass = 'test2'
        test_token = 'test3'
        user_pass_mock.return_value = (test_user, test_pass, test_token)
        # admin mock settings
        test_repo_url = 'test_url'
        Github_mock = MagicMock()
        Github_mock.exists_repo.return_value = False
        Github_mock.fork_repo.return_value = None
        Github_mock.get_repo_url.return_value = test_repo_url
        self.admin_mock.github.Github.return_value = Github_mock
        inst = self.__make_plugin_instance()
        # test
        test_service = 'github'
        test_argv = ['-s', test_service, '-v']
        ret = inst.create(test_argv)
        self.assertEqual(ret, 0)
        sys_calls = [
            call('# Creating wasanbon binder in your %s\n' % test_service),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        download_mock.assert_not_called()

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.owner_sign', new='test_owner')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.get_wasanbon_home')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.download_repository')
    @mock.patch('wasanbon.user_pass')
    def test_create_not_github(self, user_pass_mock, download_mock, wasanbon_home_mock, sys_stdout_write):
        """create normal [not github]"""
        # mock path settings
        test_home = 'test_home'
        wasanbon_home_mock.return_value = test_home
        test_user = 'test1'
        test_pass = 'test2'
        test_token = 'test3'
        user_pass_mock.return_value = (test_user, test_pass, test_token)
        # admin mock settings
        test_repo_url = 'test_url'
        Github_mock = MagicMock()
        Github_mock.exists_repo.return_value = False
        Github_mock.fork_repo.return_value = None
        Github_mock.get_repo_url.return_value = test_repo_url
        self.admin_mock.github.Github.return_value = Github_mock
        inst = self.__make_plugin_instance()
        # test
        test_service = 'test_service'
        test_argv = ['-s', test_service, '-v']
        ret = inst.create(test_argv)
        self.assertEqual(ret, -1)
        sys_calls = [
            call('# Creating wasanbon binder in your %s\n' % test_service),
            call('## Unknown service name.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        download_mock.assert_not_called()

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.owner_sign', new='test_owner')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.get_wasanbon_home')
    @mock.patch('wasanbon.util.yes_no')
    @mock.patch('wasanbon.user_pass')
    def test_delete_github_delete_abort(self, user_pass_mock, yes_no_mock, wasanbon_home_mock, sys_stdout_write):
        """delete normal [github] abort to delete repository"""
        # mock path settings
        yes_no_mock.return_value = 'no'
        test_home = 'test_home'
        wasanbon_home_mock.return_value = test_home
        test_user = 'test1'
        test_pass = 'test2'
        test_token = 'test3'
        user_pass_mock.return_value = (test_user, test_pass, test_token)
        # admin mock settings
        test_repo_url = 'test_url'
        Github_mock = MagicMock()
        Github_mock.exists_repo.return_value = True
        Github_mock.fork_repo.return_value = None
        Github_mock.get_repo_url.return_value = test_repo_url
        self.admin_mock.github.Github.return_value = Github_mock
        inst = self.__make_plugin_instance()
        # test
        test_service = 'github'
        test_argv = ['-s', test_service, '-v']
        ret = inst.delete(test_argv)
        self.assertEqual(ret, 0)
        sys_calls = [
            call('# Deleting wasanbon binder in your %s\n' % test_service),
            call('## Aborted.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.owner_sign', new='test_owner')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.get_wasanbon_home')
    @mock.patch('wasanbon.util.yes_no')
    @mock.patch('wasanbon.user_pass')
    def test_delete_github_delete(self, user_pass_mock, yes_no_mock, wasanbon_home_mock, sys_stdout_write):
        """delete normal [github] delete repository"""
        # mock path settings
        yes_no_mock.return_value = 'yes'
        test_home = 'test_home'
        wasanbon_home_mock.return_value = test_home
        test_user = 'test1'
        test_pass = 'test2'
        test_token = 'test3'
        user_pass_mock.return_value = (test_user, test_pass, test_token)
        # admin mock settings
        test_repo_url = 'test_url'
        Github_mock = MagicMock()
        Github_mock.exists_repo.return_value = True
        Github_mock.get_repo_url.return_value = test_repo_url
        self.admin_mock.github.Github.return_value = Github_mock
        inst = self.__make_plugin_instance()
        # test
        test_service = 'github'
        test_argv = ['-s', test_service, '-v']
        ret = inst.delete(test_argv)
        self.assertEqual(ret, 0)
        sys_calls = [
            call('# Deleting wasanbon binder in your %s\n' % test_service),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        Github_mock.delete_repo.assert_called_once()

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.owner_sign', new='test_owner')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.get_wasanbon_home')
    @mock.patch('wasanbon.util.yes_no')
    @mock.patch('wasanbon.user_pass')
    def test_delete_not_github(self, user_pass_mock, yes_no_mock, wasanbon_home_mock, sys_stdout_write):
        """delete normal [not github]"""
        # mock path settings
        test_home = 'test_home'
        wasanbon_home_mock.return_value = test_home
        test_user = 'test1'
        test_pass = 'test2'
        test_token = 'test3'
        user_pass_mock.return_value = (test_user, test_pass, test_token)
        # admin mock settings
        test_repo_url = 'test_url'
        Github_mock = MagicMock()
        Github_mock.exists_repo.return_value = False
        Github_mock.fork_repo.return_value = None
        Github_mock.get_repo_url.return_value = test_repo_url
        self.admin_mock.github.Github.return_value = Github_mock
        inst = self.__make_plugin_instance()
        # test
        test_service = 'test_service'
        test_argv = ['-s', test_service, '-v']
        ret = inst.delete(test_argv)
        self.assertEqual(ret, -1)
        sys_calls = [
            call('# Deleting wasanbon binder in your %s\n' % test_service),
            call('# Unknown service name %s\n' % test_service),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        yes_no_mock.assert_not_called()

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.download_repositories')
    def test_update(self, download_mock):
        """update normal """
        # admin mock settings
        test_setting_path = 'test_path'
        self.admin_mock.environment.setting_path = test_setting_path
        inst = self.__make_plugin_instance()
        # test
        test_argv = ['-v']
        inst.update(test_argv)
        path = os.path.join(test_setting_path, '..', 'repository.yaml')
        download_mock.assert_called_once_with(path, verbose=True)

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_list(self, get_binders_mock, print_mock):
        """list normal """
        # mock settings
        test_owner = 'test_owner'
        test_path = 'test_path'
        binder_mock = MagicMock()
        binder_mock.owner = test_owner
        binder_mock.path = test_path
        get_binders_mock.return_value = [binder_mock]
        inst = self.__make_plugin_instance()
        # test
        test_argv = ['-v']
        inst.list(test_argv)
        print_calls = [
            call(test_owner, ' :'),
            call('  url : ', test_path),
        ]
        print_mock.assert_has_calls(print_calls)

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_rtcs_not_long(self, get_binders_mock, print_mock):
        """rtcs normal no --long option"""
        # mock settings
        rtc_mock = MagicMock()
        test_owner = 'test_owner'
        test_path = 'test_path'
        binder_mock = MagicMock()
        binder_mock.owner = test_owner
        binder_mock.path = test_path
        binder_mock.rtcs = [rtc_mock]
        get_binders_mock.return_value = [binder_mock]
        inst = self.__make_plugin_instance()
        # test
        test_argv = ['']
        inst.rtcs(test_argv)
        print_calls = [
            call(' - %s' % rtc_mock.name),
        ]
        print_mock.assert_has_calls(print_calls)

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_rtcs_long(self, get_binders_mock, print_mock):
        """rtcs normal --long """
        # mock settings
        rtc_mock = MagicMock()
        test_owner = 'test_owner'
        test_path = 'test_path'
        binder_mock = MagicMock()
        binder_mock.owner = test_owner
        binder_mock.path = test_path
        binder_mock.rtcs = [rtc_mock]
        get_binders_mock.return_value = [binder_mock]
        inst = self.__make_plugin_instance()
        # test
        test_argv = ['-l']
        inst.rtcs(test_argv)
        print_calls = [
            call('%s :' % rtc_mock.name),
            call('  %s : %s' % ('url', rtc_mock.url)),
            call('  %s : %s' % ('type', rtc_mock.type)),
            call('  %s : "%s"' % ('description', rtc_mock.description)),
            call('  %s : %s' % ('platform', rtc_mock.platform))
        ]
        print_mock.assert_has_calls(print_calls)

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_packages_no_long(self, get_binders_mock, print_mock):
        """packages normal no --long option """
        # mock settings
        package_mock = MagicMock()
        test_owner = 'test_owner'
        test_path = 'test_path'
        binder_mock = MagicMock()
        binder_mock.owner = test_owner
        binder_mock.path = test_path
        binder_mock.packages = [package_mock]
        get_binders_mock.return_value = [binder_mock]
        inst = self.__make_plugin_instance()
        # test
        test_argv = ['']
        inst.packages(test_argv)
        print_calls = [
            call(' - %s' % package_mock.name),
        ]
        print_mock.assert_has_calls(print_calls)

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_packages_long(self, get_binders_mock, print_mock):
        """packages normal --long """
        # mock settings
        package_mock = MagicMock()
        test_owner = 'test_owner'
        test_path = 'test_path'
        binder_mock = MagicMock()
        binder_mock.owner = test_owner
        binder_mock.path = test_path
        binder_mock.packages = [package_mock]
        get_binders_mock.return_value = [binder_mock]
        inst = self.__make_plugin_instance()
        # test
        test_argv = ['-l']
        inst.packages(test_argv)
        print_calls = [
            call('%s :' % package_mock.name),
            call('  %s : %s' % ('url', package_mock.url)),
            call('  %s : %s' % ('type', package_mock.type)),
            call('  %s : %s' % ('description', package_mock.description)),
            call('  %s : %s' % ('platform', package_mock.platform))
        ]
        print_mock.assert_has_calls(print_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.Plugin.get_binder')
    def test_commit_push_success(self, get_binder_mock, sys_stdout_write):
        """commit success to push"""
        # mock settings
        binder_mock = MagicMock()
        get_binder_mock.return_value = binder_mock
        # admin mock settings
        test_output = b'test_output'
        process_mock = MagicMock()
        process_mock.returncode = 0
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        inst = self.__make_plugin_instance()
        # test
        test_binder_name = 'test_binder'
        test_comment = 'test_comment'
        test_argv = ['a', 'b', 'c', test_binder_name, test_comment, '-v', '-p']
        inst.commit(test_argv)
        sys_calls = [
            call('# Committing binder %s to local repository\n' %
                 test_binder_name),
            call(test_output.decode()),
            call('## Success.\n'),
            call('# Pushing binder %s\n' % test_binder_name),
            call(test_output.decode()),
            call('## Success.\n')
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.Plugin.get_binder')
    def test_commit_push_fail(self, get_binder_mock, sys_stdout_write):
        """commit fail to push"""
        # mock settings
        binder_mock = MagicMock()
        get_binder_mock.return_value = binder_mock
        # admin mock settings
        test_output = b'test_output'
        process_mock = MagicMock()
        process_mock.returncode = -1
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        inst = self.__make_plugin_instance()
        # test
        test_binder_name = 'test_binder'
        test_comment = 'test_comment'
        test_argv = ['a', 'b', 'c', test_binder_name, test_comment, '-v', '-p']
        inst.commit(test_argv)
        sys_calls = [
            call('# Committing binder %s to local repository\n' %
                 test_binder_name),
            call(test_output.decode()),
            call('## Success.\n'),
            call('# Pushing binder %s\n' % test_binder_name),
            call(test_output.decode()),
            call('## Failed.\n')
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.Plugin.get_binder')
    def test_commit_no_commit(self, get_binder_mock, sys_stdout_write):
        """commit nothing to commit"""
        # mock settings
        binder_mock = MagicMock()
        get_binder_mock.return_value = binder_mock
        # admin mock settings
        test_output = b'Your branch is up to date'
        process_mock = MagicMock()
        process_mock.returncode = 0
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        inst = self.__make_plugin_instance()
        # test
        test_binder_name = 'test_binder'
        test_comment = 'test_comment'
        test_argv = ['a', 'b', 'c', test_binder_name, test_comment, '-v', '-p']
        inst.commit(test_argv)
        sys_calls = [
            call('# Committing binder %s to local repository\n' %
                 test_binder_name),
            call(test_output.decode()),
            call('## Changes are not staged yet.\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_get_binders(self, get_binders_mock):
        """get_binders """
        # mock settings
        binder_mock = MagicMock()
        get_binders_mock.return_value = binder_mock
        inst = self.__make_plugin_instance()
        # test
        self.assertEqual(inst.get_binders(), binder_mock)

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_get_binder_found(self, get_binders_mock):
        """get_binder found binder"""
        # mock settings
        test_binder_name = 'test_binder_name'
        binder_mock = MagicMock()
        binder_mock.owner = test_binder_name
        get_binders_mock.return_value = [binder_mock]
        inst = self.__make_plugin_instance()
        # test
        ret = inst.get_binder(test_binder_name)
        self.assertEqual(ret, binder_mock)

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_get_binder_not_found(self, get_binders_mock):
        """get_binder not found"""
        # mock settings
        test_binder_name = 'test_binder_name'
        binder_mock = MagicMock()
        binder_mock.owner = test_binder_name
        get_binders_mock.return_value = [binder_mock]
        inst = self.__make_plugin_instance()
        # test
        ret = inst.get_binder('aaaa')
        self.assertEqual(ret, None)

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_package_repos')
    def test_get_package_repos(self, get_package_repos_mock):
        """get_binder """
        # mock settings
        test_binder_name = 'test_binder_name'
        repo_mock = MagicMock()
        repo_mock.owner = test_binder_name
        get_package_repos_mock.return_value = [repo_mock]
        inst = self.__make_plugin_instance()
        # test
        ret = inst.get_package_repos()
        self.assertEqual(ret, [repo_mock])

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_get_rtc_repos(self, get_binders_mock):
        """get_rtc_repos """
        # mock settings
        rtc_mock = MagicMock()
        binder_mock = MagicMock()
        binder_mock.rtcs = [rtc_mock]
        get_binders_mock.return_value = [binder_mock]
        inst = self.__make_plugin_instance()
        # test
        ret = inst.get_rtc_repos()
        self.assertEqual(ret, [rtc_mock])

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_get_rtc_repo(self, get_binders_mock):
        """get_rtc_repo """
        # mock settings
        test_repo_name = 'test_repo_name'
        rtc_mock = MagicMock()
        rtc_mock.name = test_repo_name
        binder_mock = MagicMock()
        binder_mock.rtcs = [rtc_mock]
        get_binders_mock.return_value = [binder_mock]
        inst = self.__make_plugin_instance()
        # test
        ret = inst.get_rtc_repo(test_repo_name)
        self.assertEqual(ret, rtc_mock)

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_package_repo')
    def test_get_package_repo(self, get_package_repo_mock):
        """get_package_repo """
        # mock settings
        binder_mock = MagicMock()
        get_package_repo_mock.return_value = [binder_mock]
        inst = self.__make_plugin_instance()
        # test
        ret = inst.get_package_repo('repo')
        self.assertEqual(ret, [binder_mock])

    def test_Repository(self):
        """Repository """
        inst = self.__make_plugin_instance()
        # test
        test_name = 'test_name'
        test_type = 'test_type'
        test_platform = 'test_platform'
        test_url = 'test_url'
        test_desc = 'test_desc'
        ret = inst.Repository(test_name, test_type,
                              test_platform, test_url, test_desc)
        from wasanbon.core.plugins.admin import binder_plugin
        self.assertIsInstance(ret, binder_plugin.Repository)

    def test_Repository__init__(self):
        """Repository.__init__ & no logic properties """
        from wasanbon.core.plugins.admin import binder_plugin
        # test
        test_name = 'test_name'
        test_type = 'test_type'
        test_platform = 'test_platform'
        test_url = 'test_url'
        test_desc = 'test_desc'
        inst = binder_plugin.Repository(
            test_name, test_type, test_platform, test_url, test_desc)
        self.assertEqual(inst._name, test_name)
        self.assertEqual(inst.name, test_name)
        self.assertEqual(inst._url, test_url)
        self.assertEqual(inst._url, test_url)
        self.assertEqual(inst._type, test_type)
        self.assertEqual(inst.type, test_type)
        self.assertEqual(inst._platform, test_platform)
        self.assertEqual(inst.platform, test_platform)
        self.assertEqual(inst._description, test_desc)
        self.assertEqual(inst.description, test_desc)
        self.assertEqual(inst._path, None)
        self.assertEqual(inst.path, None)
        self.assertEqual(inst.hash, '')

    def test_Repository_hash(self):
        """Repository hash properties """
        # admin mock settings
        test_output = 'test_output'
        process_mock = MagicMock()
        process_mock.stdout.readline.return_value = test_output
        process_mock.communicate.return_value = (test_output, None)
        self.admin_mock.git.git_command.return_value = process_mock
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        test_name = 'test_name'
        test_type = 'git'
        test_platform = 'test_platform'
        test_url = 'test_url'
        test_desc = 'test_desc'
        inst = binder_plugin.Repository(
            test_name, test_type, test_platform, test_url, test_desc)
        self.assertEqual(inst.hash, test_output[1:-1])

    def test_Repository_basename(self):
        """Repository basename properties """
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        test_name = 'test_name'
        test_type = 'git'
        test_platform = 'test_platform'
        test_url = 'test_url.git'
        test_desc = 'test_desc'
        inst = binder_plugin.Repository(
            test_name, test_type, test_platform, test_url, test_desc)
        self.assertEqual(inst.basename, test_url[:-4])

    def test_Repository_service(self):
        """Repository service properties """
        # test (without @)
        from wasanbon.core.plugins.admin import binder_plugin
        test_name = 'test_name'
        test_type = 'git'
        test_platform = 'test_platform'
        test_service = 'test_service'
        test_url = 'test_url/aaa/bbb/{}./'.format(test_service)
        test_desc = 'test_desc'
        inst = binder_plugin.Repository(
            test_name, test_type, test_platform, test_url, test_desc)
        self.assertEqual(inst.service, test_service)
        # test (with @)
        test_url = 'test_url/aaa/bbb/ccc@{}./'.format(test_service)
        inst._url = test_url
        self.assertEqual(inst.service, test_service)

    @mock.patch('os.listdir')
    def test_Binder__init__(self, listdir_mock):
        """Binder.__init__ & no logic properties """
        # mock settings
        test_yaml = 'test_yaml'
        listdir_mock.return_value = [test_yaml]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        test_owner = 'test_owner'
        test_path = 'test_path'
        inst = binder_plugin.Binder(test_owner, test_path)
        self.assertEqual(inst._owner, test_owner)
        self.assertEqual(inst.owner, test_owner)
        self.assertEqual(inst._path, test_path)
        self.assertEqual(inst.path, test_path)
        self.assertEqual(inst._rtcs, None)
        self.assertEqual(inst._packages, None)
        self.assertEqual(inst.rtcs_path, os.path.join(test_path, 'rtcs'))
        self.assertEqual(inst.packages_path,
                         os.path.join(test_path, 'packages'))
        self.assertEqual(inst.rtc_files, [test_yaml])
        self.assertEqual(inst.package_files, [test_yaml])

    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('os.listdir')
    def test_Binder_rtcs(self, listdir_mock, yaml_load_mock, _):
        """Binder rtcs properties """
        # mock settings
        test_repo_name = 'test1'
        test_desc = 'test1_desc'
        test_type = 'test1_type'
        test_platform = 'test1_platform'
        test_url = 'test1_url'
        yaml_dict = {
            test_repo_name: {'description': test_desc,
                             'type': test_type,
                             'platform': test_platform,
                             'url': test_url}
        }
        yaml_load_mock.return_value = yaml_dict
        test_yaml = 'test_yaml'
        listdir_mock.return_value = ['dummy', test_yaml]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        test_owner = 'test_owner'
        test_path = 'test_path'
        inst = binder_plugin.Binder(test_owner, test_path)
        repo = inst.rtcs[0]
        self.assertIsInstance(repo, binder_plugin.Repository)
        self.assertEqual(repo._name, test_repo_name)
        self.assertEqual(repo._url, test_url)
        self.assertEqual(repo._type, test_type)
        self.assertEqual(repo._platform, test_platform)
        self.assertEqual(repo._description, test_desc)

    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('os.listdir')
    def test_Binder_packages(self, listdir_mock, yaml_load_mock, _):
        """Binder packages properties """
        # mock settings
        test_repo_name = 'test1'
        test_desc = 'test1_desc'
        test_type = 'test1_type'
        test_platform = 'test1_platform'
        test_url = 'test1_url'
        yaml_dict = {
            test_repo_name: {'description': test_desc,
                             'type': test_type,
                             'platform': test_platform,
                             'url': test_url}
        }
        yaml_load_mock.return_value = yaml_dict
        test_yaml = 'test_yaml'
        listdir_mock.return_value = ['dummy', test_yaml]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        test_owner = 'test_owner'
        test_path = 'test_path'
        inst = binder_plugin.Binder(test_owner, test_path)
        repo = inst.packages[0]
        self.assertIsInstance(repo, binder_plugin.Repository)
        self.assertEqual(repo._name, test_repo_name)
        self.assertEqual(repo._url, test_url)
        self.assertEqual(repo._type, test_type)
        self.assertEqual(repo._platform, test_platform)
        self.assertEqual(repo._description, test_desc)

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_get_package_repos(self, get_binders_mock):
        """get_package_repos """
        # mock settings
        packages_mock = MagicMock()
        binder_mock = MagicMock()
        binder_mock.packages = [packages_mock]
        get_binders_mock.return_value = [binder_mock]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        ret = binder_plugin.get_package_repos()
        self.assertEqual(ret, [packages_mock])

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_get_package_repo_found(self, get_binders_mock):
        """get_package_repo found"""
        test_repo_name = 'test_repo'
        # mock settings
        packages_mock = MagicMock()
        packages_mock.name = test_repo_name
        binder_mock = MagicMock()
        binder_mock.packages = [packages_mock]
        get_binders_mock.return_value = [binder_mock]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        ret = binder_plugin.get_package_repo(test_repo_name)
        self.assertEqual(ret, packages_mock)

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_get_package_repo_not_found(self, get_binders_mock):
        """get_package_repo not_found"""
        test_repo_name = 'test_repo'
        # mock settings
        packages_mock = MagicMock()
        packages_mock.name = test_repo_name
        binder_mock = MagicMock()
        binder_mock.packages = [packages_mock]
        get_binders_mock.return_value = [binder_mock]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        import wasanbon
        with self.assertRaises(wasanbon.RepositoryNotFoundException):
            binder_plugin.get_package_repo('aaaa')

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_get_rtc_repos(self, get_binders_mock):
        """get_rtc_repos """
        test_repo_name = 'test_repo'
        # mock settings
        rtcs_mock = MagicMock()
        rtcs_mock.name = test_repo_name
        binder_mock = MagicMock()
        binder_mock.rtcs = [rtcs_mock]
        get_binders_mock.return_value = [binder_mock]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        ret = binder_plugin.get_rtc_repos()
        self.assertEqual(ret, [rtcs_mock])

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_get_rtc_repo_found(self, get_binders_mock):
        """get_rtc_repo found"""
        test_repo_name = 'test_repo'
        # mock settings
        rtcs_mock = MagicMock()
        rtcs_mock.name = test_repo_name
        binder_mock = MagicMock()
        binder_mock.rtcs = [rtcs_mock]
        get_binders_mock.return_value = [binder_mock]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        ret = binder_plugin.get_rtc_repo(test_repo_name)
        self.assertEqual(ret, rtcs_mock)

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_binders')
    def test_get_rtc_repo_not_found(self, get_binders_mock):
        """get_rtc_repo not found"""
        test_repo_name = 'test_repo'
        # mock settings
        rtcs_mock = MagicMock()
        rtcs_mock.name = test_repo_name
        binder_mock = MagicMock()
        binder_mock.rtcs = [rtcs_mock]
        get_binders_mock.return_value = [binder_mock]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        import wasanbon
        with self.assertRaises(wasanbon.RepositoryNotFoundException):
            binder_plugin.get_rtc_repo('aaaa')

    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.repository_path')
    def test_get_binders(self, repository_path_mock, listdir_mock):
        """get_binders """
        # mock settings
        test_path = 'test_path'
        repository_path_mock.return_value = test_path
        test_yaml = 'setting.yaml'
        listdir_mock.return_value = [test_yaml]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        ret = binder_plugin.get_binders()
        binder = ret[0]
        self.assertIsInstance(binder, binder_plugin.Binder)
        self.assertEqual(binder.owner, test_yaml)
        self.assertEqual(binder.path, os.path.join(
            test_path, test_yaml, test_yaml))

    @mock.patch('wasanbon.home_path', new='test_path')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    def test_get_default_repo_directory(self, isdir_mock, mkdir_mock):
        """get_default_repo_directory"""
        # mock settings
        isdir_mock.return_value = False
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        ret = binder_plugin.get_default_repo_directory()
        path = os.path.join('test_path', 'binder')
        self.assertEqual(ret, path)
        mkdir_mock.assert_called_once_with(path)

    @mock.patch('builtins.open')
    @mock.patch('sys.stdout.write')
    @mock.patch('yaml.safe_load')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.download_repository')
    def test_download_repositories(self, download_repository_mock, yaml_load_mock, sys_stdout_mock, _):
        """download_repositories """
        # mock settings
        test_name = 'test_name'
        test_url = 'test_url'
        test_ymal = {test_name: {'url': test_url}}
        yaml_load_mock.return_value = test_ymal
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        test_setting_file = 'test_setting'
        binder_plugin.download_repositories(test_setting_file, True)
        sys_calls = [
            call(' - Downloading Repositories....\n'),
            call('    - Opening setting file in %s\n' % test_setting_file),
        ]
        sys_stdout_mock.assert_has_calls(sys_calls)
        download_repository_mock.assert_called_once_with(
            test_url, verbose=True, force=False)

    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.get_default_repo_directory')
    def test_repository_path(self, get_default_repo_directory_mock):
        """repository_path """
        # mock settings
        test_root = 'test_root'
        get_default_repo_directory_mock.return_value = test_root
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        test_url = 'test_url'
        url = '/{}/aaa'.format(test_url)
        ret = binder_plugin.repository_path(url)
        self.assertEqual(ret, os.path.join(test_root, test_url))

    @mock.patch('builtins.open')
    @mock.patch('sys.stdout.write')
    @mock.patch('yaml.safe_load')
    @mock.patch('os.path.isfile')
    @mock.patch('os.path.isdir')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.repository_path')
    def test_download_repository_git_directory(self, repository_path_mock, isdir_mock, isfile_mock, yaml_load_mock, sys_stdout_write, _):
        """download_repository .git is exist"""
        # mock settings
        isdir_mock.return_value = True
        isfile_mock.return_value = True
        test_repo_path = 'test_root'
        repository_path_mock.return_value = test_repo_path
        test_repo_name = 'a/test_repo'
        test_yaml = {'child_binder': [test_repo_name]}
        yaml_load_mock.side_effect = [test_yaml, None]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        test_url = 'test_url'
        arg_url = 'aaa/{}'.format(test_url)
        ret = binder_plugin.download_repository(arg_url, verbose=True)
        sys_calls = [
            call('    - Downloading repository %s\n' % arg_url),
            call('        into %s\n' % os.path.join(test_repo_path, test_url)),
            call('    - Parsing child Binder\n'),
            call('    - Downloading repository %s\n' % test_repo_name),
            call('        into %s\n' % os.path.join(
                test_repo_path, test_repo_name[2:])),
            call('    - Parsing child Binder\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        git_calls = [
            call(['pull'], verbose=True, path=os.path.join(
                test_repo_path, test_url))
        ]
        self.admin_mock.git.git_command.assert_has_calls(git_calls)

    @mock.patch('builtins.open')
    @mock.patch('sys.stdout.write')
    @mock.patch('yaml.safe_load')
    @mock.patch('os.path.isfile')
    @mock.patch('os.path.isdir')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.repository_path')
    def test_download_repository_not_git_directory(self, repository_path_mock, isdir_mock, isfile_mock, yaml_load_mock, sys_stdout_write, _):
        """download_repository .git is not exist"""
        # mock settings
        isdir_mock.side_effect = [True, False, True, False]
        isfile_mock.return_value = True
        test_repo_path = 'test_root'
        repository_path_mock.return_value = test_repo_path
        test_repo_name = 'a/test_repo'
        test_yaml = {'child_binder': [test_repo_name]}
        yaml_load_mock.side_effect = [test_yaml, None]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        test_url = 'test_url'
        arg_url = 'aaa/{}'.format(test_url)
        ret = binder_plugin.download_repository(arg_url, verbose=True)
        sys_calls = [
            call('    - Downloading repository %s\n' % arg_url),
            call('        into %s\n' % os.path.join(test_repo_path, test_url)),
            call('    - Parsing child Binder\n'),
            call('    - Downloading repository %s\n' % test_repo_name),
            call('        into %s\n' % os.path.join(
                test_repo_path, test_repo_name[2:])),
            call('    - Parsing child Binder\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        git_calls = [
            call(['clone', arg_url, os.path.join(
                test_repo_path, test_url)], verbose=True)
        ]
        self.admin_mock.git.git_command.assert_has_calls(git_calls)

    @mock.patch('builtins.open')
    @mock.patch('os.makedirs')
    @mock.patch('sys.stdout.write')
    @mock.patch('yaml.safe_load')
    @mock.patch('os.path.isfile')
    @mock.patch('os.path.isdir')
    @mock.patch('wasanbon.core.plugins.admin.binder_plugin.repository_path')
    def test_download_repository_no_directory(self, repository_path_mock, isdir_mock, isfile_mock, yaml_load_mock, sys_stdout_write, mkdirs_mock, _):
        """download_repository .git is not exist"""
        # mock settings
        isdir_mock.return_value = False
        isfile_mock.return_value = True
        test_repo_path = 'test_root'
        repository_path_mock.return_value = test_repo_path
        test_repo_name = 'a/test_repo'
        test_yaml = {'child_binder': [test_repo_name]}
        yaml_load_mock.side_effect = [test_yaml, None]
        # test
        from wasanbon.core.plugins.admin import binder_plugin
        test_url = 'test_url'
        arg_url = 'aaa/{}'.format(test_url)
        ret = binder_plugin.download_repository(arg_url, verbose=True)
        sys_calls = [
            call('    - Downloading repository %s\n' % arg_url),
            call('        into %s\n' % os.path.join(test_repo_path, test_url)),
            call('    - Parsing child Binder\n'),
            call('    - Downloading repository %s\n' % test_repo_name),
            call('        into %s\n' % os.path.join(
                test_repo_path, test_repo_name[2:])),
            call('    - Parsing child Binder\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        git_calls = [
            call(['clone', arg_url, os.path.join(
                test_repo_path, test_url)], verbose=True)
        ]
        self.admin_mock.git.git_command.assert_has_calls(git_calls)
        mkdirs_mock.assert_has_calls(
            [call(os.path.join(test_repo_path, test_url))])


if __name__ == '__main__':
    unittest.main()
