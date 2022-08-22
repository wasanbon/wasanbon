# test for wasanbon/core/plugins/admin/idl_plugin/idl_parser/struct.py

import unittest
from unittest import mock
from unittest.mock import Mock, call

from wasanbon.core.plugins.admin.idl_plugin.idl_parser import struct


class TestPlugin(unittest.TestCase):

    def test_idl_value_init(self):
        """test for IDLValue.__init__"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        # test
        idl_value = struct.IDLValue(test_parent_mock)
        self.assertEqual(idl_value._verbose, True)
        self.assertEqual(idl_value._type, None)
        self.assertEqual(idl_value.sep, '::')

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_value_to_parse_blocks(self, idl_type_mock):
        """test for IDLValue.parse_blocks"""
        test_filepath = 'test_filepath'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_value = struct.IDLValue(test_parent_mock)
        # test
        test_block = [1, 2]
        mock_ret = ['a[', '[']
        with mock.patch.object(idl_value, '_name_and_type', return_value=mock_ret) as name_and_type_mock:
            idl_value.parse_blocks(test_block, test_filepath)
            name_and_type_mock.assert_called_with(test_block)
        self.assertEqual(idl_value._filepath, test_filepath)
        self.assertEqual(idl_value._name, 'a')
        self.assertEqual(idl_value._type, idl_type_mock())

    def test_idl_value_to_simple_dic(self):
        """test for IDLValue.simple_dic"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_value = struct.IDLValue(test_parent_mock)
        # test(primitive)
        type_mock = Mock(spec=['is_primitive'])
        type_mock.is_primitive = True
        idl_value._type = type_mock
        ret = idl_value.to_simple_dic(True)
        self.assertEqual(ret, str(idl_value.type) + ' ' + idl_value.name)
        # test(not primitive but enum)
        obj_mock = Mock(spec=['is_enum'])
        obj_mock.is_enum = True
        type_mock = Mock(spec=['is_primitive', 'obj'])
        type_mock.is_primitive = False
        type_mock.obj = obj_mock
        idl_value._type = type_mock
        ret = idl_value.to_simple_dic(True)
        self.assertEqual(ret, 'enum' + ' ' + idl_value.name)
        # test(nor primitive, enum)
        test_dic = 'test_dic'
        obj_mock = Mock(spec=['is_enum', 'to_simple_dic'])
        obj_mock.is_enum = False
        obj_mock.to_simple_dic.return_value = test_dic
        type_mock = Mock(spec=['is_primitive', 'obj'])
        type_mock.is_primitive = False
        type_mock.obj = obj_mock
        idl_value._type = type_mock
        ret = idl_value.to_simple_dic(True)
        expected_dic = {str(type_mock) + ' ' + idl_value.name: test_dic}
        self.assertEqual(ret, expected_dic)
        # test(not recursive)
        ret = idl_value.to_simple_dic(False)
        expected_dic = {idl_value.name: str(idl_value.type)}
        self.assertEqual(ret, expected_dic)

    def test_idl_value_to_dic(self):
        """test for IDLValue.to_dic"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_value = struct.IDLValue(test_parent_mock)
        # test
        ret = idl_value.to_dic()
        expected_dic = {'name': idl_value.name,
                        'filepath': idl_value.filepath,
                        'classname': idl_value.classname,
                        'type': str(idl_value.type)}
        self.assertEqual(ret, expected_dic)

    def test_idl_value_properties(self):
        """test for IDLValue's properties"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_value = struct.IDLValue(test_parent_mock)
        # test
        self.assertEqual(idl_value.full_path, test_parent +
                         idl_value.sep + idl_value.name)
        self.assertEqual(idl_value.type, idl_value._type)

    def test_idl_struct_init(self):
        """test for IDLStruct.__init__"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        # test
        idl_struct = struct.IDLStruct(test_name, test_parent_mock)
        self.assertEqual(idl_struct._verbose, True)
        self.assertEqual(idl_struct._members, [])
        self.assertEqual(idl_struct.sep, '::')

    def test_idl_struct_to_simple_dic(self):
        """test for IDLStruct.to_simple_dic"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_struct = struct.IDLStruct(test_name, test_parent_mock)
        # test(quiet)
        ret = idl_struct.to_simple_dic(True, False)
        self.assertEqual(ret, 'struct %s' % test_name)
        # test(not quiet)
        ret = idl_struct.to_simple_dic(False, False)
        expected_dic = {'struct %s' % test_name: []}
        self.assertEqual(ret, expected_dic)
        # test(member only)
        ret = idl_struct.to_simple_dic(False, False, member_only=True)
        self.assertEqual(ret, [])

    def test_idl_struct_to_dic(self):
        """test for IDLStruct.to_dic"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_struct = struct.IDLStruct(test_name, test_parent_mock)
        # test
        ret = idl_struct.to_dic()
        expected_dic = {'name': test_name,
                        'classname': idl_struct.classname,
                        'members': []}
        self.assertEqual(ret, expected_dic)

    @mock.patch('sys.stdout.write')
    def test_idl_interface_parse_tokens_normal(self, sys_stdout_write):
        """test for IDLInterface.parse_tokens normal"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_struct = struct.IDLStruct(test_name, test_parent_mock)
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ test1 ; test2 ; } ;']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_struct, '_parse_block') as parse_block_mock:
            idl_struct.parse_tokens(tokens, test_filepath)
            parse_block_calls = [
                call(['test1']),
                call(['test2']),
            ]
            parse_block_mock.assert_has_calls(parse_block_calls)
        sys_stdout_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    def test_idl_interface_parse_tokens_invalid_syntax(self, sys_stdout_write):
        """test for IDLInterface.parse_tokens invalid syntax"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_struct = struct.IDLStruct(test_name, test_parent_mock)
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        # test (not start with '{')
        token_line = ['test1 ; test2 ; } ;']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_struct, '_parse_block') as parse_block_mock:
            with self.assertRaises(SyntaxError):
                idl_struct.parse_tokens(tokens, test_filepath)
            parse_block_mock.assert_not_called()
        sys_out_calls = [
            call('# Error. No kakko "{".\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        # test (only '{')
        token_line = ['{']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_struct, '_parse_block') as parse_block_mock:
            with self.assertRaises(SyntaxError):
                idl_struct.parse_tokens(tokens, test_filepath)
            parse_block_mock.assert_not_called()
        sys_out_calls = [
            call('# Error. No kokka "}".\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        # test (not end with ';')
        token_line = ['{ test1 ; }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_struct, '_parse_block') as parse_block_mock:
            with self.assertRaises(SyntaxError):
                idl_struct.parse_tokens(tokens, test_filepath)
            parse_block_mock.assert_called_once()
        sys_out_calls = [
            call('# Error. No semi-colon after "}".\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.struct.IDLValue')
    def test_idl_struct_parse_blocks_normal(self, idl_value_mock):
        """test for IDLStruct._parse_block normal"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_struct = struct.IDLStruct(test_name, test_parent_mock)
        # test
        test_blocks = ['1', '2']
        idl_struct._parse_block(test_blocks)
        idl_value_calls = [
            call(idl_struct),
            call(idl_struct).parse_blocks(test_blocks, idl_struct.filepath)
        ]
        idl_value_mock.assert_has_calls(idl_value_calls)
        self.assertEqual(idl_struct._members, [idl_value_mock()])

    def test_idl_struct_properties(self):
        """test for IDLStruct's properties"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_struct = struct.IDLStruct(test_name, test_parent_mock)
        # test
        self.assertEqual(idl_struct.full_path, test_parent +
                         idl_struct.sep + test_name)
        self.assertEqual(idl_struct.members, idl_struct._members)

    def test_idl_struct_forEachMember(self):
        """test for IDLStruct.forEachMember"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_struct = struct.IDLStruct(test_name, test_parent_mock)
        # test
        mock_func = Mock()
        test_args = ['test1', 'test2']
        idl_struct._members = test_args
        idl_struct.forEachMember(mock_func)
        calls = [call(test_args[0]), call(test_args[1])]
        mock_func.assert_has_calls(calls)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.struct.IDLStruct.forEachMember')
    def test_idl_struct_post_process(self, each_member_mock):
        """test for IDLStruct._post_process"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_struct = struct.IDLStruct(test_name, test_parent_mock)
        # test
        idl_struct._post_process()
        each_member_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
