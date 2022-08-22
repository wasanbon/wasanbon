# test for wasanbon/core/plugins/admin/idl_plugin/idl_parser/typedef.py

import unittest
from unittest import mock
from unittest.mock import Mock

from wasanbon.core.plugins.admin.idl_plugin.idl_parser import typedef


class TestPlugin(unittest.TestCase):

    def test_idl_typedef_init(self):
        """test for IDLTypedef.__init__"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        # test
        idl_typedef = typedef.IDLTypedef(test_parent_mock)
        self.assertEqual(idl_typedef._verbose, True)
        self.assertEqual(idl_typedef._type, None)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_typedef_to_parse_blocks_with_blacket(self, idl_type_mock):
        """test for IDLTypedef.parse_blocks([a])"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_typedef = typedef.IDLTypedef(test_parent_mock)
        # test
        test_blocks = ['d', 'b[c', '[a']
        test_filepath = 'test_filepath'
        idl_typedef.parse_blocks(test_blocks, test_filepath)
        idl_type_mock.assert_called_once_with('d [c', idl_typedef)
        self.assertEqual(idl_typedef._filepath, test_filepath)
        self.assertEqual(idl_typedef._name, 'b')

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_typedef_to_parse_blocks_without_blacket(self, idl_type_mock):
        """test for IDLTypedef.parse_blocks without []"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_typedef = typedef.IDLTypedef(test_parent_mock)
        # test
        test_blocks = ['a']
        test_filepath = 'test_filepath'
        idl_typedef.parse_blocks(test_blocks, test_filepath)
        idl_type_mock.assert_called_once_with('', idl_typedef)
        self.assertEqual(idl_typedef._filepath, test_filepath)
        self.assertEqual(idl_typedef._name, 'a')

    def test_idl_typedef_to_simple_dic(self):
        """test for IDLTypedef.simple_dic"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_typedef = typedef.IDLTypedef(test_parent_mock)
        # test (quiet)
        ret = idl_typedef.to_simple_dic(True)
        self.assertEqual(ret, 'typedef ' + idl_typedef.name)
        # test (recursive, not primitive, member_only)
        # mock for type
        type_mock = Mock(spec=['is_primitive', 'obj'])
        type_mock.is_primitive = False
        obj_mock = Mock(spec=['to_simple_dic'])
        type_mock.obj = obj_mock
        idl_typedef._type = type_mock
        ret = idl_typedef.to_simple_dic(
            False, recursive=True, member_only=True)
        n = 'typedef ' + str(idl_typedef.type) + ' ' + idl_typedef.name
        expected_dic = {n: (obj_mock.to_simple_dic())}
        self.assertEqual(ret, expected_dic)
        # test (recursive, primitive, member_only)
        # mock for type
        type_mock = Mock(spec=['is_primitive', 'obj'])
        type_mock.is_primitive = True
        idl_typedef._type = type_mock
        ret = idl_typedef.to_simple_dic(
            False, recursive=True, member_only=True)
        n = 'typedef ' + str(idl_typedef.type) + ' ' + idl_typedef.name
        expected_dic = {n: str(idl_typedef.type)}
        self.assertEqual(ret, expected_dic)
        # test (recursive, primitive, not member_only)
        # mock for type
        type_mock = Mock(spec=['is_primitive', 'obj'])
        type_mock.is_primitive = True
        idl_typedef._type = type_mock
        ret = idl_typedef.to_simple_dic(
            False, recursive=True, member_only=False)
        n = 'typedef ' + str(idl_typedef.type) + ' ' + idl_typedef.name
        expected_dic = {idl_typedef.name: {n: str(idl_typedef.type)}}
        self.assertEqual(ret, expected_dic)
        # test (not quiet, not recursive)
        ret = idl_typedef.to_simple_dic(False, recursive=False)
        expected_dic = 'typedef %s %s' % (idl_typedef.type, idl_typedef.name)
        self.assertEqual(ret, expected_dic)

    def test_idl_typedef_to_dic(self):
        """test for IDLTypedef.to_dic"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_typedef = typedef.IDLTypedef(test_parent_mock)
        # test
        ret = idl_typedef.to_dic()
        expected_dic = {'name': idl_typedef.name,
                        'classname': idl_typedef.classname,
                        'type': str(idl_typedef.type)}
        self.assertEqual(ret, expected_dic)

    def test_idl_typedef_properties(self):
        """test for IDLTypedef's properties"""
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        idl_typedef = typedef.IDLTypedef(test_parent_mock)
        # test
        self.assertEqual(idl_typedef.full_path, test_parent +
                         typedef.sep + idl_typedef.name)
        self.assertEqual(idl_typedef.type, idl_typedef._type)


if __name__ == '__main__':
    unittest.main()
