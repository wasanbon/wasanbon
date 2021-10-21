# test for wasanbon/core/plugins/admin/systemlauncher_plugin/run.py

import unittest
from unittest import mock
from unittest.mock import Mock, call
import os
# import wasanbon before sys.platform mock is applied to prevent error while importing subprocess
import wasanbon.core.plugins.admin.systemlauncher_plugin


class TestPlugin(unittest.TestCase):

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('ctypes.CDLL')
    def test_disable_sig_darwin(self, sys_cdll_mock):
        """test for disable_sig darwin"""
        import wasanbon.core.plugins.admin.systemlauncher_plugin.run as run
        run.disable_sig()
        sys_cdll_mock.assert_called_once_with('libc.dylib')

    @mock.patch('sys.platform', new='linux')
    @mock.patch('ctypes.CDLL')
    def test_disable_sig_darwin(self, sys_cdll_mock):
        """test for disable_sig darwin"""
        import wasanbon.core.plugins.admin.systemlauncher_plugin.run as run
        run.disable_sig()
        sys_cdll_mock.assert_called_once_with('libc.so.6')

    @mock.patch('sys.platform', new='linux')
    @mock.patch('ctypes.CDLL')
    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.Popen')
    def test_start_cpp_rtcd_linux_darwin(self, popen_mock, sys_stdout_write, sys_cdll_mock):
        """test for start_cpp_rtcd linux & darwin"""
        import wasanbon.core.plugins.admin.systemlauncher_plugin.run as run
        # test
        test_filepath = 'testfile'
        run.start_cpp_rtcd(test_filepath)
        sys_stdout_write.assert_has_calls([call(' - Starting C++ rtcd.\n')])
        args = {}
        args['env'] = os.environ.copy()
        args['preexec_fn'] = run.disable_sig
        args['stdout'] = None
        args['stdin'] = None
        cmd = ['rtcd', '-f', test_filepath]
        popen_calls = [call(cmd, **args)]
        popen_mock.assert_has_calls(popen_calls)

    @mock.patch('sys.platform', new='win32')
    @mock.patch('ctypes.CDLL')
    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.Popen')
    def test_start_cpp_rtcd_win(self, popen_mock, sys_stdout_write, sys_cdll_mock):
        """test for start_cpp_rtcd win32"""
        import wasanbon.core.plugins.admin.systemlauncher_plugin.run as run
        # test
        test_filepath = 'testfile'
        run.start_cpp_rtcd(test_filepath)
        sys_stdout_write.assert_has_calls([call(' - Starting C++ rtcd.\n')])
        args = {}
        args['env'] = os.environ.copy()
        args['preexec_fn'] = None
        args['stdout'] = None
        args['stdin'] = None
        args['creationflags'] = 512
        cmd = ['rtcd', '-f', test_filepath]
        popen_calls = [call(cmd, **args)]
        popen_mock.assert_has_calls(popen_calls)

    @mock.patch('sys.platform', new='linux')
    @mock.patch('ctypes.CDLL')
    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.Popen')
    def test_start_python_rtcd_linux_darwin(self, popen_mock, sys_stdout_write, sys_cdll_mock):
        """test for start_python_rtcd linux & darwin"""
        import wasanbon.core.plugins.admin.systemlauncher_plugin.run as run
        # test
        test_filepath = 'testfile'
        run.start_python_rtcd(test_filepath, verbose=True)
        sys_stdout_write.assert_has_calls([call(' - Starting Python rtcd.\n')])
        args = {}
        args['env'] = os.environ.copy()
        args['preexec_fn'] = run.disable_sig
        args['stdout'] = None
        args['stdin'] = None
        cmd = ['rtcd_python3', '-f', test_filepath]
        popen_calls = [call(cmd, **args)]
        popen_mock.assert_has_calls(popen_calls)

    @mock.patch('sys.platform', new='win32')
    @mock.patch('sys.path', new=['test1'])
    @mock.patch('ctypes.CDLL')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.Popen')
    def test_start_python_rtcd_win(self, popen_mock, sys_stdout_write, isfile_mock, sys_cdll_mock):
        """test for start_python_rtcd win32"""
        import wasanbon.core.plugins.admin.systemlauncher_plugin.run as run
        # test
        test_filepath = 'testfile'
        run.start_python_rtcd(test_filepath, verbose=True)
        sys_stdout_write.assert_has_calls([call(' - Starting Python rtcd.\n')])
        args = {}
        args['env'] = os.environ.copy()
        args['preexec_fn'] = None
        args['stdout'] = None
        args['stdin'] = None
        args['creationflags'] = 512
        cmd = [os.path.join('test1', 'python.exe'), os.path.join('test1', 'rtcd_python.py'), '-f', test_filepath]
        popen_calls = [call(cmd, **args)]
        popen_mock.assert_has_calls(popen_calls)

    @mock.patch('sys.platform', new='linux')
    @mock.patch('ctypes.CDLL')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.listdir')
    @mock.patch('os.environ.copy')
    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.Popen')
    def test_start_java_rtcd_linux_darwin(self, popen_mock, sys_stdout_write, environ_mock, listdir_mock, isdir_mock, sys_cdll_mock):
        """test for start_java_rtcd linux & darwin"""
        # mock pacth settings
        environ_mock.return_value = {'RTM_JAVA_ROOT': 'test2'}
        listdir_mock.side_effect =(['test11.jar'], ['test12.jar'], ['test13.jar'])
        import wasanbon.core.plugins.admin.systemlauncher_plugin.run as run
        # test
        rtc_mock = Mock()
        rtc_mock.path = 'test_rtc'
        test_rtcs = [rtc_mock]
        test_filepath = 'testfile'
        run.start_java_rtcd(test_rtcs, test_filepath, verbose=True)
        args = {}
        cwd = os.getcwd()
        classpath = cwd + ':' + os.path.join(cwd, 'bin')
        classpath += ':' +  os.path.join('test2', 'jar', 'test11.jar')
        classpath += ':' +  os.path.join('test_rtc', 'jar', 'test13.jar')
        args['env'] = {'CLASSPATH': classpath, 'RTM_JAVA_ROOT': 'test2'}
        args['preexec_fn'] = run.disable_sig
        args['stdout'] = None
        args['stdin'] = None
        cmd = ['java', 'rtcd.rtcd', '-f', test_filepath]
        popen_calls = [call(cmd, **args)]
        popen_mock.assert_has_calls(popen_calls)
        sys_stdout_write.assert_has_calls([call(' - Starting Java rtcd.\n'), call('java_rtcd : cmd = %s\n' % cmd)])

    @mock.patch('sys.platform', new='win32')
    @mock.patch('ctypes.CDLL')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.listdir')
    @mock.patch('os.environ.copy')
    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.Popen')
    def test_start_java_rtcd_win(self, popen_mock, sys_stdout_write, environ_mock, listdir_mock, isdir_mock, sys_cdll_mock):
        """test for start_java_rtcd win32"""
        # mock pacth settings
        environ_mock.return_value = {'RTM_JAVA_ROOT': 'test2'}
        listdir_mock.side_effect =(['test11.jar'], ['test12.jar'], ['test13.jar'])
        import wasanbon.core.plugins.admin.systemlauncher_plugin.run as run
        # test
        rtc_mock = Mock()
        rtc_mock.path = 'test_rtc'
        test_rtcs = [rtc_mock]
        test_filepath = 'testfile'
        run.start_java_rtcd(test_rtcs, test_filepath, verbose=True)
        args = {}
        cwd = os.getcwd()
        classpath = cwd + ';' + os.path.join(cwd, 'bin')
        classpath += ';' +  os.path.join('test2', 'jar', 'test11.jar')
        classpath += ';' +  os.path.join('test_rtc', 'jar', 'test13.jar')
        args['env'] = {'CLASSPATH': classpath, 'RTM_JAVA_ROOT': 'test2'}
        args['preexec_fn'] = None
        args['stdout'] = None
        args['stdin'] = None
        args['creationflags'] = 512
        cmd = ['java', 'rtcd.rtcd', '-f', test_filepath]
        popen_calls = [call(cmd, **args)]
        popen_mock.assert_has_calls(popen_calls)
        sys_stdout_write.assert_has_calls([call(' - Starting Java rtcd.\n'), call('java_rtcd : cmd = %s\n' % cmd)])



if __name__ == '__main__':
    unittest.main()
