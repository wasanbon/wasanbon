# test for wasanbon/core/plugins/admin/editor_plugin/__init__.py Plugin class

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')


class TestPlugin(unittest.TestCase):

    class FunctionList():
        pass

    def setUp(self):
        import wasanbon.core.plugins.admin.editor_plugin as m
        self.admin_mock = MagicMock(sepc=['environment'])
        type(self.admin_mock.environment).path = {'emacs': 'emacs_path'}
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        ### set mock ###
        from wasanbon.core.plugins.admin.editor_plugin import Plugin
        mock_init.return_value = None
        ### test ###
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        ### test ###
        self.assertEqual(['admin.environment'], self.plugin.depends())

    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.Plugin.path', new={'emacs': 'test'})
    def test_get_editor_path(self):
        """get_editor_path normal case"""
        ### test ###
        self.assertEqual('emacs_path', self.plugin.get_editor_path())

    @mock.patch('subprocess.call')
    @mock.patch('signal.signal')
    @mock.patch('wasanbon.core.plugins.admin.editor_plugin.find_rtc_srcs')
    @mock.patch('wasanbon.core.plugins.admin.editor_plugin.Plugin.get_editor_path')
    @mock.patch('wasanbon.get_home_path')
    @mock.patch('os.environ.copy')
    def test_edit_rtc(self, mock_environ_copy, mock_get_home_path, mock_get_editor_path, mock_find_rtc_srcs, mock_signal, mock_subprocess_call):
        """edit_rtc normal case"""
        ### set mock ###
        mock_environ_copy.return_value = {'HOME': 'home_path'}
        mock_get_editor_path.return_value = 'emacs_path'
        rtc = MagicMock()
        type(rtc).rtcprofile = 'rtcprofile'
        mock_find_rtc_srcs.return_value = ['rtc_path']
        mock_find_rtc_srcs.return_value = ['rtc_path']
        ### test ###
        self.plugin.edit_rtc(rtc)
        des_val = ['emacs_path']
        des_val = des_val + ['-nw']
        des_val = des_val + ['rtc_path']
        mock_signal.assert_called_once()
        mock_subprocess_call.assert_any_call(des_val, env={'HOME': 'home_path'})

    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.call')
    @mock.patch('signal.signal')
    @mock.patch('wasanbon.core.plugins.admin.editor_plugin.find_rtc_srcs')
    @mock.patch('wasanbon.core.plugins.admin.editor_plugin.Plugin.get_editor_path')
    @mock.patch('wasanbon.get_home_path')
    @mock.patch('os.environ.copy')
    # , mock_stdout_write):
    def test_edit_rtc_v(self, mock_environ_copy, mock_get_home_path, mock_get_editor_path, mock_find_rtc_srcs, mock_signal, mock_subprocess_call, mock_write):
        """edit_rtc normal case with -v option"""
        ### set mock ###
        mock_environ_copy.return_value = {'HOME': 'home_path'}
        mock_get_editor_path.return_value = 'emacs_path'
        rtc = MagicMock()
        type(rtc).rtcprofile = 'rtcprofile'
        mock_find_rtc_srcs.return_value = ['rtc_path']
        ### test ###
        self.plugin.edit_rtc(rtc, verbose=True)
        des_val = ['emacs_path']
        des_val = des_val + ['-nw']
        des_val = des_val + ['rtc_path']
        mock_signal.assert_called_once()
        mock_subprocess_call.assert_any_call(des_val, env={'HOME': 'home_path'})
        mock_write.assert_called_once()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.editor_plugin.Plugin.get_editor_path')
    @mock.patch('wasanbon.get_home_path')
    @mock.patch('os.environ.copy')
    def test_edit_rtc_err(self, mock_environ_copy, mock_get_home_path, mock_get_editor_path, mock_stdout_write):
        """edit_rtc err case"""
        ### set mock ###
        mock_environ_copy.return_value = {'HOME': 'home_path'}
        mock_get_editor_path.return_value = ''
        rtc = MagicMock()
        type(rtc).rtcprofile = 'rtcprofile'
        ### test ###
        self.assertEqual(-1, self.plugin.edit_rtc(rtc))
        mock_stdout_write.assert_called_once()

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    def test_find_rtc_srcs_python(self, mock_split, mock_search_file):
        """find_rtc_srcs normal case
        rtcp language.kind = 'Python'
        """
        ### set mock ###
        mock_split.return_value = 'path', None
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'Python'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_search_file.side_effect = ['python_file']
        ### test ###
        from wasanbon.core.plugins.admin.editor_plugin import find_rtc_srcs
        self.assertEqual('python_file', find_rtc_srcs(rtcp))
        mock_search_file.assert_called_once_with('path', 'rtcp_name' + '.py')

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    def test_find_rtc_srcs_java(self, mock_split, mock_search_file):
        """find_rtc_srcs normal case
        rtcp language.kind = 'Java'
        """
        ### set mock ###
        mock_split.return_value = 'path', None
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'Java'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_search_file.side_effect = ['java_file']
        ### test ###
        from wasanbon.core.plugins.admin.editor_plugin import find_rtc_srcs
        self.assertEqual('java_file', find_rtc_srcs(rtcp))
        mock_search_file.assert_called_once_with('path', 'rtcp_name' + 'Impl.java')

    @mock.patch('wasanbon.util.search_file')
    @mock.patch('os.path.split')
    def test_find_rtc_srcs_cpp(self, mock_split, mock_search_file):
        """find_rtc_srcs normal case
        rtcp language.kind = 'C++'
        """
        ### set mock ###
        mock_split.return_value = 'path', None
        rtcp = MagicMock(spec=['language', 'basicInfo'])
        type(rtcp).filename = 'filename'
        type(rtcp.language).kind = 'C++'
        type(rtcp.basicInfo).name = 'rtcp_name'
        mock_search_file.side_effect = ['hdrs', 'srcs']
        ### test ###
        from wasanbon.core.plugins.admin.editor_plugin import find_rtc_srcs
        self.assertEqual('hdrs' + 'srcs', find_rtc_srcs(rtcp))
        mock_search_file.assert_has_calls([call('path', 'rtcp_name' + '.h'), call('path', 'rtcp_name' + '.cpp')])


if __name__ == '__main__':
    unittest.main()
