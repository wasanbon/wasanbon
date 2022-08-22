# test for wasanbon/core/plugins/admin/idl_plugin/idl_parser/.py

import unittest
from unittest import mock
from unittest.mock import Mock, call

from wasanbon.core.plugins.admin.idl_plugin.idl_parser import module


class TestPlugin(unittest.TestCase):

    def test_idl_module_init(self):
        """test for IDLModule.__init__"""
        test_name = None
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        # test
        idl_module = module.IDLModule(test_name, test_parent_mock)
        self.assertEqual(idl_module._verbose, False)
        self.assertEqual(idl_module._name, module.global_namespace)
        self.assertEqual(idl_module._interfaces, [])
        self.assertEqual(idl_module._typedefs, [])
        self.assertEqual(idl_module._structs, [])
        self.assertEqual(idl_module._enums, [])
        self.assertEqual(idl_module._consts, [])
        self.assertEqual(idl_module._modules, [])

    def test_idl_module_to_simple_dic(self):
        """test for IDLModule.to_simple_dic"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        ret = idl_module.to_simple_dic(True)
        expected_dic = {'module %s' % test_name: []}
        self.assertEqual(ret, expected_dic)

    def test_idl_module_to_dic(self):
        """test for IDLModule.to_dic"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        ret = idl_module.to_dic()
        expected_dic = {'name': test_name,
                        'filepath': idl_module.filepath,
                        'classname': idl_module.classname,
                        'interfaces': [],
                        'typedefs': [],
                        'structs': [],
                        'enums': [],
                        'modules': [],
                        'consts': []}
        self.assertEqual(ret, expected_dic)

    @mock.patch('sys.stdout.write')
    def test_idl_module_parse_tokens_normal_module(self, sys_stdout_write):
        """test for IDLModule.parse_tokens normal token: module"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ module mod_name1 { } }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_module, 'module_by_name', return_value=None) as module_by_name_mock:
            idl_module.parse_tokens(tokens, test_filepath)
            module_by_name_calls = [
                call('mod_name1'),
            ]
            module_by_name_mock.assert_has_calls(module_by_name_calls)
        self.assertIsInstance(idl_module._modules[0], module.IDLModule)
        sys_stdout_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.typedef.IDLTypedef')
    def test_idl_module_parse_tokens_normal_typedef(self, idl_typedef_mock, sys_stdout_write):
        """test for IDLModule.parse_tokens normal token: typedef"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ typedef t1 ; }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        idl_module.parse_tokens(tokens, test_filepath)
        self.assertEqual(idl_module._typedefs, [idl_typedef_mock()])
        idl_typedef_calls = [
            call(idl_module),
            call().parse_blocks(['t1'], filepath=test_filepath)
        ]
        idl_typedef_mock.assert_has_calls(idl_typedef_calls)
        sys_stdout_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.typedef.IDLTypedef')
    def test_idl_module_parse_tokens_invalid_typedef(self, idl_typedef_mock, sys_stdout_write):
        """test for IDLModule.parse_tokens invalid token: typedef"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ typedef ']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with self.assertRaises(SyntaxError):
            idl_module.parse_tokens(tokens, test_filepath)
        self.assertEqual(idl_module._typedefs, [])
        idl_typedef_mock.assert_not_called()
        sys_stdout_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.struct.IDLStruct')
    def test_idl_module_parse_tokens_normal_struct(self, idl_struct_mock, sys_stdout_write):
        """test for IDLModule.parse_tokens normal token: struct"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ struct s1 ; }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_module, 'struct_by_name', return_value=False) as struct_by_name_mock:
            idl_module.parse_tokens(tokens, test_filepath)
            struct_by_name_calls = [
                call('s1'),
            ]
            struct_by_name_mock.assert_has_calls(struct_by_name_calls)
        self.assertEqual(idl_module._structs, [idl_struct_mock()])
        idl_struct_calls = [
            call('s1', idl_module),
            call().parse_tokens(tokens, filepath=test_filepath)
        ]
        idl_struct_mock.assert_has_calls(idl_struct_calls)
        sys_stdout_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.struct.IDLStruct')
    def test_idl_module_parse_tokens_invalid_struct(self, idl_struct_mock, sys_stdout_write):
        """test for IDLModule.parse_tokens invalid token: struct"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        idl_module._verbose = True
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ struct s1 ; }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_module, 'struct_by_name', return_value=True) as struct_by_name_mock:
            idl_module.parse_tokens(tokens, test_filepath)
            struct_by_name_calls = [
                call('s1'),
            ]
            struct_by_name_mock.assert_has_calls(struct_by_name_calls)
        idl_struct_calls = [
            call('s1', idl_module),
            call().parse_tokens(tokens, filepath=test_filepath)
        ]
        idl_struct_mock.assert_has_calls(idl_struct_calls)
        sys_calls = [call('# Error. Same Struct Defined (%s)\n' % 's1')]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.interface.IDLInterface')
    def test_idl_module_parse_tokens_normal_interface(self, idl_interface_mock, sys_stdout_write):
        """test for IDLModule.parse_tokens normal token: interface"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ interface i1 ; }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_module, 'interface_by_name', return_value=False) as by_name_mock:
            idl_module.parse_tokens(tokens, test_filepath)
            by_name_calls = [
                call('i1'),
            ]
            by_name_mock.assert_has_calls(by_name_calls)
        self.assertEqual(idl_module._interfaces, [idl_interface_mock()])
        idl_struct_calls = [
            call('i1', idl_module),
            call().parse_tokens(tokens, filepath=test_filepath)
        ]
        idl_interface_mock.assert_has_calls(idl_struct_calls)
        sys_stdout_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.interface.IDLInterface')
    def test_idl_module_parse_tokens_invalid_interface(self, idl_interface_mock, sys_stdout_write):
        """test for IDLModule.parse_tokens invalid token: interface"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        idl_module._verbose = True
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ interface i1 ; }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_module, 'interface_by_name', return_value=True) as by_name_mock:
            idl_module.parse_tokens(tokens, test_filepath)
            by_name_calls = [
                call('i1'),
            ]
            by_name_mock.assert_has_calls(by_name_calls)
        self.assertEqual(idl_module._interfaces, [])
        idl_calls = [
            call('i1', idl_module),
            call().parse_tokens(tokens, filepath=test_filepath)
        ]
        idl_interface_mock.assert_has_calls(idl_calls)
        sys_calls = [call('# Error. Same Interface Defined (%s)\n' % 'i1')]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.enum.IDLEnum')
    def test_idl_module_parse_tokens_normal_enum(self, idl_enum_mock, sys_stdout_write):
        """test for IDLModule.parse_tokens normal token: enum"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ enum e1 ; }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_module, 'enum_by_name', return_value=False) as by_name_mock:
            idl_module.parse_tokens(tokens, test_filepath)
            by_name_calls = [
                call('e1'),
            ]
            by_name_mock.assert_has_calls(by_name_calls)
        self.assertEqual(idl_module._enums, [idl_enum_mock()])
        idl_calls = [
            call('e1', idl_module),
            call().parse_tokens(tokens, test_filepath)
        ]
        idl_enum_mock.assert_has_calls(idl_calls)
        sys_stdout_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.enum.IDLEnum')
    def test_idl_module_parse_tokens_invalid_enum(self, idl_enum_mock, sys_stdout_write):
        """test for IDLModule.parse_tokens invalid token: enum"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        idl_module._verbose = True
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ enum e1 ; }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_module, 'enum_by_name', return_value=True) as by_name_mock:
            idl_module.parse_tokens(tokens, test_filepath)
            by_name_calls = [
                call('e1'),
            ]
            by_name_mock.assert_has_calls(by_name_calls)
        self.assertEqual(idl_module._enums, [])
        idl_calls = [
            call('e1', idl_module),
            call().parse_tokens(tokens, test_filepath)
        ]
        idl_enum_mock.assert_has_calls(idl_calls)
        sys_calls = [call('# Error. Same Enum Defined (%s)\n' % 'e1')]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.const.IDLConst')
    def test_idl_module_parse_tokens_normal_const(self, idl_const_mock, sys_stdout_write):
        """test for IDLModule.parse_tokens normal token: const"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ const c1 c2 c3 c4 ; }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_module, 'const_by_name', return_value=False) as by_name_mock:
            idl_module.parse_tokens(tokens, test_filepath)
            by_name_calls = [
                call('c2'),
            ]
            by_name_mock.assert_has_calls(by_name_calls)
        self.assertEqual(idl_module._consts, [idl_const_mock()])
        idl_calls = [
            call('c2', 'c1', 'c4', idl_module, filepath=test_filepath)
        ]
        idl_const_mock.assert_has_calls(idl_calls)
        sys_stdout_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.const.IDLConst')
    def test_idl_module_parse_tokens_invalid_const(self, idl_const_mock, sys_stdout_write):
        """test for IDLModule.parse_tokens invalid token: const"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        idl_module._verbose = True
        # test
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        token_line = ['{ const c1 c2 c3 c4 ; }']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with mock.patch.object(idl_module, 'const_by_name', return_value=True) as by_name_mock:
            idl_module.parse_tokens(tokens, test_filepath)
            by_name_calls = [
                call('c2'),
            ]
            by_name_mock.assert_has_calls(by_name_calls)
        self.assertEqual(idl_module._consts, [])
        idl_calls = [
            call('c2', 'c1', 'c4', idl_module, filepath=test_filepath)
        ]
        idl_const_mock.assert_has_calls(idl_calls)
        sys_calls = [call('# Error. Same Const Defined (%s)\n' % 'c2')]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    def test_idl_module_parse_tokens_invalid_syntax(self, sys_stdout_write):
        """test for IDLModule.parse_tokens invalid syntax"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        idl_module._verbose = True
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer
        # test (not start with '{')
        token_line = ['test1 ; test2 ; } ;']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with self.assertRaises(SyntaxError):
            idl_module.parse_tokens(tokens, test_filepath)
        sys_out_calls = [
            call('# Error. No kakko "{".\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        # test (only '{')
        token_line = ['{']
        tokens = token_buffer.TokenBuffer(token_line)
        test_filepath = 'test_filepath'
        with self.assertRaises(SyntaxError):
            idl_module.parse_tokens(tokens, test_filepath)
        sys_out_calls = [
            call('# Error. No kokka "}".\n'),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)

    def test_idl_module_module_by_name(self):
        """test for IDLModule.module_by_name"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # mock for module

        class ModuleMock:
            def __init__(self, name) -> None:
                self.name = name
        test_modules = [ModuleMock('a'), ModuleMock('b'), ModuleMock('c')]
        idl_module._modules = test_modules
        # test (get name)
        test_module_name = 'c'
        ret = idl_module.module_by_name(test_module_name)
        self.assertEqual(ret, test_modules[2])
        # test (get None)
        test_module_name = 'd'
        ret = idl_module.module_by_name(test_module_name)
        self.assertEqual(ret, None)

    def test_idl_module_forEachModule(self):
        """test for IDLModule.forEachModule"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        mock_func = Mock()
        test_args = ['test1', 'test2']
        idl_module._modules = test_args
        idl_module.forEachModule(mock_func)
        calls = [call(test_args[0]), call(test_args[1])]
        mock_func.assert_has_calls(calls)

    def test_idl_module_interface_by_name(self):
        """test for IDLModule.interface_by_name"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # mock for module

        class ModuleMock:
            def __init__(self, name) -> None:
                self.name = name
        test_modules = [ModuleMock('a'), ModuleMock('b'), ModuleMock('c')]
        idl_module._interfaces = test_modules
        # test (get name)
        test_module_name = 'c'
        ret = idl_module.interface_by_name(test_module_name)
        self.assertEqual(ret, test_modules[2])
        # test (get None)
        test_module_name = 'd'
        ret = idl_module.interface_by_name(test_module_name)
        self.assertEqual(ret, None)

    def test_idl_module_forEachInterface(self):
        """test for IDLModule.forEachInterface"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        mock_func = Mock()
        test_args = ['test1', 'test2']
        idl_module._interfaces = test_args
        idl_module.forEachInterface(mock_func)
        calls = [call(test_args[0]), call(test_args[1])]
        mock_func.assert_has_calls(calls)

    def test_idl_module_enum_by_name(self):
        """test for IDLModule.enum_by_name"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # mock for module

        class ModuleMock:
            def __init__(self, name) -> None:
                self.name = name
        test_modules = [ModuleMock('a'), ModuleMock('b'), ModuleMock('c')]
        idl_module._enums = test_modules
        # test (get name)
        test_module_name = 'c'
        ret = idl_module.enum_by_name(test_module_name)
        self.assertEqual(ret, test_modules[2])
        # test (get None)
        test_module_name = 'd'
        ret = idl_module.enum_by_name(test_module_name)
        self.assertEqual(ret, None)

    def test_idl_module_forEachEnum(self):
        """test for IDLModule.forEachEnum"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        mock_func = Mock()
        test_args = ['test1', 'test2']
        idl_module._enums = test_args
        idl_module.forEachEnum(mock_func)
        calls = [call(test_args[0]), call(test_args[1])]
        mock_func.assert_has_calls(calls)

    def test_idl_module_const_by_name(self):
        """test for IDLModule.const_by_name"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # mock for module

        class ModuleMock:
            def __init__(self, name) -> None:
                self.name = name
        test_modules = [ModuleMock('a'), ModuleMock('b'), ModuleMock('c')]
        idl_module._consts = test_modules
        # test (get name)
        test_module_name = 'c'
        ret = idl_module.const_by_name(test_module_name)
        self.assertEqual(ret, test_modules[2])
        # test (get None)
        test_module_name = 'd'
        ret = idl_module.const_by_name(test_module_name)
        self.assertEqual(ret, None)

    def test_idl_module_forEachConst(self):
        """test for IDLModule.forEachConst"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        mock_func = Mock()
        test_args = ['test1', 'test2']
        idl_module._consts = test_args
        idl_module.forEachConst(mock_func)
        calls = [call(test_args[0]), call(test_args[1])]
        mock_func.assert_has_calls(calls)

    def test_idl_module_typedef_by_name(self):
        """test for IDLModule.typedef_by_name"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # mock for module

        class ModuleMock:
            def __init__(self, name) -> None:
                self.name = name
        test_modules = [ModuleMock('a'), ModuleMock('b'), ModuleMock('c')]
        idl_module._typedefs = test_modules
        # test (get name)
        test_module_name = 'c'
        ret = idl_module.typedef_by_name(test_module_name)
        self.assertEqual(ret, test_modules[2])
        # test (get None)
        test_module_name = 'd'
        ret = idl_module.typedef_by_name(test_module_name)
        self.assertEqual(ret, None)

    def test_idl_module_forEachTypedef(self):
        """test for IDLModule.forEachTypedef"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        mock_func = Mock()
        test_args = ['test1', 'test2']
        idl_module._typedefs = test_args
        idl_module.forEachTypedef(mock_func)
        calls = [call(test_args[0]), call(test_args[1])]
        mock_func.assert_has_calls(calls)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.is_primitive', return_value=True)
    def test_idl_module_find_types_primitive(self, _, idl_type_mock):
        """test for IDLModule.find_types primitive"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        test_full_typename = 'test_full_typename'
        ret = idl_module.find_types(test_full_typename)
        self.assertEqual(ret, [idl_type_mock()])

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.module.IDLModule.forEachModule')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.module.IDLModule.forEachStruct')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.module.IDLModule.forEachTypedef')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.module.IDLModule.forEachEnum')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.module.IDLModule.forEachInterface')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.is_primitive', return_value=False)
    def test_idl_module_find_types_not_primitive(self, _, each_interface_mock, each_enum_mock, each_typedef_mock, each_struct_mock, each_module_mock):
        """test for IDLModule.find_types not primitive"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        # test
        test_full_typename = 'test_full_typename'
        ret = idl_module.find_types(test_full_typename)
        each_module_mock.called_once()
        each_struct_mock.called_once()
        each_typedef_mock.called_once()
        each_enum_mock.called_once()
        each_interface_mock.called_once()
        self.assertEqual(ret, [])

    def test_idl_module_properties(self):
        """test for IDLModule's properties"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        # test (full_path length > 0)
        idl_module = module.IDLModule(test_name, test_parent_mock)
        self.assertEqual(idl_module.is_global, test_name ==
                         module.global_namespace)
        self.assertEqual(idl_module.interfaces, idl_module._interfaces)
        self.assertEqual(idl_module.structs, idl_module._structs)
        self.assertEqual(idl_module.enums, idl_module._enums)
        self.assertEqual(idl_module.consts, idl_module._consts)
        self.assertEqual(idl_module.typedefs, idl_module._typedefs)
        self.assertEqual(idl_module.full_path, test_parent +
                         module.sep + test_name)
        # test(full_path is None)
        test_parent = None
        idl_module = module.IDLModule(test_name, test_parent)
        self.assertEqual(idl_module.full_path, '')
        # test(full_path length == 0)
        test_parent = ''
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_module = module.IDLModule(test_name, test_parent_mock)
        self.assertEqual(idl_module.full_path, test_name)


if __name__ == '__main__':
    unittest.main()
