# test for wasanbon/core/plugins/admin/eclipse_plugin/__init__.py Plugin class

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
        ### setting admin mock ###
        import wasanbon.core.plugins.admin.eclipse_plugin as m
        self.admin_mock = MagicMock(spec=['environment'])
        type(self.admin_mock.environment).path = {'eclipse': 'eclipse_cmd'}
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()

        ### setting parse_args return option ###
        self.options = self.FunctionList()
        flags = ['verbose_flag', 'directory']
        for flag in flags:
            ## default: False ##
            setattr(self.options, flag, False)

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.eclipse_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment'], self.plugin.depends())

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value=-1))
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH':'path', 'RTM_ROOT': None}))
    @mock.patch('subprocess.Popen')
    @mock.patch('wasanbon.get_rtm_root')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_eclipse_1(self, mock_join, mock_isdir, mock_rtm_root, mock_Popen, mock_environ, mock_PIPE, mock_platform):
        """launch_eclipse normal case 
        sys.platform == win32
        """
        ### set mock ###
        if sys.platform == 'darwin':
            mock_join.side_effect = ['eclipse_dir', 'eclipse_dir_mac']
        else:
            mock_join.side_effect = ['eclipse_dir']
        mock_isdir.return_value = True

        self.admin_mock.environment.path = {'eclipse': 'eclipse_cmd'}
        mock_rtm_root.return_value = 'rtm_root'
        p = MagicMock(spec=['wait'])
        mock_Popen.return_value = p
        ### test ###
        self.assertEqual(0, self.plugin.launch_eclipse())
        if sys.platform == 'win32':
            mock_Popen.assert_called_once_with(['eclipse_cmd'], creationflags=512, env={'PATH': 'rtm_rootjre\\bin;path', 'RTM_ROOT': 'rtm_root'}, stdout=None, stderr=None)
        elif sys.platform == 'darwin':
            mock_Popen.assert_called_once_with(['eclipse_cmd'], env={'RTM_ROOT': 'rtm_root'}, stdout=-1, stderr=-1)
        else:
            mock_Popen.assert_called_once_with(['eclipse_cmd'], env={'RTM_ROOT': 'rtm_root'}, stdout=-1, stderr=-1)
        p.wait.assert_not_called()
        
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value=-1))
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'RTM_ROOT': None}))
    @mock.patch('subprocess.Popen')
    @mock.patch('wasanbon.get_rtm_root')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_eclipse_2(self, mock_join, mock_isdir, mock_rtm_root, mock_Popen, mock_environ, mock_PIPE, mock_platform):
        """launch_eclipse normal case 
        sys.platform == darwin
        """
        ### set mock ###
        if sys.platform == 'darwin':
            #mock_join.side_effect = ['eclipse_dir', 'eclipse_dir_mac']
            mock_join.side_effect = ['eclipse_dir_mac']
        else:
            mock_join.side_effect = ['eclipse_dir']
        mock_isdir.return_value = True

        self.admin_mock.environment.path = {'eclipse': 'eclipse_cmd'}
        mock_rtm_root.return_value = 'rtm_root'
        p = MagicMock(spec=['wait'])
        mock_Popen.return_value = p
        ### test ###
        self.assertEqual(0, self.plugin.launch_eclipse())
        if sys.platform == 'win32':
            mock_Popen.assert_called_once_with(['eclipse_cmd'], creationflags=512, env={'PATH': 'rtm_rootjre\\bin;path', 'RTM_ROOT': 'rtm_root'}, stdout=None, stderr=None)
        elif sys.platform == 'darwin':
            mock_Popen.assert_called_once_with(['eclipse_cmd'], env={'RTM_ROOT': 'rtm_root'}, stdout=None, stderr=None)
        else:
            mock_Popen.assert_called_once_with(['eclipse_cmd'], env={'RTM_ROOT': 'rtm_root'}, stdout=-1, stderr=-1)
        p.wait.assert_not_called()
        
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value=-1))
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'RTM_ROOT': None}))
    @mock.patch('subprocess.Popen')
    @mock.patch('wasanbon.get_rtm_root')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_eclipse_3(self, mock_join, mock_isdir, mock_rtm_root, mock_Popen, mock_environ, mock_PIPE, mock_platform):
        """launch_eclipse normal case 
        sys.platform == linux
        """
        ### set mock ###
        if sys.platform == 'darwin':
            mock_join.side_effect = ['eclipse_dir', 'eclipse_dir_mac']
        else:
            mock_join.side_effect = ['eclipse_dir']
        mock_isdir.return_value = True

        self.admin_mock.environment.path = {'eclipse': 'eclipse_cmd'}
        mock_rtm_root.return_value = 'rtm_root'
        p = MagicMock(spec=['wait'])
        mock_Popen.return_value = p
        ### test ###
        self.assertEqual(0, self.plugin.launch_eclipse())
        if sys.platform == 'win32':
            mock_Popen.assert_called_once_with(['eclipse_cmd'], creationflags=512, env={'PATH': 'rtm_rootjre\\bin;path', 'RTM_ROOT': 'rtm_root'}, stdout=None, stderr=None)
        elif sys.platform == 'darwin':
            mock_Popen.assert_called_once_with(['eclipse_cmd'], env={'RTM_ROOT': 'rtm_root'}, stdout=-1, stderr=-1)
        else:
            mock_Popen.assert_called_once_with(['eclipse_cmd'], env={'RTM_ROOT': 'rtm_root'}, stdout=-1, stderr=-1)
        p.wait.assert_not_called()

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_eclipse_err_1(self, mock_join, mock_isdir, mock_write, mock_platform):
        """launch_eclipse error case
        eclipse dir is not found
        """
        ### set mock ###
        if sys.platform == 'darwin':
            mock_join.side_effect = ['eclipse_dir', 'eclipse_dir_mac']
        else:
            mock_join.side_effect = ['eclipse_dir']
        mock_isdir.return_value = False
        ### test ###
        self.assertEqual(-1, self.plugin.launch_eclipse())
        mock_write.assert_called_once()
        
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_eclipse_err_2(self, mock_join, mock_isdir, mock_write, mock_platform):
        """launch_eclipse error case
        eclipse dir is not found
        """
        ### set mock ###
        if sys.platform == 'darwin':
            mock_join.side_effect = ['eclipse_dir', 'eclipse_dir_mac']
        else:
            mock_join.side_effect = ['eclipse_dir']
        mock_isdir.return_value = False
        ### test ###
        self.assertEqual(-1, self.plugin.launch_eclipse())
        mock_write.assert_called_once()

    @mock.patch('wasanbon.core.plugins.admin.eclipse_plugin.Plugin.launch_eclipse')
    def test_launch_1(self, mock_launch_eclipse):
        """launch normal case (argv>3)"""
        test_workbench = 'test_path'
        test_argv = ['admin', 'launch', 'eclipse', '-d', test_workbench, '-v', 'a']
        self.assertEqual(0, self.plugin.launch(test_argv))
        eclipse_call = [call(workbench=test_workbench, argv=['a'], verbose=True)]
        mock_launch_eclipse.assert_has_calls(eclipse_call)

    @mock.patch('wasanbon.core.plugins.admin.eclipse_plugin.Plugin.launch_eclipse')
    def test_launch_2(self, mock_launch_eclipse):
        """launch normal case (argv<=3)"""
        test_argv = ['admin', 'launch', 'eclipse', 'a']
        self.assertEqual(0, self.plugin.launch(test_argv))
        eclipse_call = [call(workbench='.', argv=['a'], verbose=False)]
        mock_launch_eclipse.assert_has_calls(eclipse_call)


if __name__ == '__main__':
    unittest.main()
