# test for wasanbon/core/plugins/admin/idl_plugin/idl_parser/interface.py

import unittest
from unittest import mock
from unittest.mock import Mock, call

from wasanbon.core.plugins.admin.idl_plugin.idl_parser import interface


class TestPlugin(unittest.TestCase):

    def test_idl_argument_init(self):
        """test for IDLArgument.__init__"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        # test
        idl_argument = interface.IDLArgument(test_parent_mock)
        self.assertEqual(idl_argument._verbose, True)
        self.assertEqual(idl_argument._dir, 'in')
        self.assertEqual(idl_argument._type, None)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_argument_to_parse_blocks(self, idl_type_mock):
        """test for IDLArgument.parse_blocks"""
        test_filepath = 'test_filepath'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_argument = interface.IDLArgument(test_parent_mock)
        # test
        test_block = ['inout', 2]
        mock_ret = ['test1', 'test2']
        with mock.patch.object(idl_argument, '_name_and_type', return_value=mock_ret) as name_and_type_mock:
            idl_argument.parse_blocks(test_block, test_filepath)
            name_and_type_mock.assert_called_with(test_block)
        self.assertEqual(idl_argument._filepath, test_filepath)
        self.assertEqual(idl_argument._name, mock_ret[0])
        self.assertEqual(idl_argument._type, idl_type_mock())

    def test_idl_argument_to_simple_dic(self):
        """test for IDLArgument.simple_dic"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_argument = interface.IDLArgument(test_parent_mock)
        # test
        ret = idl_argument.to_simple_dic()
        expected_dic = '%s %s %s' % (
            idl_argument.direction, idl_argument.type, idl_argument.name)
        self.assertEqual(ret, expected_dic)

    def test_idl_argument_to_dic(self):
        """test for IDLArgument.to_dic"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_argument = interface.IDLArgument(test_parent_mock)
        # test
        ret = idl_argument.to_dic()
        expected_dic = {'name': idl_argument.name,
                        'classname': idl_argument.classname,
                        'type': str(idl_argument.type),
                        'direction': idl_argument.direction,
                        'filepath': idl_argument.filepath}
        self.assertEqual(ret, expected_dic)

    def test_idl_argument_properties(self):
        """test for IDLArgument's properties"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_argument = interface.IDLArgument(test_parent_mock)
        # test
        self.assertEqual(idl_argument.direction, idl_argument._dir)
        self.assertEqual(idl_argument.type, idl_argument._type)

    def test_idl_method_init(self):
        """test for IDLMethod.__init__"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        # test
        idl_method = interface.IDLMethod(test_parent_mock)
        self.assertEqual(idl_method._verbose, True)
        self.assertEqual(idl_method._returns, None)
        self.assertEqual(idl_method._arguments, [])

    def test_idl_method_to_simple_dic(self):
        """test for IDLMethod.to_simple_dic"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_method = interface.IDLMethod(test_parent_mock)
        # test
        ret = idl_method.to_simple_dic()
        expected_dic = {idl_method.name: {
            'returns': str(idl_method.returns),
            'params': []}}
        self.assertEqual(ret, expected_dic)

    def test_idl_method_to_dic(self):
        """test for IDLMethod.to_dic"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_method = interface.IDLMethod(test_parent_mock)
        # test
        ret = idl_method.to_dic()
        expected_dic = {'name': idl_method.name,
                        'filepath': idl_method.filepath,
                        'classname': idl_method.classname,
                        'returns': str(idl_method._returns),
                        'arguments': []}
        self.assertEqual(ret, expected_dic)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.interface.IDLArgument')
    def test_idl_method_parse_blocks_normal(self, idl_argument_mock, idl_type_mock):
        """test for IDLMethod.parse_blocks normal"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_method = interface.IDLMethod(test_parent_mock)
        # test
        test_blocks = ['oneway', '1', '2', '(', 'arg1', 'arg2', ')']
        test_filepath = 'test_filepath'
        idl_method.parse_blocks(test_blocks, test_filepath)
        idl_type_calls = [
            call(test_blocks[0], idl_method),
        ]
        idl_argument_calls = [
            call(idl_method),
            call(idl_method).parse_blocks(
                [test_blocks[3], test_blocks[4]], idl_method.filepath),
        ]
        idl_type_mock.assert_has_calls(idl_type_calls)
        idl_argument_mock.assert_has_calls(idl_argument_calls)
        self.assertEqual(idl_method._filepath, test_filepath)
        self.assertEqual(idl_method._oneway, True)
        self.assertEqual(idl_method._returns, idl_type_mock())
        self.assertEqual(idl_method._name, test_blocks[1])
        self.assertEqual(idl_method._arguments, [idl_argument_mock()])

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.interface.IDLArgument')
    def test_idl_method_parse_blocks_no_end(self, idl_argument_mock, idl_type_mock):
        """test for IDLMethod.parse_blocks end with '('"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_method = interface.IDLMethod(test_parent_mock)
        # test
        test_blocks = ['0', '1', '(']
        test_filepath = 'test_filepath'
        idl_method.parse_blocks(test_blocks, test_filepath)
        idl_type_calls = [
            call(test_blocks[0], idl_method),
        ]
        idl_type_mock.assert_has_calls(idl_type_calls)
        idl_argument_mock.assert_not_called()
        self.assertEqual(idl_method._filepath, test_filepath)
        self.assertEqual(idl_method._oneway, False)
        self.assertEqual(idl_method._returns, idl_type_mock())
        self.assertEqual(idl_method._name, test_blocks[1])
        self.assertEqual(idl_method._arguments, [])

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.interface.IDLArgument')
    def test_idl_method_parse_blocks_no_args(self, idl_argument_mock, idl_type_mock):
        """test for IDLMethod.parse_blocks no arguments"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_method = interface.IDLMethod(test_parent_mock)
        # test
        test_blocks = ['0', '1', '(', ')']
        test_filepath = 'test_filepath'
        idl_method.parse_blocks(test_blocks, test_filepath)
        idl_type_calls = [
            call(test_blocks[0], idl_method),
        ]
        idl_type_mock.assert_has_calls(idl_type_calls)
        idl_argument_mock.assert_not_called()
        self.assertEqual(idl_method._filepath, test_filepath)
        self.assertEqual(idl_method._oneway, False)
        self.assertEqual(idl_method._returns, idl_type_mock())
        self.assertEqual(idl_method._name, test_blocks[1])
        self.assertEqual(idl_method._arguments, [])

    def test_idl_method_properties(self):
        """test for IDLMethod's properties"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_method = interface.IDLMethod(test_parent_mock)
        # test
        self.assertEqual(idl_method.returns, idl_method._returns)
        self.assertEqual(idl_method.arguments, idl_method._arguments)

    def test_idl_method_forEachArgument(self):
        """test for IDLMethod.forEachArgument"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_method = interface.IDLMethod(test_parent_mock)
        # test
        mock_func = Mock()
        test_args = ['test1', 'test2']
        idl_method._arguments = test_args
        idl_method.forEachArgument(mock_func)
        calls = [call(test_args[0]), call(test_args[1])]
        mock_func.assert_has_calls(calls)

    def test_idl_interface_init(self):
        """test for IDLInterface.__init__"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        # test
        idl_interface = interface.IDLInterface(test_name, test_parent_mock)
        self.assertEqual(idl_interface._verbose, True)
        self.assertEqual(idl_interface._methods, [])

    def test_idl_interface_to_simple_dic_case_true(self):
        """test for IDLInterface.to_simple_dic(True)"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_interface = interface.IDLInterface(test_name, test_parent_mock)
        # test
        ret = idl_interface.to_simple_dic(True)
        self.assertEqual(ret, 'interface %s' % test_name)

    def test_idl_interface_to_simple_dic_case_false(self):
        """test for IDLInterface.to_simple_dic(False)"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_interface = interface.IDLInterface(test_name, test_parent_mock)
        # test
        ret = idl_interface.to_simple_dic(False)
        expected_dic = {'interface ' + test_name: []}
        self.assertEqual(ret, expected_dic)

    def test_idl_interface_to_dic(self):
        """test for IDLInterface.to_dic"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_interface = interface.IDLInterface(test_name, test_parent_mock)
        # test
        ret = idl_interface.to_dic()
        expected_dic = {'name': idl_interface.name,
                        'filepath': idl_interface.filepath,
                        'classname': idl_interface.classname,
                        'methods': []}
        self.assertEqual(ret, expected_dic)

    @mock.patch('sys.stdout.write')
    def test_idl_interface_parse_tokens_normal(self, sys_stdout_write):
        """test for IDLInterface.parse_tokens normal"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_interface = interface.IDLInterface(test_name, test_parent_mock)
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ test1 ; test2 ; } ;']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_interface, '_parse_block') as parse_block_mock:
            idl_interface.parse_tokens(tokens, test_filepath)
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
        idl_interface = interface.IDLInterface(test_name, test_parent_mock)
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        # test (not start with '{')
        token_line = ['test1 ; test2 ; } ;']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_interface, '_parse_block') as parse_block_mock:
            with self.assertRaises(SyntaxError):
                idl_interface.parse_tokens(tokens, test_filepath)
            parse_block_mock.assert_not_called()
        sys_out_calls = [
            call('# Error. No kakko "{".\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        # test (only '{')
        token_line = ['{']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_interface, '_parse_block') as parse_block_mock:
            with self.assertRaises(SyntaxError):
                idl_interface.parse_tokens(tokens, test_filepath)
            parse_block_mock.assert_not_called()
        sys_out_calls = [
            call('# Error. No kokka "}".\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        # test (not end with ';')
        token_line = ['{ test1 ; }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_interface, '_parse_block') as parse_block_mock:
            with self.assertRaises(SyntaxError):
                idl_interface.parse_tokens(tokens, test_filepath)
            parse_block_mock.assert_called_once()
        sys_out_calls = [
            call('# Error. No semi-colon after "}".\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)

    def test_idl_interface_post_process(self):
        """test for IDLInterface._post_process"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_interface = interface.IDLInterface(test_name, test_parent_mock)
        # test
        with mock.patch.object(idl_interface, 'forEachMethod') as forEachMethod_mock:
            idl_interface._post_process()
            forEachMethod_mock.assert_called_once()

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.interface.IDLMethod')
    def test_idl_interface_parse_block(self, idl_method_mock):
        """test for IDLInterface._parse_block"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_interface = interface.IDLInterface(test_name, test_parent_mock)
        # test
        test_block = ['test1']
        idl_interface._parse_block(test_block)
        idl_method_calls = [
            call(idl_interface),
            call().parse_blocks(test_block, idl_interface.filepath)
        ]
        idl_method_mock.assert_has_calls(idl_method_calls)
        self.assertEqual(idl_interface._methods, [idl_method_mock()])

    def test_idl_interface_forEachMethod(self):
        """test for IDLInterface.forEachMethod"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_interface = interface.IDLInterface(test_name, test_parent_mock)
        # test
        mock_func = Mock()
        test_args = ['test1', 'test2']
        idl_interface._methods = test_args
        idl_interface.forEachMethod(mock_func)
        calls = [call(test_args[0]), call(test_args[1])]
        mock_func.assert_has_calls(calls)

    def test_idl_interface_properties(self):
        """test for IDLInterface's properties"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_interface = interface.IDLInterface(test_name, test_parent_mock)
        # test
        self.assertEqual(idl_interface.full_path,
                         test_parent + interface.sep + test_name)
        self.assertEqual(idl_interface.methods, idl_interface._methods)


if __name__ == '__main__':
    unittest.main()
