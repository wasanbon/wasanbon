# test for wasanbon/core/plugins/admin/idl_plugin/idl_parser/enum.py

import unittest
from unittest import mock
from unittest.mock import Mock, call

from wasanbon.core.plugins.admin.idl_plugin.idl_parser import enum


class TestPlugin(unittest.TestCase):

    def test_idl_enum_value_init(self):
        """test for IDLEnumValue.__init__"""
        test_value = 123
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        # test
        idl_enum_value = enum.IDLEnumValue(test_value, test_parent_mock)
        self.assertEqual(idl_enum_value._value, test_value)
        self.assertEqual(idl_enum_value._verbose, True)

    def test_idl_enum_value_to_parse_blocks(self):
        """test for IDLEnumValue.parse_blocks(blocks=1)"""
        test_value = 123
        test_filepath = 'test_filepath'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_enum_value = enum.IDLEnumValue(test_value, test_parent_mock)
        # test
        idl_enum_value.parse_blocks([1], test_filepath)
        self.assertEqual(idl_enum_value._filepath, test_filepath)
        self.assertEqual(idl_enum_value._name, 1)

    @mock.patch('sys.stdout.write')
    def test_idl_enum_value_to_parse_blocks(self, sys_stdout_write):
        """test for IDLEnumValue.parse_blocks(blocks=2)"""
        test_value = 123
        test_filepath = 'test_filepath'
        test_blocks = [1, 2]
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_enum_value = enum.IDLEnumValue(test_value, test_parent_mock)
        # test
        idl_enum_value.parse_blocks(test_blocks, test_filepath)
        self.assertEqual(idl_enum_value._filepath, test_filepath)
        sys_out_calls = [
            call('Unkown Enum format %s\n' % test_blocks),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)

    def test_idl_enum_value_to_simple_dic(self):
        """test for IDLEnumValue.simple_dic"""
        test_value = 123
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_enum_value = enum.IDLEnumValue(test_value, test_parent_mock)
        # test
        ret = idl_enum_value.to_simple_dic()
        expected_dic = {idl_enum_value.name: test_value}
        self.assertEqual(ret, expected_dic)

    def test_idl_enum_value_to_dic(self):
        """test for IDLEnumValue.to_dic"""
        test_value = 123
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_enum_value = enum.IDLEnumValue(test_value, test_parent_mock)
        # test
        ret = idl_enum_value.to_dic()
        expected_dic = {'name': idl_enum_value.name,
                        'filepath': idl_enum_value.filepath,
                        'classname': idl_enum_value.classname,
                        'value': test_value}
        self.assertEqual(ret, expected_dic)

    def test_idl_enum_value_properties(self):
        """test for IDLEnumValue's properties"""
        test_value = 123
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_enum_value = enum.IDLEnumValue(test_value, test_parent_mock)
        # test
        self.assertEqual(idl_enum_value.value, test_value)

    def test_idl_enum_init(self):
        """test for IDLEnum.__init__"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        # test
        idl_enum = enum.IDLEnum(test_name, test_parent_mock)
        self.assertEqual(idl_enum._members, [])
        self.assertEqual(idl_enum._verbose, True)

    def test_idl_enum_to_simple_dic_case_true(self):
        """test for IDLEnum.to_simple_dic(True, True)"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_enum = enum.IDLEnum(test_name, test_parent_mock)
        # test
        ret = idl_enum.to_simple_dic(True, True)
        self.assertEqual(ret, 'enum %s' % idl_enum.full_path)

    def test_idl_enum_to_simple_dic_case_false(self):
        """test for IDLEnum.to_simple_dic(False, False)"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_enum = enum.IDLEnum(test_name, test_parent_mock)
        # test
        ret = idl_enum.to_simple_dic(False, False)
        expected_dic = {'enum %s' % test_name: []}
        self.assertEqual(ret, expected_dic)

    @mock.patch('sys.stdout.write')
    def test_idl_enum_parse_tokens_normal(self, sys_stdout_write):
        """test for IDLEnum.parse_tokens normal"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_enum = enum.IDLEnum(test_name, test_parent_mock)
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ test1 , test2 } ;']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_enum, '_parse_block') as parse_block_mock:
            idl_enum.parse_tokens(tokens, test_filepath)
            parse_block_calls = [
                call(['test1']),
                call(['test2']),
            ]
            parse_block_mock.assert_has_calls(parse_block_calls)
        sys_stdout_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    def test_idl_enum_parse_tokens_invalid_syntax(self, sys_stdout_write):
        """test for IDLEnum.parse_tokens invalid syntax"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_enum = enum.IDLEnum(test_name, test_parent_mock)
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        # test (not start with '{')
        token_line = ['test1 , test2 } ;']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_enum, '_parse_block') as parse_block_mock:
            with self.assertRaises(SyntaxError):
                idl_enum.parse_tokens(tokens, test_filepath)
            parse_block_mock.assert_not_called()
        sys_out_calls = [
            call('# Error. No kakko "{".\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        # test (only '{')
        token_line = ['{']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_enum, '_parse_block') as parse_block_mock:
            with self.assertRaises(SyntaxError):
                idl_enum.parse_tokens(tokens, test_filepath)
            parse_block_mock.assert_not_called()
        sys_out_calls = [
            call('# Error. No kokka "}".\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        # test (not end with ';')
        token_line = ['{ test1 , test2 }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_enum, '_parse_block') as parse_block_mock:
            with self.assertRaises(SyntaxError):
                idl_enum.parse_tokens(tokens, test_filepath)
            parse_block_mock.assert_called_once()
        sys_out_calls = [
            call('# Error. No semi-colon after "}".\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.enum.IDLEnumValue')
    def test_idl_enum_parse_block(self, idl_enum_value_mock):
        """test for IDLEnum._parse_block"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_enum = enum.IDLEnum(test_name, test_parent_mock)
        # test
        test_block = ['test1']
        idl_enum._counter = 1
        idl_enum._parse_block(test_block)

        parse_block_calls = [
            call(1, idl_enum),
            call().parse_blocks(test_block, idl_enum.filepath),
        ]
        idl_enum_value_mock.assert_has_calls(parse_block_calls)
        self.assertEqual(idl_enum._counter, 2)
        self.assertEqual(idl_enum._members, [idl_enum_value_mock()])

    def test_idl_enum_properties(self):
        """test for IDLEnum's properties"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_enum = enum.IDLEnum(test_name, test_parent_mock)
        # test
        self.assertEqual(idl_enum.members, idl_enum._members)
        self.assertEqual(idl_enum.full_path, test_parent+enum.sep+test_name)


if __name__ == '__main__':
    unittest.main()
