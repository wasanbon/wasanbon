# test for wasanbon/core/plugins/admin/idlcompiler_plugin/dart_converter.py

import unittest
from unittest import mock
from unittest.mock import Mock, call

from wasanbon.core.plugins.admin.idlcompiler_plugin import dart_converter


class TestPlugin(unittest.TestCase):

    @mock.patch('builtins.open')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter.generate_class_dart')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._apply_post_process_dart')
    def test_generate_converter(self, post_process_mock, generate_mock, os_mkdir_mock, os_isdir_mock, open_mock):
        """test for generate_converter"""
        # make parser
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import parser
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import module
        from wasanbon.core.plugins.admin.idl_plugin.idl_parser import struct
        test_parser = parser.IDLParser()
        test_module_name = 'm1'
        module_mock = module.IDLModule()
        module_mock._name = test_module_name
        test_struct_name = 's1'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = 'test_parent'
        struct_mock = struct.IDLStruct(test_struct_name, test_parent_mock)
        module_mock._structs = [struct_mock]
        test_parser._global_module._modules = [module_mock]
        # mock path settings
        generate_mock.return_value = 'test1'
        post_process_mock.return_value = 'test2'
        file_mock = Mock()
        open_mock.return_value = file_mock
        os_isdir_mock.return_value = False
        # test
        dart_converter.generate_converter(test_parser)
        generate_mock.assert_called_once_with(
            test_parser.global_module, struct_mock.full_path)
        post_process_mock.assert_called_once_with('test1\n')
        os_calls = [
            call('dart'),
            call('dart/lib'),
        ]
        os_isdir_mock.assert_has_calls(os_calls)
        os_mkdir_mock.assert_has_calls(os_calls)
        comment_code = """/// file: %s
/// generator: wasanbon
///


""" % (test_module_name + '.dart')
        open_calls = [
            call('dart/lib/%s.dart' % (test_module_name), 'w'),
            call().write(comment_code),
            call().write('test2'),
            call().close()
        ]
        open_mock.assert_has_calls(open_calls)

    def test_type_filter(self):
        """test for _type_filter"""
        # test (string)
        test_type = 'string'
        test_global_module = 'test_gm'
        ret = dart_converter._type_filter(test_type, test_global_module)
        self.assertEqual(ret, 'String')
        # test (bool)
        test_type = 'boolean'
        test_global_module = 'test_gm'
        ret = dart_converter._type_filter(test_type, test_global_module)
        self.assertEqual(ret, 'bool')
        # test (int)
        test_type = 'byte'
        test_global_module = 'test_gm'
        ret = dart_converter._type_filter(test_type, test_global_module)
        self.assertEqual(ret, 'int')
        # test (double)
        test_type = 'double'
        test_global_module = 'test_gm'
        ret = dart_converter._type_filter(test_type, test_global_module)
        self.assertEqual(ret, 'double')
        # test (sequence)
        test_type = 'sequence<double>'
        test_global_module = 'test_gm'
        ret = dart_converter._type_filter(test_type, test_global_module)
        self.assertEqual(ret, test_type)
        # test (list)
        test_type = 'double[1]'
        test_global_module = 'test_gm'
        ret = dart_converter._type_filter(test_type, test_global_module)
        self.assertEqual(ret, 'List<double>')
        # test (else)
        test_type = 'aaaa'
        test_global_module = Mock()
        test_global_module.find_types.return_value = [Mock()]
        ret = dart_converter._type_filter(test_type, test_global_module)
        self.assertEqual(ret, 'int')

    def test_type_name(self):
        """test for _type_name"""
        test_m_type = Mock()
        test_basename = 'b1'
        test_pathname = 'p1'
        test_name = 'n1'
        test_m_type.name = test_name
        test_m_type.basename = test_basename
        test_m_type.pathname = test_pathname
        self.assertEqual(dart_converter._type_name(
            test_m_type, test_pathname), test_basename)
        self.assertEqual(dart_converter._type_name(test_m_type, ''), test_name)

    def test_default_value(self):
        """test for _default_value"""
        # test ([])
        test_type = 'double[2]'
        ret = dart_converter._default_value(test_type)
        self.assertEqual(ret, '[0.0, 0.0]')
        # test (string)
        test_type = 'string'
        ret = dart_converter._default_value(test_type)
        self.assertEqual(ret, '""')
        # test (bool)
        test_type = 'boolean'
        ret = dart_converter._default_value(test_type)
        self.assertEqual(ret, 'false')
        # test (else)
        test_type = 'aaaa'
        ret = dart_converter._default_value(test_type)
        self.assertEqual(ret, '0')

    @mock.patch('sys.stdout.write')
    def test_generate_class_dart_type_error(self, sys_stdout_write):
        """test for generate_class_dart type error"""
        # mock for global_module
        test_gm = Mock()
        test_gm.find_types.return_value = []
        test_typename = 'double[2]'
        ret = dart_converter.generate_class_dart(test_gm, test_typename)
        sys_calls = [call('# Error. Type(%s) not found.\n' % test_typename)]
        sys_stdout_write.assert_has_calls(sys_calls)
        self.assertEqual(ret, None)

    @mock.patch('sys.stdout.write')
    def test_generate_class_dart_not_struct(self, sys_stdout_write):
        """test for generate_class_dart not struct"""
        # mock for global_module
        test_gm = Mock()
        type_mock = Mock(spec=['is_struct'])
        type_mock.is_struct = False
        test_gm.find_types.return_value = [type_mock]
        test_typename = 'double[2]'
        ret = dart_converter.generate_class_dart(test_gm, test_typename)
        sys_stdout_write.assert_not_called()
        self.assertEqual(ret, '')

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._type_filter')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._default_value')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._type_name')
    def test_generate_class_dart_struct_primitive_list(self, type_name_mock, default_value_mock, type_filter_mock, sys_stdout_write):
        """test for generate_class_dart struct member's type: primitive, list """
        # reset dart_converter's global variable
        dart_converter._parsed_types = []
        # mock for global_module
        test_gm = Mock()
        members_type_obj_type_mock = Mock(spec=['pathname', 'name', 'is_sequence'])
        members_type_obj_type_mock.pathname = 'mtot_pathname'
        members_type_obj_type_mock.name = 'boolean[1][1]' # Zero Constructor (list), Deserialization Function (primitive: bool)
        members_type_obj_type_mock.is_sequence = True # To string method (sequence)
        members_type_obj_mock = Mock(spec=['type', 'is_typedef', 'pathname', 'name'])
        members_type_obj_mock.type = members_type_obj_type_mock
        members_type_obj_mock.pathname = 'mto_pathname'
        members_type_obj_mock.name = 'mto_name'
        members_type_obj_mock.is_typedef = True
        members_type_mock = Mock(spec=['is_primitive', 'obj', 'is_array'])
        members_type_mock.is_primitive = False
        members_type_mock.is_array = True
        members_type_mock.obj = members_type_obj_mock
        member_mock = Mock(spec=['is_primitive', 'type', 'name'])
        member_mock.is_primitive = True
        member_mock.type = members_type_mock
        member_mock.name = 'member_mock'
        type_mock = Mock(spec=['is_struct', 'full_path', 'members', 'basename', 'name'])
        type_mock.is_struct = True
        type_mock.full_path = 'module1::fullpath'
        type_mock.name = 'type_mock'
        type_mock.basename = 'b1'
        type_mock.members = [member_mock]
        test_gm.find_types.return_value = [type_mock]
        # mock patch settings
        type_filter_mock.return_value = 'test1'
        default_value_mock.return_value = 'test2'
        type_name_mock.return_value = 'primitive[1]inner[1]' # typename list
        # test
        test_typename = 'double[2]'
        ret = dart_converter.generate_class_dart(test_gm, test_typename)
        sys_stdout_write.assert_not_called()
        # make expected return
        code = 'class %s {' % type_mock.basename + '\n'
        code += '  String typeCode = "%s";\n' % type_mock.full_path.replace('::', '.')
        code += '  %s %s;\n' % (type_filter_mock.return_value, member_mock.name)
        code +='\n\n  %s.zeros() {\n' % type_mock.basename
        code += '    %s = %s;\n' % (member_mock.name, default_value_mock.return_value)
        code += '  }\n'
        # Constructor
        code += '\n\n  %s( ' % type_mock.name
        code += '%s %s' % (type_filter_mock.return_value, member_mock.name + '_')
        code += ') {\n'
        code += '    %s = %s;\n' % (member_mock.name, member_mock.name + '_')
        code += '  }\n'
        code += '\n'
        code += '  List<String> serialize() {\n'
        code += '    var ls = [];\n'
        code += '    ls.add(%s[%s].toString());\n' % (member_mock.name + '[%s]' % 0, 0)
        code += '    return ls;\n'
        code += '  }\n\n'
        code += '  int parse(List<String> ls) {\n'
        code += '    int index = 0;\n'
        code += '    var len;\n'
        code += '    bool cleared = false;\n'
        code += '    %s[%s] = (ls[index] == "true");\n' % (member_mock.name + '[%s]' % 0, 0)
        code += '    index++;\n'
        code += '    return index;\n'
        code += '  }\n\n'
        code += '  String toString() {\n'
        code += '    String ret = "%s(";\n' % type_mock.name
        code += '    ret += "%s = [";\n' % member_mock.name
        code += '    for(int i = 0;i < %s.length;i++) {\n' % member_mock.name
        code += '      var elem = %s[i];\n' % member_mock.name
        code += '      ret += "$elem";\n'
        code += '      if (i != %s.length-1) {\n' % member_mock.name
        code += '        ret += ", ";\n'
        code += '      }\n'
        code += '    }\n'
        code += '    ret += "]";\n'
        code += '    return ret + ")";\n'
        code += '  }\n\n'
        code += '}\n\n'
        # comment in to know diff
        # with open('ret.txt', 'w') as f:
        #     f.write(ret)
        # with open('code.txt', 'w') as f:
        #     f.write(code)
        self.assertEqual(ret, code)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._type_filter')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._default_value')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._type_name')
    def test_generate_class_dart_struct_primitive_sequence(self, type_name_mock, default_value_mock, type_filter_mock, sys_stdout_write):
        """test for generate_class_dart struct member's type: primitive, sequence """
        # reset dart_converter's global variable
        dart_converter._parsed_types = []
        # mock for global_module
        test_gm = Mock()
        members_type_obj_type_obj_inner_type_mock = Mock(spec=['is_primitive', 'name'])
        members_type_obj_type_obj_inner_type_mock.name = 'string' # # Deserialization Function (string)
        members_type_obj_type_obj_inner_type_mock.is_primitive = True # Serialization Function (m_type.obj.inner_type.is_primitive=True)
        members_type_obj_type_mock = Mock(spec=['pathname', 'name', 'is_sequence', 'obj', 'inner_type'])
        members_type_obj_type_mock.inner_type = members_type_obj_type_obj_inner_type_mock
        members_type_obj_type_mock.pathname = 'mtot_pathname'
        members_type_obj_type_mock.name = 'boole' # Zero Constructor (sequence), Deserialization Function (primitive: bool)
        members_type_obj_type_mock.is_sequence = True # To string method (sequence)
        members_type_obj_mock = Mock(spec=['type', 'is_typedef', 'pathname', 'name'])
        members_type_obj_mock.type = members_type_obj_type_mock
        members_type_obj_mock.pathname = 'mto_pathname'
        members_type_obj_mock.name = 'mto_name'
        members_type_obj_mock.is_typedef = True
        members_type_mock = Mock(spec=['is_primitive', 'obj', 'is_array'])
        members_type_mock.is_primitive = False
        members_type_mock.is_array = True
        members_type_mock.obj = members_type_obj_mock
        member_mock = Mock(spec=['is_primitive', 'type', 'name'])
        member_mock.is_primitive = True
        member_mock.type = members_type_mock
        member_mock.name = 'member_mock'
        type_mock = Mock(spec=['is_struct', 'full_path', 'members', 'basename', 'name'])
        type_mock.is_struct = True
        type_mock.full_path = 'module1::fullpath'
        type_mock.name = 'type_mock'
        type_mock.basename = 'b1'
        type_mock.members = [member_mock]
        test_gm.find_types.return_value = [type_mock]
        # mock patch settings
        type_filter_mock.return_value = 'test1'
        default_value_mock.return_value = 'test2'
        type_name_mock.return_value = 'test3' # Serialization Function (sequence)
        # test
        test_typename = 'double[2]'
        ret = dart_converter.generate_class_dart(test_gm, test_typename)
        sys_stdout_write.assert_not_called()
        # make expected return
        code = 'class %s {' % type_mock.basename + '\n'
        code += '  String typeCode = "%s";\n' % type_mock.full_path.replace('::', '.')
        code += '  %s %s;\n' % (type_filter_mock.return_value, member_mock.name)
        # Zero Constructor
        code +='\n\n  %s.zeros() {\n' % type_mock.basename
        code += '    %s = [];\n' % member_mock.name
        code += '  }\n'
        # Constructor
        code += '\n\n  %s( ' % type_mock.name
        code += '%s %s' % (type_filter_mock.return_value, member_mock.name + '_')
        code += ') {\n'
        code += '    %s = %s;\n' % (member_mock.name, member_mock.name + '_')
        code += '  }\n'
        code += '\n'
        # Serialization Function
        code += '  List<String> serialize() {\n'
        code += '    var ls = [];\n'
        code += '    ls.add(%s.length.toString());\n' % member_mock.name
        code += '    %s.forEach((var elem) {\n' % member_mock.name
        code += '      ls.add(elem.toString());\n'
        code += '    });\n'
        code += '    return ls;\n'
        code += '  }\n\n'
        # Deserialization Function
        code += '  int parse(List<String> ls) {\n'
        code += '    int index = 0;\n'
        code += '    var len;\n'
        code += '    bool cleared = false;\n'
        code += '    len = num.parse(ls[index]);\n'
        code += '    index++;\n'
        code += '    cleared = len != %s.length;\n' % member_mock.name
        code += '    if (cleared) %s.clear();\n' % member_mock.name
        code += '    for(int i = 0;i < len;i++) {\n'
        code += '      if (cleared) %s.add((ls[index]));\n' % member_mock.name
        code += '      else %s[i] = (ls[index]);\n' % member_mock.name
        code += '      index++;\n'
        code += '    }\n'
        code += '    return index;\n'
        code += '  }\n\n'
        # To string method
        code += '  String toString() {\n'
        code += '    String ret = "%s(";\n' % type_mock.name
        code += '    ret += "%s = [";\n' % member_mock.name
        code += '    for(int i = 0;i < %s.length;i++) {\n' % member_mock.name
        code += '      var elem = %s[i];\n' % member_mock.name
        code += '      ret += "$elem";\n'
        code += '      if (i != %s.length-1) {\n' % member_mock.name
        code += '        ret += ", ";\n'
        code += '      }\n'
        code += '    }\n'
        code += '    ret += "]";\n'
        code += '    return ret + ")";\n'
        code += '  }\n\n'
        code += '}\n\n'
        # comment in to know diff
        # with open('ret.txt', 'w') as f:
        #     f.write(ret)
        # with open('code.txt', 'w') as f:
        #     f.write(code)
        # self.assertEqual(ret, code)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._type_filter')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._default_value')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._type_name')
    def test_generate_class_dart_struct_primitive_primitive(self, type_name_mock, default_value_mock, type_filter_mock, sys_stdout_write):
        """test for generate_class_dart struct member's type: primitive, primitive """
        # reset dart_converter's global variable
        dart_converter._parsed_types = []
        # mock for global_module
        test_gm = Mock()
        members_type_obj_type_obj_inner_type_mock = Mock(spec=['is_primitive', 'name'])
        members_type_obj_type_obj_inner_type_mock.name = 'string'
        members_type_obj_type_obj_inner_type_mock.is_primitive = True # Serialization Function (m_type.obj.inner_type.is_primitive=True)
        members_type_obj_type_mock = Mock(spec=['pathname', 'name', 'is_sequence', 'is_primitive' 'obj', 'inner_type'])
        members_type_obj_type_mock.inner_type = members_type_obj_type_obj_inner_type_mock
        members_type_obj_type_mock.pathname = 'mtot_pathname'
        members_type_obj_type_mock.name = 'boolean' # Zero Constructor (not list), Deserialization Function (primitive: bool)
        members_type_obj_type_mock.is_sequence = False # To string method (not sequence)
        members_type_obj_type_mock.is_primitive = True # Zero Constructor (primitive)
        members_type_obj_mock = Mock(spec=['type', 'is_typedef', 'pathname', 'name'])
        members_type_obj_mock.type = members_type_obj_type_mock
        members_type_obj_mock.pathname = 'mto_pathname'
        members_type_obj_mock.name = 'mto_name'
        members_type_obj_mock.is_typedef = True
        members_type_mock = Mock(spec=['is_primitive', 'obj', 'is_array'])
        members_type_mock.is_primitive = False
        members_type_mock.is_array = True
        members_type_mock.obj = members_type_obj_mock
        member_mock = Mock(spec=['is_primitive', 'type', 'name'])
        member_mock.is_primitive = True
        member_mock.type = members_type_mock
        member_mock.name = 'member_mock'
        type_mock = Mock(spec=['is_struct', 'full_path', 'members', 'basename', 'name'])
        type_mock.is_struct = True
        type_mock.full_path = 'module1::fullpath'
        type_mock.name = 'type_mock'
        type_mock.basename = 'b1'
        type_mock.members = [member_mock]
        test_gm.find_types.return_value = [type_mock]
        # mock patch settings
        type_filter_mock.return_value = 'test1'
        default_value_mock.return_value = 'test2'
        type_name_mock.return_value = 'test3' # Serialization Function (sequence)
        # test
        test_typename = 'double[2]'
        ret = dart_converter.generate_class_dart(test_gm, test_typename)
        sys_stdout_write.assert_not_called()
        # make expected return
        code = 'class %s {' % type_mock.basename + '\n'
        code += '  String typeCode = "%s";\n' % type_mock.full_path.replace('::', '.')
        code += '  %s %s;\n' % (type_filter_mock.return_value, member_mock.name)
        # Zero Constructor
        code +='\n\n  %s.zeros() {\n' % type_mock.basename
        code += '    %s = %s;\n' % (member_mock.name, default_value_mock.return_value)
        code += '  }\n'
        # Constructor
        code += '\n\n  %s( ' % type_mock.name
        code += '%s %s' % (type_filter_mock.return_value, member_mock.name + '_')
        code += ') {\n'
        code += '    %s = %s;\n' % (member_mock.name, member_mock.name + '_')
        code += '  }\n'
        code += '\n'
        # Serialization Function
        code += '  List<String> serialize() {\n'
        code += '    var ls = [];\n'
        code += '    ls.add(%s.toString());\n' % member_mock.name
        code += '    return ls;\n'
        code += '  }\n\n'
        # Deserialization Function
        code += '  int parse(List<String> ls) {\n'
        code += '    int index = 0;\n'
        code += '    var len;\n'
        code += '    bool cleared = false;\n'
        code += '    %s = ls[index] == "true";\n' % member_mock.name
        code += '    index++;\n'
        code += '    return index;\n'
        code += '  }\n\n'
        # To string method
        code += '  String toString() {\n'
        code += '    String ret = "%s(";\n' % type_mock.name
        code += '    ret += "%s = $%s";\n' % (member_mock.name, member_mock.name)
        code += '    return ret + ")";\n'
        code += '  }\n\n'
        code += '}\n\n'
        # comment in to know diff
        # with open('ret.txt', 'w') as f:
        #     f.write(ret)
        # with open('code.txt', 'w') as f:
        #     f.write(code)
        # self.assertEqual(ret, code)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._type_filter')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._default_value')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._type_name')
    def test_generate_class_dart_struct_primitive_struct(self, type_name_mock, default_value_mock, type_filter_mock, sys_stdout_write):
        """test for generate_class_dart struct member's type: primitive, struct """
        # reset dart_converter's global variable
        dart_converter._parsed_types = []
        # mock for global_module
        test_gm = Mock()
        members_type_obj_type_obj_inner_type_mock = Mock(spec=['is_primitive', 'name'])
        members_type_obj_type_obj_inner_type_mock.name = 'string'
        members_type_obj_type_obj_inner_type_mock.is_primitive = True # Serialization Function (m_type.obj.inner_type.is_primitive=True)
        members_type_obj_type_obj_mock = Mock(spec=['is_struct'])
        members_type_obj_type_obj_mock.is_struct = True # Zero Constructor (struct)
        members_type_obj_type_mock = Mock(spec=['pathname', 'name', 'is_sequence', 'is_struct', 'is_primitive' 'obj', 'inner_type'])
        members_type_obj_type_mock.inner_type = members_type_obj_type_obj_inner_type_mock
        members_type_obj_type_mock.pathname = 'mtot_pathname'
        members_type_obj_type_mock.name = 'boolean' # Zero Constructor (not list), Deserialization Function (primitive: bool)
        members_type_obj_type_mock.is_sequence = False # To string method (not sequence)
        members_type_obj_type_mock.is_primitive = False # Zero Constructor (not primitive)
        members_type_obj_type_mock.obj = members_type_obj_type_obj_mock
        members_type_obj_mock = Mock(spec=['type', 'is_typedef', 'pathname', 'name'])
        members_type_obj_mock.type = members_type_obj_type_mock
        members_type_obj_mock.pathname = 'mto_pathname'
        members_type_obj_mock.name = 'mto_name'
        members_type_obj_mock.is_typedef = True
        members_type_mock = Mock(spec=['is_primitive', 'obj', 'is_array'])
        members_type_mock.is_primitive = False
        members_type_mock.is_array = True
        members_type_mock.obj = members_type_obj_mock
        member_mock = Mock(spec=['is_primitive', 'type', 'name'])
        member_mock.is_primitive = True
        member_mock.type = members_type_mock
        member_mock.name = 'member_mock'
        type_mock = Mock(spec=['is_struct', 'full_path', 'members', 'basename', 'name'])
        type_mock.is_struct = True
        type_mock.full_path = 'module1::fullpath'
        type_mock.name = 'type_mock'
        type_mock.basename = 'b1'
        type_mock.members = [member_mock]
        test_gm.find_types.return_value = [type_mock]
        # mock patch settings
        type_filter_mock.return_value = 'test1'
        default_value_mock.return_value = 'test2'
        type_name_mock.return_value = 'test3' # Serialization Function (sequence)
        # test
        test_typename = 'double[2]'
        ret = dart_converter.generate_class_dart(test_gm, test_typename)
        sys_stdout_write.assert_not_called()
        # make expected return
        code = 'class %s {' % type_mock.basename + '\n'
        code += '  String typeCode = "%s";\n' % type_mock.full_path.replace('::', '.')
        code += '  %s %s;\n' % (type_filter_mock.return_value, member_mock.name)
        # Zero Constructor
        code +='\n\n  %s.zeros() {\n' % type_mock.basename
        code += '    %s = new %s.zeros();\n' % (member_mock.name, members_type_obj_mock.name)
        code += '  }\n'
        # Constructor
        code += '\n\n  %s( ' % type_mock.name
        code += '%s %s' % (type_filter_mock.return_value, member_mock.name + '_')
        code += ') {\n'
        code += '    %s = %s;\n' % (member_mock.name, member_mock.name + '_')
        code += '  }\n'
        code += '\n'
        # Serialization Function
        code += '  List<String> serialize() {\n'
        code += '    var ls = [];\n'
        code += '    ls.addAll(%s.serialize());\n' % (member_mock.name)
        code += '    return ls;\n'
        code += '  }\n\n'
        # Deserialization Function
        code += '  int parse(List<String> ls) {\n'
        code += '    int index = 0;\n'
        code += '    var len;\n'
        code += '    bool cleared = false;\n'
        code += '    index += %s.parse(ls.sublist(index));\n' % member_mock.name
        code += '    return index;\n'
        code += '  }\n\n'
        # To string method
        code += '  String toString() {\n'
        code += '    String ret = "%s(";\n' % type_mock.name
        code += '    ret += "%s = $%s";\n' % (member_mock.name, member_mock.name)
        code += '    return ret + ")";\n'
        code += '  }\n\n'
        code += '}\n\n'
        # comment in to know diff
        # with open('ret.txt', 'w') as f:
        #     f.write(ret)
        # with open('code.txt', 'w') as f:
        #     f.write(code)
        # self.assertEqual(ret, code)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._type_filter')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._default_value')
    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter._type_name')
    def test_generate_class_dart_struct_primitive_enum(self, type_name_mock, default_value_mock, type_filter_mock, sys_stdout_write):
        """test for generate_class_dart struct member's type: primitive, enum """
        # reset dart_converter's global variable
        dart_converter._parsed_types = []
        # mock for global_module
        test_gm = Mock()
        members_type_obj_type_obj_inner_type_mock = Mock(spec=['is_primitive', 'name'])
        members_type_obj_type_obj_inner_type_mock.name = 'string'
        members_type_obj_type_obj_inner_type_mock.is_primitive = True # Serialization Function (m_type.obj.inner_type.is_primitive=True)
        members_type_obj_type_obj_mock = Mock(spec=['is_struct'])
        members_type_obj_type_obj_mock.is_struct = False # Zero Constructor (not struct)
        members_type_obj_type_obj_mock.is_enum = True # Zero Constructor (enum)
        members_type_obj_type_mock = Mock(spec=['pathname', 'name', 'is_sequence', 'is_struct', 'is_primitive' 'obj', 'inner_type'])
        members_type_obj_type_mock.inner_type = members_type_obj_type_obj_inner_type_mock
        members_type_obj_type_mock.pathname = 'mtot_pathname'
        members_type_obj_type_mock.name = 'boolean' # Zero Constructor (not list), Deserialization Function (primitive: bool)
        members_type_obj_type_mock.is_sequence = False # To string method (not sequence)
        members_type_obj_type_mock.is_primitive = False # Zero Constructor (not primitive)
        members_type_obj_type_mock.obj = members_type_obj_type_obj_mock
        members_type_obj_mock = Mock(spec=['type', 'is_typedef', 'pathname', 'name'])
        members_type_obj_mock.type = members_type_obj_type_mock
        members_type_obj_mock.pathname = 'mto_pathname'
        members_type_obj_mock.name = 'mto_name'
        members_type_obj_mock.is_typedef = True
        members_type_mock = Mock(spec=['is_primitive', 'obj', 'is_array'])
        members_type_mock.is_primitive = False
        members_type_mock.is_array = True
        members_type_mock.obj = members_type_obj_mock
        member_mock = Mock(spec=['is_primitive', 'type', 'name'])
        member_mock.is_primitive = True
        member_mock.type = members_type_mock
        member_mock.name = 'member_mock'
        type_mock = Mock(spec=['is_struct', 'full_path', 'members', 'basename', 'name'])
        type_mock.is_struct = True
        type_mock.full_path = 'module1::fullpath'
        type_mock.name = 'type_mock'
        type_mock.basename = 'b1'
        type_mock.members = [member_mock]
        test_gm.find_types.return_value = [type_mock]
        # mock patch settings
        type_filter_mock.return_value = 'test1'
        default_value_mock.return_value = 'test2'
        type_name_mock.return_value = 'test3' # Serialization Function (sequence)
        # test
        test_typename = 'double[2]'
        ret = dart_converter.generate_class_dart(test_gm, test_typename)
        sys_stdout_write.assert_not_called()
        # make expected return
        code = 'class %s {' % type_mock.basename + '\n'
        code += '  String typeCode = "%s";\n' % type_mock.full_path.replace('::', '.')
        code += '  %s %s;\n' % (type_filter_mock.return_value, member_mock.name)
        # Zero Constructor
        code +='\n\n  %s.zeros() {\n' % type_mock.basename
        code += '    %s = 0;\n' % (member_mock.name)
        code += '  }\n'
        # Constructor
        code += '\n\n  %s( ' % type_mock.name
        code += '%s %s' % (type_filter_mock.return_value, member_mock.name + '_')
        code += ') {\n'
        code += '    %s = %s;\n' % (member_mock.name, member_mock.name + '_')
        code += '  }\n'
        code += '\n'
        # Serialization Function
        code += '  List<String> serialize() {\n'
        code += '    var ls = [];\n'
        code += '    return ls;\n'
        code += '  }\n\n'
        # Deserialization Function
        code += '  int parse(List<String> ls) {\n'
        code += '    int index = 0;\n'
        code += '    var len;\n'
        code += '    bool cleared = false;\n'
        code += '    return index;\n'
        code += '  }\n\n'
        # To string method
        code += '  String toString() {\n'
        code += '    String ret = "%s(";\n' % type_mock.name
        code += '    return ret + ")";\n'
        code += '  }\n\n'
        code += '}\n\n'
        # comment in to know diff
        # with open('ret.txt', 'w') as f:
        #     f.write(ret)
        # with open('code.txt', 'w') as f:
        #     f.write(code)
        # self.assertEqual(ret, code)



if __name__ == '__main__':
    unittest.main()
