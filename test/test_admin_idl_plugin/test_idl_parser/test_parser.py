# test for wasanbon/core/plugins/admin/idl_plugin/idl_parser/parser.py

import os
import tempfile
import unittest
from unittest import mock
from unittest.mock import Mock, call

from wasanbon.core.plugins.admin.idl_plugin.idl_parser import parser


class TestPlugin(unittest.TestCase):

    def test_init(self):
        """test for init"""
        test_dirs = 'test_dirs'
        # test
        idl_parser = parser.IDLParser(test_dirs)
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser.module import \
            IDLModule
        self.assertIsInstance(idl_parser._global_module, IDLModule)
        self.assertEqual(idl_parser._dirs, test_dirs)
        self.assertEqual(idl_parser._verbose, False)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.is_primitive')
    def test_is_primitive(self, primitive_mock):
        """test for is_primitive"""
        test_dirs = 'test_dirs'
        idl_parser = parser.IDLParser(test_dirs)
        # test
        test_name = 'test name'
        idl_parser.is_primitive(test_name)
        primitive_mock.assert_called_once_with(test_name)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.parser.IDLParser.forEachIDL')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.parser.IDLParser.parse_idl')
    def test_parse(self, parse_idl_mock, each_idl_mock):
        """test for parse"""
        test_dirs = 'test_dirs'
        idl_parser = parser.IDLParser(test_dirs)
        # test
        test_idls = ['test1']
        test_exept_files = ['test1']
        idl_parser.parse(idls=test_idls, except_files=test_exept_files)
        each_idl_mock.assert_called_once_with(
            parse_idl_mock, except_files=test_exept_files, idls=test_idls)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.module.IDLModule')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.token_buffer.TokenBuffer')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.parser.IDLParser._clear_comments')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.parser.IDLParser._clear_ifdef')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.parser.IDLParser._paste_include')
    @mock.patch('sys.stdout.write')
    def test_parse_idl(self, sys_stdout_write, paste_include_mock, clear_ifdef_mock, clear_comments_mock, token_buffer_mock, idl_module_mock):
        """test for parse_idl"""
        test_dirs = 'test_dirs'
        idl_parser = parser.IDLParser(test_dirs)
        idl_parser._verbose = True
        # make temporary file
        test_lines1 = 'abc\n'
        test_lines2 = '123\n'
        test_lines = test_lines1 + test_lines2
        # mock settings
        clear_comments_mock.return_value = [test_lines1, test_lines2]
        paste_include_mock.return_value = [test_lines1, test_lines2]
        clear_ifdef_mock.return_value = [test_lines1, test_lines2]
        token_buffer_mock.return_value = ['test1']
        with tempfile.TemporaryDirectory() as tmp:
            test_idl_path = os.path.join(tmp, 'test_file')
            with open(test_idl_path, 'w') as f:
                f.write(test_lines)
            # test
            idl_parser.parse_idl(test_idl_path)
        sys_calls = [call(' - Parsing IDL (%s)\n' % test_idl_path)]
        sys_stdout_write.assert_has_calls(sys_calls)
        clear_comments_mock.assert_called_once_with([test_lines1, test_lines2])
        paste_include_mock.assert_called_once_with([test_lines1, test_lines2])
        clear_ifdef_mock.assert_called_once_with([test_lines1, test_lines2])
        token_buffer_mock.assert_called_once_with([test_lines1, test_lines2])
        idl_module_calls = [
            call(),
            call().parse_tokens(['test1'], filepath=test_idl_path)
        ]
        idl_module_mock.assert_has_calls(idl_module_calls)

    @mock.patch('os.listdir', return_value=['test1.idl'])
    @mock.patch('sys.stdout.write')
    def test_forEachIDL(self, sys_stdout_write, _):
        """test for forEachIDL"""
        test_dirs = ['test_dirs']
        idl_parser = parser.IDLParser(test_dirs)
        idl_parser._verbose = True
        # test
        test_func = Mock()
        test_idl_dirs = ['dir1']
        test_except_files = ['except1']
        test_idls = ['idl1']
        idl_parser.forEachIDL(test_func, test_idl_dirs,
                              test_except_files, test_idls)
        file_path = os.path.join(test_dirs[0], 'test1.idl')
        sys_calls = [call(' - Apply function to %s\n' % file_path)]
        sys_stdout_write.assert_has_calls(sys_calls)
        test_func_calls = [call(file_path), call(test_idls[0])]
        test_func.assert_has_calls(test_func_calls)

    @mock.patch('sys.stdout.write')
    def test_find_idl(self, sys_stdout_write):
        """test for _find_idl"""
        test_dirs = ['test_dirs']
        idl_parser = parser.IDLParser(test_dirs)
        idl_parser._verbose = True
        # overwrite forEachIDL
        def mock_for_each_idl(func, idl_dirs):
            return func(idl_dirs)
        idl_parser.forEachIDL = mock_for_each_idl
        # test
        test_func = Mock()
        test_func.return_value = 'mock_return'
        test_filename = 'test_filename'
        test_idl_dirs = os.path.join('dir1', test_filename)
        ret = idl_parser._find_idl(test_filename, test_func, test_idl_dirs)
        sys_calls = [call(' --- Find %s\n' % test_filename)]
        sys_stdout_write.assert_has_calls(sys_calls)
        test_func_calls = [call(test_idl_dirs)]
        test_func.assert_has_calls(test_func_calls)
        self.assertEqual(ret, 'mock_return')

    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.parser.IDLParser._find_idl')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.parser.IDLParser._clear_comments')
    def test_paste_include_original_file(self, clear_comments_mock, find_idl_mock, open_mock, sys_stdout_write):
        """test for _paste_include (#include "file.h")"""
        test_dirs = ['test_dirs']
        idl_parser = parser.IDLParser(test_dirs)
        idl_parser._verbose = True
        # mock setting
        test_idl_file = 'test.idl'
        find_idl_mock.return_value = test_idl_file
        open_mock.return_value = ['l1']
        clear_comments_mock.return_value = ['l1']
        # test
        include_filename = 'test1.h'
        test_lines = ['#include "{}"'.format(include_filename)]
        ret = idl_parser._paste_include(test_lines)
        sys_calls = [call(' -- Includes %s\n' % include_filename)]
        sys_stdout_write.assert_has_calls(sys_calls)
        find_idl_mock.assert_called_once()
        clear_comments_mock.assert_has_calls([call(['l1'])])
        self.assertEqual(ret, ['l1', ''])

    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.parser.IDLParser._find_idl')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.parser.IDLParser._clear_comments')
    def test_paste_include_library_file(self, clear_comments_mock, find_idl_mock, open_mock, sys_stdout_write):
        """test for _paste_include (#include <file.h>)"""
        test_dirs = ['test_dirs']
        idl_parser = parser.IDLParser(test_dirs)
        idl_parser._verbose = True
        # mock setting
        test_idl_file = 'test.idl'
        find_idl_mock.return_value = test_idl_file
        open_mock.return_value = ['l1']
        clear_comments_mock.return_value = ['l1']
        # test
        include_filename = 'test1.h'
        test_lines = ['#include <{}>'.format(include_filename)]
        ret = idl_parser._paste_include(test_lines)
        sys_calls = [call(' -- Includes %s\n' % include_filename)]
        sys_stdout_write.assert_has_calls(sys_calls)
        find_idl_mock.assert_called_once()
        clear_comments_mock.assert_has_calls([call(['l1'])])
        self.assertEqual(ret, ['l1', ''])

    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.parser.IDLParser._find_idl')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.parser.IDLParser._clear_comments')
    def test_paste_include_not_found(self, clear_comments_mock, find_idl_mock, open_mock, sys_stdout_write):
        """test for _paste_include file not found"""
        test_dirs = ['test_dirs']
        idl_parser = parser.IDLParser(test_dirs)
        idl_parser._verbose = True
        # mock setting
        find_idl_mock.return_value = None
        open_mock.return_value = ['l1']
        clear_comments_mock.return_value = ['l1']
        # test ("")
        include_filename = 'test1.h'
        test_lines = ['#include "{}"'.format(include_filename)]
        with self.assertRaises(FileNotFoundError):
            idl_parser._paste_include(test_lines)
        sys_calls = [
            call(' -- Includes %s\n' % include_filename),
            call(' # IDL (%s) can not be found.\n' % include_filename)
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        find_idl_mock.assert_called_once()
        clear_comments_mock.assert_not_called()
        # test (<>)
        include_filename = 'test1.h'
        test_lines = ['#include "<>"'.format(include_filename)]
        with self.assertRaises(FileNotFoundError):
            idl_parser._paste_include(test_lines)
        sys_calls = [
            call(' -- Includes %s\n' % include_filename),
            call(' # IDL (%s) can not be found.\n' % include_filename)
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        self.assertEqual(find_idl_mock.call_count, 2)
        clear_comments_mock.assert_not_called()

    def test_clear_comments(self):
        """test for _clear_comments"""
        test_dirs = ['test_dirs']
        idl_parser = parser.IDLParser(test_dirs)
        idl_parser._verbose = True
        # test(startwith //)
        test_lines = ['// //']
        ret = idl_parser._clear_comments(test_lines)
        self.assertEqual(ret, [])
        # test(/* */)
        test_lines = ['ab/* c d*/ef']
        ret = idl_parser._clear_comments(test_lines)
        self.assertEqual(ret, ['ab ef\n'])
        # test(else)
        test_lines = ['ab{cd;ef(g,)}']
        ret = idl_parser._clear_comments(test_lines)
        self.assertEqual(ret, ['ab { cd ;ef ( g ,  )  }\n'])

    def test_clear_ifdef(self):
        """test for _clear_ifdef"""
        test_dirs = ['test_dirs']
        idl_parser = parser.IDLParser(test_dirs)
        idl_parser._verbose = True
        # test
        test_lines = ['#define a', '#ifdef a', '#ifndef b', '#endif']
        ret = idl_parser._clear_ifdef(test_lines)
        self.assertEqual(ret, [])

    def test_properties(self):
        """test for properties"""
        test_dirs = 'test_dirs'
        idl_parser = parser.IDLParser(test_dirs)
        # test
        self.assertEqual(idl_parser.global_module, idl_parser._global_module)
        self.assertEqual(idl_parser.dirs, idl_parser._dirs)


if __name__ == '__main__':
    unittest.main()
