# test for wasanbon/core/plugins/admin/rtcconf_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')


class TestRTCConf(unittest.TestCase):

    class FunctionList:
        pass

    @mock.patch('builtins.open')
    def setUp(self, mock_open):
        fin = MagicMock(spec=['readline'])
        fin.readline.side_effect = ['#comment', '1:\\', 'hoge', False]
        mock_open.return_value = fin
        import wasanbon.core.plugins.admin.rtcconf_plugin as m
        from wasanbon.core.plugins.admin.rtcconf_plugin import RTCConf
        self.test = RTCConf('rtcconf', verbose=False)

    @mock.patch('builtins.print')
    @mock.patch('builtins.open')
    @mock.patch('sys.stdout.write')
    def test_init_1(self, mock_write, mock_open, mock_print):
        """__init__ normal case
        verbose = False
        len(nv)>2
        """
        ### setting ###
        fin = MagicMock(spec=['readline'])
        fin.readline.side_effect = ['#comment', '1:\\', 'hoge', False]
        mock_open.return_value = fin
        import wasanbon.core.plugins.admin.rtcconf_plugin as m
        from wasanbon.core.plugins.admin.rtcconf_plugin import RTCConf
        test = RTCConf('rtcconf', verbose=False)
        ### test ###
        self.assertEqual({'1': 'hoge'}, test.dic)
        self.assertEqual('rtcconf', test.filename)
        self.assertEqual(0, mock_print.call_count)

    @mock.patch('builtins.print')
    @mock.patch('builtins.open')
    @mock.patch('sys.stdout.write')
    def test_init_2(self, mock_write, mock_open, mock_print):
        """__init__ normal case
        verbose = True
        len(nv)<=2
        """
        ### setting ###
        fin = MagicMock(spec=['readline'])
        fin.readline.side_effect = ['#comment', '1\\', 'hoge', False]
        mock_open.return_value = fin
        import wasanbon.core.plugins.admin.rtcconf_plugin as m
        from wasanbon.core.plugins.admin.rtcconf_plugin import RTCConf
        test = RTCConf('rtcconf', verbose=True)
        ### test ###
        self.assertEqual({}, test.dic)
        self.assertEqual('rtcconf', test.filename)
        self.assertEqual(2, mock_print.call_count)
        self.assertEqual(1, mock_write.call_count)

    def test__str__(self):
        """__str__ normal case"""
        ### test ###
        self.assertEqual(str({'1': 'hoge'}), str(self.test))

    def test_keys(self):
        """keys normal case"""
        ### test ###
        self.assertEqual(list({'1': 'hoge'}.keys()), self.test.keys())

    def test_values(self):
        """values normal case"""
        ### test ###
        self.assertEqual(list({'1': 'hoge'}.values()), self.test.values())

    def test_items(self):
        """items normal case"""
        ### test ###
        temp = {'1': 'hoge'}
        self.assertEqual(list(zip(list(temp.keys()), list(temp.values()))), self.test.items())

    def test__getitem__(self):
        """__getitem__ normal case"""
        ### test ###
        self.assertEqual('hoge', self.test['1'])
        self.assertEqual('', self.test['2'])

    def test__setitem__(self):
        """__setitem__ normal case"""
        ### test ###
        self.assertEqual('hoge', self.test['1'])
        self.test['1'] = 'test'
        self.assertEqual('test', self.test['1'])
        self.assertEqual('', self.test['2'])
        self.test['2'] = 'test'
        self.assertEqual('test', self.test['2'])

    def test_pop(self):
        """pop normal case"""
        ### test ###
        self.assertEqual('hoge', self.test['1'])
        self.assertEqual(None, self.test.pop('1'))
        self.assertEqual('', self.test['1'])

    @mock.patch('sys.stdout.write')
    def test_append_1(self, mock_write):
        """append normal case
        """
        ### test ###
        # if not key in list(self.dic.keys()): True
        # verbose = False
        self.assertEqual(1, self.test.append('test', 'test', verbose=False))
        self.assertEqual(0, mock_write.call_count)
        self.assertEqual('test', self.test['test'])
        # if not key in list(self.dic.keys()): True
        # verbose = True
        self.assertEqual(None, self.test.pop('test'))
        self.assertEqual('', self.test['test'])
        self.assertEqual(1, self.test.append('test', 'test', verbose=True))
        self.assertEqual(1, mock_write.call_count)
        # if not key in list(self.dic.keys()): False
        # len(self.dic[key].strip()) == 0:
        self.assertEqual(None, self.test.pop('test'))
        self.assertEqual('', self.test['test'])
        self.assertEqual(1, self.test.append('test', '', verbose=False))
        self.assertEqual(1, self.test.append('test', 'test', verbose=True))
        self.assertEqual(1, mock_write.call_count)

    @mock.patch('sys.stdout.write')
    def test_append_2(self, mock_write):
        """append normal case
        # if not key in list(self.dic.keys()): False
        # len(self.dic[key].strip()) != 0:
        """
        ### test ###
        # if not value in values: True
        self.assertEqual(1, self.test.append('test', 'test'))
        self.assertEqual(1, self.test.append('test', 'hoge'))
        self.assertEqual('test,hoge', self.test['test'])
        self.assertEqual(0, mock_write.call_count)
        # if not value in values: False
        # verbose = True
        # allow_duplicate = False
        self.assertEqual(0, self.test.append('test', 'hoge', verbose=True, allow_duplicate=False))
        self.assertEqual('test,hoge', self.test['test'])
        self.assertEqual(1, mock_write.call_count)
        # if not value in values: False
        # verbose = True
        # allow_duplicate = True
        self.assertEqual(2, self.test.append('test', 'hoge', verbose=True, allow_duplicate=True))
        self.assertEqual('test,hoge,hoge', self.test['test'])
        self.assertEqual(3, mock_write.call_count)

    @mock.patch('sys.stdout.write')
    def test_remove_1(self, mock_write):
        """remove normal case
        verbose=False
        if not key in list(self.dic.keys()): True
        """
        ### test ###
        self.assertEqual(None, self.test.remove('nokey', verbose=False))
        self.assertEqual(0, mock_write.call_count)

    @mock.patch('sys.stdout.write')
    def test_remove_2(self, mock_write):
        """remove normal case
        verbose=True
        if not key in list(self.dic.keys()): False
        elif len(self.dic[key].strip()) == 0: True
        """
        ### test ###
        self.test['test'] = ''
        self.assertEqual(None, self.test.remove('test', verbose=True))
        self.assertEqual(1, mock_write.call_count)

    @mock.patch('sys.stdout.write')
    def test_remove_3(self, mock_write):
        """remove normal case
        verbose=True
        if not key in list(self.dic.keys()): False
        elif len(self.dic[key].strip()) == 0: False
        value = None
        """
        ### test ###
        self.test['test'] = 'hoge'
        self.assertEqual(None, self.test.remove('test', value=None, verbose=True))
        self.assertEqual('', self.test['test'])
        self.assertEqual(1, mock_write.call_count)

    @mock.patch('sys.stdout.write')
    def test_remove_4(self, mock_write):
        """remove normal case
        verbose=True
        if not key in list(self.dic.keys()): False
        elif len(self.dic[key].strip()) == 0: False
        value = hoge
        """
        ### test ###
        self.test['test'] = 'test,hoge,test'
        self.assertEqual(None, self.test.remove('test', value='hoge', verbose=True))
        self.assertEqual('test,test', self.test['test'])
        self.assertEqual(1, mock_write.call_count)

    @mock.patch('builtins.open')
    @mock.patch('os.rename')
    @mock.patch('os.remove')
    @mock.patch('os.path.isfile')
    def test_sync_1(self, mock_isfile, mock_remove, mock_rename, mock_open):
        """sync normal case
        if len(outfilename) == 0: True
        if os.path.isfile(backup_filename): True
        if not line_new: True
        """
        ### setting ###
        mock_isfile.side_effect = [True, True]
        fin = MagicMock(spec=['readline'])
        fin.readline.side_effect = ['#1', '2\\', None]
        fout = MagicMock(spec=['write'])
        mock_open.side_effect = [fin, fout]
        ### test ###
        self.assertEqual(None, self.test.sync())
        self.assertEqual(1, fout.write.call_count)
        self.assertEqual(1, mock_remove.call_count)
        self.assertEqual(1, mock_rename.call_count)

    @mock.patch('builtins.print')
    @mock.patch('builtins.open')
    @mock.patch('os.rename')
    @mock.patch('os.remove')
    @mock.patch('os.path.isfile')
    def test_sync_2(self, mock_isfile, mock_remove, mock_rename, mock_open, mock_print):
        """sync normal case
        if len(outfilename) == 0: True
        if os.path.isfile(backup_filename): False
        if not line_new: True
        if len(nv) < 2: True
        """
        ### setting ###
        mock_isfile.side_effect = [False, True]
        fin = MagicMock(spec=['readline'])
        fin.readline.side_effect = ['#1', '2\\', '3']
        fout = MagicMock(spec=['write'])
        mock_open.side_effect = [fin, fout]
        ### test ###
        self.assertEqual(None, self.test.sync())
        self.assertEqual(1, fout.write.call_count)
        self.assertEqual(0, mock_remove.call_count)
        self.assertEqual(1, mock_rename.call_count)
        self.assertEqual(2, mock_print.call_count)

    @mock.patch('builtins.open')
    @mock.patch('os.rename')
    @mock.patch('os.remove')
    @mock.patch('os.path.isfile')
    def test_sync_3(self, mock_isfile, mock_remove, mock_rename, mock_open):
        """sync normal case
        if len(outfilename) == 0: True
        if os.path.isfile(backup_filename): False
        if not line_new: True
        if len(nv) > 2: True
        """
        ### setting ###
        mock_isfile.side_effect = [False, True]
        fin = MagicMock(spec=['readline', 'close'])
        fin.readline.side_effect = ['#1', '2:\\', '3:\\', '4\\', '5', ' ', None]
        fout = MagicMock(spec=['write', 'close'])
        mock_open.side_effect = [fin, fout]
        ### test ###
        self.assertEqual(None, self.test.sync())
        self.assertEqual(3, fout.write.call_count)
        self.assertEqual(1, mock_remove.call_count)
        self.assertEqual(1, mock_rename.call_count)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.get_bin_file_ext', return_value='exe')
    def test_ext_check_1(self, mock_get_bin_file_ext, mock_write):
        """ext_check normal case
        verbose = False
        autofix = False
        interactive = False
        if not rtcbin.endswith(wasanbon.get_bin_file_ext()): True
        """
        self.test['manager.modules.preload'] = 'test.exe'
        ### test ###
        self.assertEqual(None, self.test.ext_check())
        self.assertEqual('', self.test['manager.modules.preload'])
        self.assertEqual(0, mock_write.call_count)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.get_bin_file_ext', return_value='.exe')
    def test_ext_check_2(self, mock_get_bin_file_ext, mock_write):
        """ext_check normal case
        verbose = False
        autofix = False
        interactive = False
        if not rtcbin.endswith(wasanbon.get_bin_file_ext()): True
        """
        self.test['manager.modules.preload'] = 'test.hoge'
        ### test ###
        self.assertEqual(None, self.test.ext_check())
        self.assertEqual('', self.test['manager.modules.preload'])
        self.assertEqual(0, mock_write.call_count)
        self.assertEqual(2, mock_get_bin_file_ext.call_count)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.get_bin_file_ext', return_value='.exe')
    def test_ext_check_3(self, mock_get_bin_file_ext, mock_write):
        """ext_check normal case
        verbose = True
        autofix = True
        interactive = False
        if not rtcbin.endswith(wasanbon.get_bin_file_ext()): True
        """
        self.test['manager.modules.preload'] = 'test.hoge'
        ### test ###
        self.assertEqual(None, self.test.ext_check(verbose=True, autofix=True))
        self.assertEqual('test.exe', self.test['manager.modules.preload'])
        self.assertEqual(2, mock_write.call_count)
        self.assertEqual(2, mock_get_bin_file_ext.call_count)

    @mock.patch('wasanbon.util.yes_no', return_value='yes')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.get_bin_file_ext', return_value='.exe')
    def test_ext_check_4(self, mock_get_bin_file_ext, mock_write, mock_yes_no):
        """ext_check normal case
        verbose = False
        autofix = False
        interactive = True
        if not rtcbin.endswith(wasanbon.get_bin_file_ext()): True
        """
        self.test['manager.modules.preload'] = 'test.hoge'
        ### test ###
        self.assertEqual(None, self.test.ext_check(verbose=False, autofix=False, interactive=True))
        self.assertEqual('test.exe', self.test['manager.modules.preload'])
        self.assertEqual(2, mock_write.call_count)
        self.assertEqual(2, mock_get_bin_file_ext.call_count)

    @mock.patch('wasanbon.util.yes_no', return_value='no')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.get_bin_file_ext', return_value='.exe')
    def test_ext_check_5(self, mock_get_bin_file_ext, mock_write, mock_yes_no):
        """ext_check normal case
        verbose = False
        autofix = False
        interactive = True
        if not rtcbin.endswith(wasanbon.get_bin_file_ext()): True
        """
        self.test['manager.modules.preload'] = 'test.hoge'
        ### test ###
        self.assertEqual(None, self.test.ext_check(verbose=False, autofix=False, interactive=True))
        self.assertEqual('test.hoge', self.test['manager.modules.preload'])
        self.assertEqual(1, mock_write.call_count)
        self.assertEqual(2, mock_get_bin_file_ext.call_count)

    @mock.patch('sys.stdout.write')
    def test_validate_1(self, mock_write):
        """validate normal case"""
        self.assertEqual(None, self.test.validate(verbose=False, autofix=False, interactive=True))
        self.assertEqual(0, mock_write.call_count)

    @mock.patch('sys.stdout.write')
    def test_validate_2(self, mock_write):
        """validate normal case"""
        self.assertEqual(None, self.test.validate(verbose=True, autofix=False, interactive=True))
        self.assertEqual(1, mock_write.call_count)


if __name__ == '__main__':
    unittest.main()
