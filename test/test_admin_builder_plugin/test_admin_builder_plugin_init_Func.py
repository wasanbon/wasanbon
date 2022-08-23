# test for wasanbon/core/plugins/admin/builder_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')


class Test(unittest.TestCase):

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.admin.builder_plugin as m
        self.admin_mock = MagicMock(spec=['environment'])
        self.admin_mock.environment(sepc=['getIDE'])
        type(self.admin_mock.environment).path = PropertyMock()
        setattr(m, 'admin', self.admin_mock)
        self.test = m

    def test_getIDE(self):
        """getIDE normal case"""
        self.admin_mock.environment.getIDE.return_value = 'hoge'
        ### test ###
        self.assertEqual(self.test.getIDE(), 'hoge')

    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH': 'path'}))
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.getIDE', return_value='IDE')
    @mock.patch('os.path.dirname')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.split')
    @mock.patch('sys.stdout.write')
    def test_build_rtc_cpp_1(self, mock_write, mock_split, mock_join, mock_platform, mock_dirname, mock_getIDE, mock_getcwd, mock_chdir, mock_isdir, mock_makedirs, mock_PIPE, mock_Popen, mock_environ):
        """build_rtc_cpp normal case
        verbose = False
        sys.platform = win32
        os.path.isdir(build_dir) = True
        ret != 0: return
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', 'rtc_xml'
        type(self.admin_mock.environment).path = PropertyMock(return_value={'cmake': 'cmake_path',
                                                                            'msbuild': 'msbuild_path'})
        mock_dirname.return_value = 'msbuild_dir'
        mock_isdir.return_value = True
        p = MagicMock(spec=['communicate'])
        p.communicate.side_effect = [['std_out'], ]
        type(p).returncode = PropertyMock(side_effect=[-1])
        mock_Popen.return_value = p
        ### test ###
        self.assertEqual((False, 'std_out'), self.test.build_rtc_cpp(rtcp))
        self.assertEqual(1, mock_write.call_count)
        mock_dirname.assert_called_once_with('msbuild_path')
        mock_getIDE.assert_called_once()  # win32
        mock_makedirs.assert_not_called()
        mock_Popen.assert_called_once_with(['cmake_path', '..', '-G', 'IDE'], env={'PATH': 'path;msbuild_dir'}, stdout='PIPE', stderr='PIPE')

    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH': 'path'}))
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.getIDE', return_value='IDE')
    @mock.patch('os.path.dirname')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.split')
    @mock.patch('sys.stdout.write')
    def test_build_rtc_cpp_2(self, mock_write, mock_split, mock_join, mock_platform, mock_dirname, mock_getIDE, mock_getcwd, mock_chdir, mock_isdir, mock_makedirs, mock_PIPE, mock_Popen, mock_environ):
        """build_rtc_cpp normal case
        verbose = True
        sys.platform = win32
        os.path.isdir(build_dir) = True
        ret != 0
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', 'rtc_xml'
        type(self.admin_mock.environment).path = PropertyMock(return_value={'cmake': 'cmake_path',
                                                                            'msbuild': 'msbuild_path'})
        mock_dirname.return_value = 'msbuild_dir'
        mock_isdir.return_value = True
        p = MagicMock(spec=['communicate'])
        p.communicate.side_effect = [['std_out'], ]
        type(p).returncode = PropertyMock(side_effect=[-1])
        mock_Popen.return_value = p
        ### test ###
        self.assertEqual((False, None), self.test.build_rtc_cpp(rtcp, verbose=True))
        self.assertEqual(3, mock_write.call_count)
        mock_dirname.assert_called_once_with('msbuild_path')
        mock_getIDE.assert_called_once()  # win32
        mock_makedirs.assert_not_called()
        mock_Popen.assert_called_once_with(['cmake_path', '..', '-G', 'IDE'], env={'PATH': 'path;msbuild_dir'}, stdout=None, stderr=None)

    @mock.patch('os.listdir')
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH': 'path'}))
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.getIDE', return_value='IDE')
    @mock.patch('os.path.dirname')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.split')
    @mock.patch('sys.stdout.write')
    def test_build_rtc_cpp_3(self, mock_write, mock_split, mock_join, mock_platform, mock_dirname, mock_getIDE, mock_getcwd, mock_chdir, mock_isdir, mock_makedirs, mock_PIPE, mock_Popen, mock_environ, mock_listdir):
        """build_rtc_cpp normal case
        verbose = False
        sys.platform = win32
        os.path.isdir(build_dir) = True
        ret = 0
        if sln in os.listdir(os.getcwd()): False
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', 'rtc_xml'
        type(self.admin_mock.environment).path = PropertyMock(return_value={'cmake': 'cmake_path',
                                                                            'msbuild': 'msbuild_path'})
        mock_dirname.return_value = 'msbuild_dir'
        mock_isdir.return_value = True
        p = MagicMock(spec=['communicate'])
        p.communicate.side_effect = [['std_out'], ]
        type(p).returncode = PropertyMock(side_effect=[0])
        mock_Popen.return_value = p
        mock_listdir.return_value = ['hoge.sln']
        ### test ###
        self.assertEqual(None, self.test.build_rtc_cpp(rtcp, verbose=False))
        self.assertEqual(2, mock_write.call_count)
        mock_dirname.assert_called_once_with('msbuild_path')
        mock_getIDE.assert_called_once()  # win32
        mock_makedirs.assert_not_called()
        mock_Popen.assert_called_once_with(['cmake_path', '..', '-G', 'IDE'], env={'PATH': 'path;msbuild_dir'}, stdout='PIPE', stderr='PIPE')

    @mock.patch('os.path.basename', return_value='basename')
    @mock.patch('os.listdir')
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH': 'path', 'OMNI_ROOT': 'omni_root'}))
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.getIDE', return_value='IDE')
    @mock.patch('os.path.dirname')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.split')
    @mock.patch('sys.stdout.write')
    def test_build_rtc_cpp_4(self, mock_write, mock_split, mock_join, mock_platform, mock_dirname, mock_getIDE, mock_getcwd, mock_chdir, mock_isdir, mock_makedirs, mock_PIPE, mock_Popen, mock_environ, mock_listdir, mock_basename):
        """build_rtc_cpp normal case
        verbose = False
        sys.platform = win32
        os.path.isdir(build_dir) = True
        ret = 0
        if sln in os.listdir(os.getcwd()): True
        std_out = None
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', 'rtc_xml'
        type(self.admin_mock.environment).path = PropertyMock(return_value={'cmake': 'cmake_path',
                                                                            'msbuild': 'msbuild_path'})
        mock_dirname.return_value = 'msbuild_dir'
        mock_isdir.return_value = True
        p = MagicMock(spec=['communicate'])
        p.communicate.side_effect = [['std_out'], (None, None)]
        type(p).returncode = PropertyMock(side_effect=[0, 0])
        mock_Popen.return_value = p
        mock_listdir.return_value = ['rtcp_name.sln']
        mock_join.side_effect = ['build_dir', 'omni_root']
        ### test ###
        self.assertEqual((True, ''), self.test.build_rtc_cpp(rtcp, verbose=False))
        self.assertEqual(4, mock_write.call_count)
        mock_dirname.assert_called_once_with('msbuild_path')
        mock_getIDE.assert_called_once()  # win32
        mock_makedirs.assert_not_called()
        mock_Popen.assert_any_call(['msbuild_path', 'rtcp_name.sln', '/p:Configuration=Release', '/clp:ErrorsOnly'], stdout=None,
                                   stderr=None, env={'PATH': 'path;msbuild_dir;omni_root', 'OMNI_ROOT': 'omni_root'})
        mock_basename.assert_called_once()

    @mock.patch('os.path.basename', return_value='basename')
    @mock.patch('os.listdir')
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH': 'path', 'OMNI_ROOT': 'omni_root'}))
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.getIDE', return_value='IDE')
    @mock.patch('os.path.dirname')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.split')
    @mock.patch('sys.stdout.write')
    def test_build_rtc_cpp_5(self, mock_write, mock_split, mock_join, mock_platform, mock_dirname, mock_getIDE, mock_getcwd, mock_chdir, mock_isdir, mock_makedirs, mock_PIPE, mock_Popen, mock_environ, mock_listdir, mock_basename):
        """build_rtc_cpp normal case
        verbose = False
        sys.platform = win32
        os.path.isdir(build_dir) = True
        ret = 0
        if sln in os.listdir(os.getcwd()): True
        std_out = error
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', 'rtc_xml'
        type(self.admin_mock.environment).path = PropertyMock(return_value={'cmake': 'cmake_path',
                                                                            'msbuild': 'msbuild_path'})
        mock_dirname.return_value = 'msbuild_dir'
        mock_isdir.return_value = True
        p = MagicMock(spec=['communicate'])
        p.communicate.side_effect = [['std_out'], ('error', None)]
        type(p).returncode = PropertyMock(side_effect=[0, 0])
        mock_Popen.return_value = p
        mock_listdir.return_value = ['rtcp_name.sln']
        mock_join.side_effect = ['build_dir', 'omni_root']
        ### test ###
        self.assertEqual((False, 'error'), self.test.build_rtc_cpp(rtcp, verbose=False))
        self.assertEqual(4, mock_write.call_count)
        mock_dirname.assert_called_once_with('msbuild_path')
        mock_getIDE.assert_called_once()  # win32
        mock_makedirs.assert_not_called()
        mock_Popen.assert_any_call(['msbuild_path', 'rtcp_name.sln', '/p:Configuration=Release', '/clp:ErrorsOnly'], stdout=None,
                                   stderr=None, env={'PATH': 'path;msbuild_dir;omni_root', 'OMNI_ROOT': 'omni_root'})
        mock_basename.assert_called_once()

    @mock.patch('os.path.basename', return_value='basename')
    @mock.patch('os.listdir')
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH': 'path', 'OMNI_ROOT': 'omni_root'}))
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.getIDE', return_value='IDE')
    @mock.patch('os.path.dirname')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.split')
    @mock.patch('sys.stdout.write')
    def test_build_rtc_cpp_6(self, mock_write, mock_split, mock_join, mock_platform, mock_dirname, mock_getIDE, mock_getcwd, mock_chdir, mock_isdir, mock_makedirs, mock_PIPE, mock_Popen, mock_environ, mock_listdir, mock_basename):
        """build_rtc_cpp normal case
        verbose = True
        sys.platform = win32
        os.path.isdir(build_dir) = True
        ret = 0
        if sln in os.listdir(os.getcwd()): True
        std_out = error
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', 'rtc_xml'
        type(self.admin_mock.environment).path = PropertyMock(return_value={'cmake': 'cmake_path',
                                                                            'msbuild': 'msbuild_path'})
        mock_dirname.return_value = 'msbuild_dir'
        mock_isdir.return_value = True
        p = MagicMock(spec=['communicate'])
        p.communicate.side_effect = [['std_out'], ('error', None)]
        type(p).returncode = PropertyMock(side_effect=[0, 0])
        mock_Popen.return_value = p
        mock_listdir.return_value = ['rtcp_name.sln']
        mock_join.side_effect = ['build_dir', 'omni_root']
        ### test ###
        self.assertEqual((True, ''), self.test.build_rtc_cpp(rtcp, verbose=True))
        self.assertEqual(7, mock_write.call_count)
        mock_dirname.assert_called_once_with('msbuild_path')
        mock_getIDE.assert_called_once()  # win32
        mock_makedirs.assert_not_called()
        mock_Popen.assert_any_call(['msbuild_path', 'rtcp_name.sln', '/p:Configuration=Release', '/clp:ErrorsOnly'], stdout=None,
                                   stderr=None, env={'PATH': 'path;msbuild_dir;omni_root', 'OMNI_ROOT': 'omni_root'})
        mock_basename.assert_called_once()

    @mock.patch('os.path.basename', return_value='basename')
    @mock.patch('os.listdir')
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH': 'path', 'OMNI_ROOT': 'omni_root'}))
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.getIDE', return_value='IDE')
    @mock.patch('os.path.dirname')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.split')
    @mock.patch('sys.stdout.write')
    def test_build_rtc_cpp_7(self, mock_write, mock_split, mock_join, mock_platform, mock_dirname, mock_getIDE, mock_getcwd, mock_chdir, mock_isdir, mock_makedirs, mock_PIPE, mock_Popen, mock_environ, mock_listdir, mock_basename):
        """build_rtc_cpp normal case
        verbose = False
        sys.platform = linux
        os.path.isdir(build_dir) = False
        ret = 0
        if 'Makefile' in os.listdir(os.getcwd()): False
        std_out = error
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', 'rtc_xml'
        type(self.admin_mock.environment).path = PropertyMock(return_value={'cmake': 'cmake_path'})
        mock_dirname.return_value = None
        mock_isdir.return_value = False
        p = MagicMock(spec=['communicate'])
        p.communicate.side_effect = [['std_out'], ('error', None)]
        type(p).returncode = PropertyMock(side_effect=[0, 0])
        mock_Popen.return_value = p
        mock_listdir.return_value = ['hoge']
        mock_join.side_effect = ['build_dir', 'omni_root']
        ### test ###
        self.assertEqual(None, self.test.build_rtc_cpp(rtcp, verbose=False))
        self.assertEqual(1, mock_write.call_count)
        mock_dirname.assert_not_called()
        mock_getIDE.assert_not_called()  # win32
        mock_makedirs.assert_called_once()
        mock_Popen.assert_any_call(['cmake_path', '..'], env={'PATH': 'path', 'OMNI_ROOT': 'omni_root',
                                   'PKG_CONFIG_PATH': '/usr/lib/pkgconfig/:/usr/local/lib/pkgconfig/'}, stdout='PIPE', stderr='PIPE')
        mock_basename.assert_not_called()

    @mock.patch('os.path.basename', return_value='basename')
    @mock.patch('os.listdir')
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH': 'path', 'OMNI_ROOT': 'omni_root'}))
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.getIDE', return_value='IDE')
    @mock.patch('os.path.dirname')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.split')
    @mock.patch('sys.stdout.write')
    def test_build_rtc_cpp_8(self, mock_write, mock_split, mock_join, mock_platform, mock_dirname, mock_getIDE, mock_getcwd, mock_chdir, mock_isdir, mock_makedirs, mock_PIPE, mock_Popen, mock_environ, mock_listdir, mock_basename):
        """build_rtc_cpp normal case
        verbose = False
        sys.platform = linux
        os.path.isdir(build_dir) = False
        ret = 0
        if 'Makefile' in os.listdir(os.getcwd()): True
        std_out = error
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', 'rtc_xml'
        type(self.admin_mock.environment).path = PropertyMock(return_value={'cmake': 'cmake_path'})
        mock_dirname.return_value = None
        mock_isdir.return_value = False
        p = MagicMock(spec=['communicate'])
        p.communicate.side_effect = [['std_out'], ('error', None)]
        type(p).returncode = PropertyMock(side_effect=[0, 0])
        mock_Popen.return_value = p
        mock_listdir.return_value = ['Makefile']
        mock_join.side_effect = ['build_dir', 'omni_root']
        ### test ###
        self.assertEqual((True, 'error'), self.test.build_rtc_cpp(rtcp, verbose=False))
        self.assertEqual(1, mock_write.call_count)
        mock_dirname.assert_not_called()
        mock_getIDE.assert_not_called()  # win32
        mock_makedirs.assert_called_once()
        mock_Popen.assert_any_call(['cmake_path', '..'], env={'PATH': 'path', 'OMNI_ROOT': 'omni_root',
                                   'PKG_CONFIG_PATH': '/usr/lib/pkgconfig/:/usr/local/lib/pkgconfig/'}, stdout='PIPE', stderr='PIPE')
        mock_basename.assert_not_called()

    @mock.patch('os.path.basename', return_value='basename')
    @mock.patch('os.listdir')
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH': 'path', 'OMNI_ROOT': 'omni_root'}))
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.getIDE', return_value='IDE')
    @mock.patch('os.path.dirname')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.split')
    @mock.patch('sys.stdout.write')
    def test_build_rtc_cpp_9(self, mock_write, mock_split, mock_join, mock_platform, mock_dirname, mock_getIDE, mock_getcwd, mock_chdir, mock_isdir, mock_makedirs, mock_PIPE, mock_Popen, mock_environ, mock_listdir, mock_basename):
        """build_rtc_cpp normal case
        verbose = True
        sys.platform = linux
        os.path.isdir(build_dir) = False
        ret != 0
        if 'Makefile' in os.listdir(os.getcwd()): True
        std_out = error
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', 'rtc_xml'
        type(self.admin_mock.environment).path = PropertyMock(return_value={'cmake': 'cmake_path'})
        mock_dirname.return_value = None
        mock_isdir.return_value = False
        p = MagicMock(spec=['communicate'])
        p.communicate.side_effect = [['std_out'], ('error', None)]
        type(p).returncode = PropertyMock(side_effect=[0, -1])
        mock_Popen.return_value = p
        mock_listdir.return_value = ['Makefile']
        mock_join.side_effect = ['build_dir', 'omni_root']
        ### test ###
        self.assertEqual((False, 'error'), self.test.build_rtc_cpp(rtcp, verbose=True))
        self.assertEqual(10, mock_write.call_count)
        mock_dirname.assert_not_called()
        mock_getIDE.assert_not_called()  # win32
        mock_makedirs.assert_called_once()
        mock_Popen.assert_any_call(['cmake_path', '..'], env={'PATH': 'path', 'OMNI_ROOT': 'omni_root',
                                   'PKG_CONFIG_PATH': '/usr/lib/pkgconfig/:/usr/local/lib/pkgconfig/'}, stdout=None, stderr=None)
        mock_basename.assert_not_called()

    @mock.patch('os.path.basename', return_value='basename')
    @mock.patch('os.listdir')
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH': 'path', 'OMNI_ROOT': 'omni_root'}))
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.getIDE', return_value='IDE')
    @mock.patch('os.path.dirname')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.split')
    @mock.patch('sys.stdout.write')
    def test_build_rtc_cpp_10(self, mock_write, mock_split, mock_join, mock_platform, mock_dirname, mock_getIDE, mock_getcwd, mock_chdir, mock_isdir, mock_makedirs, mock_PIPE, mock_Popen, mock_environ, mock_listdir, mock_basename):
        """build_rtc_cpp normal case
        verbose = True
        sys.platform = darwin
        os.path.isdir(build_dir) = False
        ret != 0
        if 'Makefile' in os.listdir(os.getcwd()): True
        std_out = error
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', 'rtc_xml'
        type(self.admin_mock.environment).path = PropertyMock(return_value={'cmake': 'cmake_path'})
        mock_dirname.return_value = None
        mock_isdir.return_value = False
        p = MagicMock(spec=['communicate'])
        p.communicate.side_effect = [['std_out'], ('error', None)]
        type(p).returncode = PropertyMock(side_effect=[0, -1])
        mock_Popen.return_value = p
        mock_listdir.return_value = ['Makefile']
        mock_join.side_effect = ['build_dir', 'omni_root']
        ### test ###
        self.assertEqual((False, 'error'), self.test.build_rtc_cpp(rtcp, verbose=True))
        self.assertEqual(11, mock_write.call_count)
        mock_dirname.assert_not_called()
        mock_getIDE.assert_not_called()  # win32
        mock_makedirs.assert_called_once()
        mock_Popen.assert_any_call(['cmake_path', '..'], env={'PATH': 'path', 'OMNI_ROOT': 'omni_root',
                                   'PKG_CONFIG_PATH': '/usr/lib/pkgconfig/:/usr/local/lib/pkgconfig/'}, stdout=None, stderr=None)
        mock_basename.assert_not_called()

    @mock.patch('os.path.basename', return_value='basename')
    @mock.patch('os.listdir')
    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'PATH': 'path', 'OMNI_ROOT': 'omni_root'}))
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.getIDE', return_value='IDE')
    @mock.patch('os.path.dirname')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='hoge'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.split')
    @mock.patch('sys.stdout.write')
    def test_build_rtc_cpp_11(self, mock_write, mock_split, mock_join, mock_platform, mock_dirname, mock_getIDE, mock_getcwd, mock_chdir, mock_isdir, mock_makedirs, mock_PIPE, mock_Popen, mock_environ, mock_listdir, mock_basename):
        """build_rtc_cpp normal case
        verbose = True
        sys.platform = hoge
        os.path.isdir(build_dir) = False
        ret != 0
        if 'Makefile' in os.listdir(os.getcwd()): True
        std_out = error
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', 'rtc_xml'
        type(self.admin_mock.environment).path = PropertyMock(return_value={'cmake': 'cmake_path'})
        mock_dirname.return_value = None
        mock_isdir.return_value = False
        p = MagicMock(spec=['communicate'])
        p.communicate.side_effect = [['std_out'], ('error', None)]
        type(p).returncode = PropertyMock(side_effect=[0, -1])
        mock_Popen.return_value = p
        mock_listdir.return_value = ['Makefile']
        mock_join.side_effect = ['build_dir', 'omni_root']
        ### test ###
        self.assertEqual((-1, 'Unknown Platform (hoge)'), self.test.build_rtc_cpp(rtcp, verbose=True))
        self.assertEqual(6, mock_write.call_count)
        mock_dirname.assert_not_called()
        mock_getIDE.assert_not_called()  # win32
        mock_makedirs.assert_called_once()
        mock_Popen.assert_called_once_with(['cmake_path', '..'], env={'PATH': 'path', 'OMNI_ROOT': 'omni_root'}, stdout=None, stderr=None)

    @mock.patch('subprocess.call')
    @mock.patch('os.listdir')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    @mock.patch('sys.stdout.write')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('os.path.split')
    def test_build_rtc_python_1(self, mock_split, mock_getcwd, mock_chdir, mock_write, mock_platform, mock_listdir, mock_subprocess_call):
        """build_rtc_python normal case
        sys.platform = 'darwin'
        if 'idlcompile.sh' in os.listdir(os.getcwd()): False
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        mock_listdir.return_value = ['hoge']
        ### test ###
        self.assertEqual((True, ""), self.test.build_rtc_python(rtcp))
        self.assertEqual(1, mock_write.call_count)
        mock_subprocess_call.assert_not_called()

    @mock.patch('subprocess.call')
    @mock.patch('os.listdir')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    @mock.patch('sys.stdout.write')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('os.path.split')
    def test_build_rtc_python_2(self, mock_split, mock_getcwd, mock_chdir, mock_write, mock_platform, mock_listdir, mock_subprocess_call):
        """build_rtc_python normal case
        sys.platform = 'darwin'
        if 'idlcompile.sh' in os.listdir(os.getcwd()): True
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        mock_listdir.return_value = ['idlcompile.sh']
        ### test ###
        self.assertEqual((True, ""), self.test.build_rtc_python(rtcp))
        self.assertEqual(1, mock_write.call_count)
        mock_subprocess_call.assert_called_once()

    @mock.patch('subprocess.call')
    @mock.patch('os.listdir')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('os.path.split')
    def test_build_rtc_python_3(self, mock_split, mock_getcwd, mock_chdir, mock_write, mock_platform, mock_listdir, mock_subprocess_call):
        """build_rtc_python normal case
        sys.platform = 'linux'
        if 'idlcompile.sh' in os.listdir(os.getcwd()): False
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        mock_listdir.return_value = ['hoge']
        ### test ###
        self.assertEqual((True, ""), self.test.build_rtc_python(rtcp))
        self.assertEqual(1, mock_write.call_count)
        mock_subprocess_call.assert_not_called()

    @mock.patch('subprocess.call')
    @mock.patch('os.listdir')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('os.path.split')
    def test_build_rtc_python_4(self, mock_split, mock_getcwd, mock_chdir, mock_write, mock_platform, mock_listdir, mock_subprocess_call):
        """build_rtc_python normal case
        sys.platform = 'linux'
        if 'idlcompile.sh' in os.listdir(os.getcwd()): True
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        mock_listdir.return_value = ['idlcompile.sh']
        ### test ###
        self.assertEqual((True, ""), self.test.build_rtc_python(rtcp))
        self.assertEqual(1, mock_write.call_count)
        mock_subprocess_call.assert_called_once()

    @mock.patch('subprocess.call')
    @mock.patch('os.listdir')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('sys.stdout.write')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('os.path.split')
    def test_build_rtc_python_5(self, mock_split, mock_getcwd, mock_chdir, mock_write, mock_platform, mock_listdir, mock_subprocess_call):
        """build_rtc_python normal case
        sys.platform = 'win32'
        if 'idlcompile.sh' in os.listdir(os.getcwd()): False
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        mock_listdir.return_value = ['hoge']
        ### test ###
        self.assertEqual((True, ""), self.test.build_rtc_python(rtcp))
        self.assertEqual(1, mock_write.call_count)
        mock_subprocess_call.assert_not_called()

    @mock.patch('subprocess.call')
    @mock.patch('os.listdir')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('sys.stdout.write')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd')
    @mock.patch('os.path.split')
    def test_build_rtc_python_6(self, mock_split, mock_getcwd, mock_chdir, mock_write, mock_platform, mock_listdir, mock_subprocess_call):
        """build_rtc_python normal case
        sys.platform = 'win32'
        if 'idlcompile.sh' in os.listdir(os.getcwd()): True
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        mock_listdir.return_value = ['idlcompile.bat']
        ### test ###
        self.assertEqual((True, ""), self.test.build_rtc_python(rtcp))
        self.assertEqual(1, mock_write.call_count)
        mock_subprocess_call.assert_called_once()

    @mock.patch('subprocess.Popen')
    @mock.patch('os.walk')
    @mock.patch('os.listdir')
    @mock.patch('sys.platform', return_value='win32')
    @mock.patch('subprocess.call')
    @mock.patch('os.environ')
    @mock.patch('xml.etree.ElementTree')
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('os.path.join', return_value='')
    @mock.patch('os.path.split')
    def test_build_rtc_java_1(self, mock_split, mock_join, mock_getcwd, mock_chdir, mock_PIPE, mock_isdir, mock_makedirs, mock_et, mock_environ, mock_subprocess_call, mock_platform, mock_listdir, mock_walk, mock_Popen):
        """build_rtc_java normal case
        vrebose = False
        os.path.isdir = True
        if target.attrib['name'] == 'idlcompile': False , True
        if 'RTM_ROOT' in list(os.environ.keys()): True
        if not "CLASSPATH" in list(java_env.keys()): True
        sys.platform = win32
        ret != 0
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        type(self.admin_mock.environment).path = PropertyMock(return_value={'javac': 'javac_path'})
        mock_isdir.return_value = True
        mock_et(spec=['parse'])
        parse = MagicMock(spec=['findall'])
        target1 = MagicMock()
        type(target1).attrib = {'name': 'hoge'}
        target2 = MagicMock()
        type(target2).attrib = {'name': 'idcompile'}
        a = MagicMock()
        type(a).attrib = {'line': '1 2 3 4 56789'}
        type(target2).getiterator = {'arg': ''}
        parse.findall.return_value = [target1, target2]
        mock_et.parse.return_value = parse
        mock_environ(spec=['keys', 'copy'])
        mock_environ.keys.return_value = {'RTM_ROOT'}
        mock_environ.copy.return_value = {'RTM_JAVA_ROOT': 'java_root'}
        mock_listdir.return_value = ['listdir']
        mock_walk.return_value = [('root', 'dirs', ['hoge', 'test.jar'])]
        p = MagicMock(spec=['communicate', 'wait'])
        p.wait.return_value = -1
        p.communicate.return_value = ('stdout_data', None)
        #type(p).returncode = PropertyMock(side_effect=[0, -1])
        mock_Popen.return_value = p
        ### test ###
        self.assertEqual((False, 'stdout_data'), self.test.build_rtc_java(rtcp, verbose=False))
        self.assertEqual(0, mock_subprocess_call.call_count)

    @mock.patch('subprocess.Popen')
    @mock.patch('os.walk')
    @mock.patch('os.listdir')
    @mock.patch('sys.platform', return_value='win32')
    @mock.patch('subprocess.call')
    @mock.patch('os.environ')
    @mock.patch('xml.etree.ElementTree')
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('os.path.join', return_value='')
    @mock.patch('os.path.split')
    def test_build_rtc_java_2(self, mock_split, mock_join, mock_getcwd, mock_chdir, mock_PIPE, mock_isdir, mock_makedirs, mock_et, mock_environ, mock_subprocess_call, mock_platform, mock_listdir, mock_walk, mock_Popen):
        """build_rtc_java normal case
        vrebose = False
        os.path.isdir = True
        if target.attrib['name'] == 'idlcompile': False , True
        if 'RTM_ROOT' in list(os.environ.keys()): True
        if not "CLASSPATH" in list(java_env.keys()): True
        sys.platform = win32
        ret = 0
        ret = 0
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        type(self.admin_mock.environment).path = PropertyMock(return_value={'javac': 'javac_path'})
        mock_isdir.return_value = True
        mock_et(spec=['parse'])
        parse = MagicMock(spec=['findall'])
        target1 = MagicMock()
        type(target1).attrib = {'name': 'hoge'}
        target2 = MagicMock()
        type(target2).attrib = {'name': 'idcompile'}
        a = MagicMock()
        type(a).attrib = {'line': '1 2 3 4 56789'}
        type(target2).getiterator = {'arg': ''}
        parse.findall.return_value = [target1, target2]
        mock_et.parse.return_value = parse
        mock_environ(spec=['keys', 'copy'])
        mock_environ.keys.return_value = {'RTM_ROOT'}
        mock_environ.copy.return_value = {'RTM_JAVA_ROOT': 'java_root'}
        mock_listdir.return_value = ['listdir']
        p = MagicMock(spec=['communicate', 'wait'])
        p.wait.return_value = 0
        p.communicate.return_value = ('stdout_data', None)
        #type(p).returncode = PropertyMock(side_effect=[0, -1])
        mock_Popen.return_value = p
        mock_walk.side_effect = [[('root', 'dirs', ['hoge', 'test.jar'])],
                                 [('root', 'dirs', ['hoge', 'test.class'])]]
        mock_subprocess_call.return_value = 0
        ### test ###
        self.assertEqual((True, ''), self.test.build_rtc_java(rtcp, verbose=False))
        self.assertEqual(1, mock_subprocess_call.call_count)

    @mock.patch('subprocess.Popen')
    @mock.patch('os.walk')
    @mock.patch('os.listdir')
    @mock.patch('sys.platform', return_value='win32')
    @mock.patch('subprocess.call')
    @mock.patch('os.environ')
    @mock.patch('xml.etree.ElementTree')
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('os.path.join', return_value='')
    @mock.patch('os.path.split')
    def test_build_rtc_java_3(self, mock_split, mock_join, mock_getcwd, mock_chdir, mock_PIPE, mock_isdir, mock_makedirs, mock_et, mock_environ, mock_subprocess_call, mock_platform, mock_listdir, mock_walk, mock_Popen):
        """build_rtc_java normal case
        vrebose = False
        os.path.isdir = True
        if target.attrib['name'] == 'idlcompile': False , True
        if 'RTM_ROOT' in list(os.environ.keys()): True
        if not "CLASSPATH" in list(java_env.keys()): True
        sys.platform = win32
        ret = 0
        ret != 0
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        type(self.admin_mock.environment).path = PropertyMock(return_value={'javac': 'javac_path'})
        mock_isdir.return_value = True
        mock_et(spec=['parse'])
        parse = MagicMock(spec=['findall'])
        target1 = MagicMock()
        type(target1).attrib = {'name': 'hoge'}
        target2 = MagicMock()
        type(target2).attrib = {'name': 'idcompile'}
        a = MagicMock()
        type(a).attrib = {'line': '1 2 3 4 56789'}
        type(target2).getiterator = {'arg': ''}
        parse.findall.return_value = [target1, target2]
        mock_et.parse.return_value = parse
        mock_environ(spec=['keys', 'copy'])
        mock_environ.keys.return_value = {'RTM_ROOT'}
        mock_environ.copy.return_value = {'RTM_JAVA_ROOT': 'java_root'}
        mock_listdir.return_value = ['listdir']
        p = MagicMock(spec=['communicate', 'wait'])
        p.wait.return_value = 0
        p.communicate.return_value = ('stdout_data', None)
        #type(p).returncode = PropertyMock(side_effect=[0, -1])
        mock_Popen.return_value = p
        mock_walk.side_effect = [[('root', 'dirs', ['hoge', 'test.jar'])],
                                 [('root', 'dirs', ['hoge', 'test.class'])]]
        mock_subprocess_call.return_value = -1
        ### test ###
        self.assertEqual(None, self.test.build_rtc_java(rtcp, verbose=False))
        self.assertEqual(1, mock_subprocess_call.call_count)

    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.Popen')
    @mock.patch('os.walk')
    @mock.patch('os.listdir')
    @mock.patch('sys.platform', return_value='win32')
    @mock.patch('subprocess.call')
    @mock.patch('os.environ')
    @mock.patch('xml.etree.ElementTree')
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('os.path.join', return_value='')
    @mock.patch('os.path.split')
    def test_build_rtc_java_4(self, mock_split, mock_join, mock_getcwd, mock_chdir, mock_PIPE, mock_isdir, mock_makedirs, mock_et, mock_environ, mock_subprocess_call, mock_platform, mock_listdir, mock_walk, mock_Popen, mock_write):
        """build_rtc_java normal case
        vrebose = True
        os.path.isdir = True
        if target.attrib['name'] == 'idlcompile': False , True
        if 'RTM_ROOT' in list(os.environ.keys()): True
        if not "CLASSPATH" in list(java_env.keys()): True
        sys.platform = win32
        ret = 0
        ret != 0
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        type(self.admin_mock.environment).path = PropertyMock(return_value={'javac': 'javac_path'})
        mock_isdir.return_value = True
        mock_et(spec=['parse'])
        parse = MagicMock(spec=['findall'])
        target1 = MagicMock()
        type(target1).attrib = {'name': 'hoge'}
        target2 = MagicMock()
        type(target2).attrib = {'name': 'idcompile'}
        a = MagicMock()
        type(a).attrib = {'line': '1 2 3 4 56789'}
        type(target2).getiterator = {'arg': ''}
        parse.findall.return_value = [target1, target2]
        mock_et.parse.return_value = parse
        mock_environ(spec=['keys', 'copy'])
        mock_environ.keys.return_value = {'RTM_ROOT'}
        mock_environ.copy.return_value = {'RTM_JAVA_ROOT': 'java_root'}
        mock_listdir.return_value = ['listdir']
        p = MagicMock(spec=['communicate', 'wait'])
        p.wait.return_value = 0
        p.communicate.return_value = ('stdout_data', None)
        #type(p).returncode = PropertyMock(side_effect=[0, -1])
        mock_Popen.return_value = p
        mock_walk.side_effect = [[('root', 'dirs', ['hoge', 'test.jar'])],
                                 [('root', 'dirs', ['hoge', 'test.class'])]]
        mock_subprocess_call.return_value = -1
        ### test ###
        self.assertEqual(None, self.test.build_rtc_java(rtcp, verbose=True))
        self.assertEqual(1, mock_subprocess_call.call_count)
        self.assertEqual(6, mock_write.call_count)

    @mock.patch('os.path.isfile')
    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.Popen')
    @mock.patch('os.walk')
    @mock.patch('os.listdir')
    @mock.patch('sys.platform', return_value='win32')
    @mock.patch('subprocess.call')
    @mock.patch('os.environ')
    @mock.patch('xml.etree.ElementTree.parse')
    @mock.patch('os.makedirs')
    @mock.patch('os.path.isdir')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd', return_value='')
    @mock.patch('os.path.join', return_value='')
    @mock.patch('os.path.split')
    def test_build_rtc_java_5(self, mock_split, mock_join, mock_getcwd, mock_chdir, mock_PIPE, mock_isdir, mock_makedirs, mock_et, mock_environ, mock_subprocess_call, mock_platform, mock_listdir, mock_walk, mock_Popen, mock_write, mock_isfile):
        """build_rtc_java normal case
        vrebose = True
        os.path.isdir = False
        os.isfile = True
        if target.attrib['name'] == 'idlcompile': False , True
        if 'RTM_ROOT' in list(os.environ.keys()): True
        if not "CLASSPATH" in list(java_env.keys()): True
        sys.platform = win32
        ret = 0
        ret != 0
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        type(self.admin_mock.environment).path = PropertyMock(return_value={'javac': 'javac_path'})
        mock_isdir.return_value = False
        mock_isfile.return_file = True
        # mock_et(spec=['parse'])
        parse = MagicMock(spec=['findall'])
        target1 = MagicMock()
        type(target1).attrib = {'name': 'hoge'}
        target2 = MagicMock()
        type(target2).attrib = {'name': 'idcompile'}
        a = MagicMock()
        type(a).attrib = {'line': '1 2 3 4 56789'}
        type(target2).getiterator = {'arg': ''}
        parse.findall.return_value = [target1, target2]
        mock_et.return_value = parse
        mock_environ(spec=['keys', 'copy'])
        mock_environ.keys.return_value = {'RTM_ROOT'}
        mock_environ.copy.return_value = {'RTM_JAVA_ROOT': 'java_root'}
        mock_listdir.return_value = ['listdir']
        p = MagicMock(spec=['communicate', 'wait'])
        p.wait.return_value = 0
        p.communicate.return_value = ('stdout_data', None)
        #type(p).returncode = PropertyMock(side_effect=[0, -1])
        mock_Popen.return_value = p
        mock_walk.side_effect = [[('root', 'dirs', ['hoge', 'test.jar'])],
                                 [('root', 'dirs', ['hoge', 'test.class'])]]
        mock_subprocess_call.return_value = -1
        ### test ###
        self.assertEqual(None, self.test.build_rtc_java(rtcp, verbose=True))
        self.assertEqual(1, mock_subprocess_call.call_count)
        self.assertEqual(6, mock_write.call_count)

    @mock.patch('os.remove')
    @mock.patch('os.getcwd')
    @mock.patch('os.path.join')
    @mock.patch('os.walk')
    @mock.patch('shutil.rmtree')
    @mock.patch('builtins.print')
    @mock.patch('os.path.isdir')
    @mock.patch('sys.platform', return_value='hoge')
    @mock.patch('os.path.split')
    def test_clean_rtc_cpp_1(self, mock_split, mock_platform, mock_isdir, mock_print, mock_rmtree, mock_walk, mock_join, mock_getcwd, mock_remove):
        """clean_rtc_cpp normal case
        verbose = True
        os.path.isdir = True
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        mock_isdir.return_value = True
        mock_walk.return_value = [('root', 'dirs', ['hoge', 'test1234~', 'test5678~'])]
        mock_join.side_effect = ['build_dir', '1234', '', 'test5678', '']
        mock_getcwd.return_value = 'test'
        ### test ###
        self.assertEqual((True, None), self.test.clean_rtc_cpp(rtcp, verbose=True))
        self.assertEqual(3, mock_print.call_count)
        self.assertEqual(1, mock_rmtree.call_count)
        self.assertEqual(2, mock_remove.call_count)
        self.assertEqual(3, mock_getcwd.call_count)
        self.assertEqual(5, mock_join.call_count)

    @mock.patch('os.remove')
    @mock.patch('os.getcwd')
    @mock.patch('os.path.join')
    @mock.patch('os.walk')
    @mock.patch('shutil.rmtree')
    @mock.patch('builtins.print')
    @mock.patch('os.path.isdir')
    @mock.patch('sys.platform', return_value='hoge')
    @mock.patch('os.path.split')
    def test_clean_rtc_cpp_2(self, mock_split, mock_platform, mock_isdir, mock_print, mock_rmtree, mock_walk, mock_join, mock_getcwd, mock_remove):
        """clean_rtc_cpp normal case
        verbose = False
        os.path.isdir = False
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        mock_isdir.return_value = False
        mock_walk.return_value = [('root', 'dirs', ['hoge', 'test1234~', 'test5678~'])]
        mock_join.side_effect = ['build_dir', '1234', '', 'test5678', '']
        mock_getcwd.return_value = 'test'
        ### test ###
        self.assertEqual((True, None), self.test.clean_rtc_cpp(rtcp, verbose=False))
        self.assertEqual(0, mock_print.call_count)
        self.assertEqual(0, mock_rmtree.call_count)
        self.assertEqual(2, mock_remove.call_count)
        self.assertEqual(3, mock_getcwd.call_count)
        self.assertEqual(5, mock_join.call_count)

    @mock.patch('os.remove')
    @mock.patch('os.getcwd')
    @mock.patch('os.path.join')
    @mock.patch('os.walk')
    @mock.patch('shutil.rmtree')
    @mock.patch('builtins.print')
    @mock.patch('os.path.isdir')
    @mock.patch('sys.platform', return_value='hoge')
    @mock.patch('os.path.split')
    def test_clean_rtc_java_1(self, mock_split, mock_platform, mock_isdir, mock_print, mock_rmtree, mock_walk, mock_join, mock_getcwd, mock_remove):
        """clean_rtc_java normal case
        verbose = True
        os.path.isdir = True
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        mock_isdir.return_value = True
        mock_walk.return_value = [('root', 'dirs', ['hoge', 'test1234~', 'test5678~'])]
        mock_join.side_effect = ['build_dir', '1234', '', 'test5678', '']
        mock_getcwd.return_value = 'test'
        ### test ###
        self.assertEqual((True, None), self.test.clean_rtc_java(rtcp, verbose=True))
        self.assertEqual(3, mock_print.call_count)
        self.assertEqual(1, mock_rmtree.call_count)
        self.assertEqual(2, mock_remove.call_count)
        self.assertEqual(3, mock_getcwd.call_count)
        self.assertEqual(5, mock_join.call_count)

    @mock.patch('os.remove')
    @mock.patch('os.getcwd')
    @mock.patch('os.path.join')
    @mock.patch('os.walk')
    @mock.patch('shutil.rmtree')
    @mock.patch('builtins.print')
    @mock.patch('os.path.isdir')
    @mock.patch('sys.platform', return_value='hoge')
    @mock.patch('os.path.split')
    def test_clean_rtc_java_2(self, mock_split, mock_platform, mock_isdir, mock_print, mock_rmtree, mock_walk, mock_join, mock_getcwd, mock_remove):
        """clean_rtc_java normal case
        verbose = False
        os.path.isdir = False
        """
        ### setting ###
        rtcp = MagicMock(spec=['basicInfo'])
        type(rtcp.basicInfo).name = PropertyMock(return_value='rtcp_name')
        type(rtcp).filename = PropertyMock(return_value='rtcp_filename')
        mock_split.return_value = 'rtc_dir', None
        mock_isdir.return_value = False
        mock_walk.return_value = [('root', 'dirs', ['hoge', 'test1234~', 'test5678~'])]
        mock_join.side_effect = ['build_dir', '1234', '', 'test5678', '']
        mock_getcwd.return_value = 'test'
        ### test ###
        self.assertEqual((True, None), self.test.clean_rtc_java(rtcp, verbose=False))
        self.assertEqual(0, mock_print.call_count)
        self.assertEqual(0, mock_rmtree.call_count)
        self.assertEqual(2, mock_remove.call_count)
        self.assertEqual(3, mock_getcwd.call_count)
        self.assertEqual(5, mock_join.call_count)

    def test_clean_rtc_python(self):
        """clean_rtc_python normal case"""
        ### test ###
        self.assertEqual((True, None), self.test.clean_rtc_python('rtcp', verbose=False))


if __name__ == '__main__':
    unittest.main()
