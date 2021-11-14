# test for wasanbon/core/plugins/admin/idl_plugin/idl_parser/node.py

import unittest
from unittest.mock import Mock

from wasanbon.core.plugins.admin.idl_plugin.idl_parser import node


class TestPlugin(unittest.TestCase):

    def test_init(self):
        """test for init"""
        test_classname = 'test_classname'
        test_name = 'test_name'
        # mock for parent
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path.return_value = 'test_parent'
        # test
        idl_node = node.IDLNode(test_classname, test_name, test_parent_mock)
        self.assertEqual(idl_node._classname, test_classname)
        self.assertEqual(idl_node._parent, test_parent_mock)
        self.assertEqual(idl_node._name, test_name)
        self.assertEqual(idl_node._filepath, None)

    def test_name_and_type(self):
        """test for _name_and_type"""
        test_classname = 'test_classname'
        test_name = 'test_name'
        # mock for parent
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path.return_value = 'test_parent'
        idl_node = node.IDLNode(test_classname, test_name, test_parent_mock)
        # test
        test_blocks = ['test1', 'test2']
        ret = idl_node._name_and_type(test_blocks)
        self.assertEqual(ret, (test_blocks[1], test_blocks[0]))

    def test_refine_typename_no_sequence_and_type(self):
        """test for refine_typename sequence < 0, find_types = '' """
        test_classname = 'test_classname'
        test_name = 'test_name'
        # mock for parent
        test_parent_mock = Mock(spec=['full_path', 'is_root', 'find_types'])
        test_parent_mock.full_path.return_value = 'test_parent'
        test_parent_mock.is_root.return_value = True
        test_parent_mock.find_types.return_value = ''
        idl_node = node.IDLNode(test_classname, test_name, test_parent_mock)
        # test
        test_typ = 'test1'
        ret = idl_node.refine_typename(test_typ)
        self.assertEqual(ret, test_typ)

    def test_refine_typename_no_sequence_but_find_full_path(self):
        """test for refine_typename sequence < 0, find_types = [Mock] """
        test_classname = 'test_classname'
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'is_root', 'find_types'])
        test_parent_mock.full_path.return_value = test_parent
        test_parent_mock.is_root.return_value = True
        # mock for find_types
        test_full_path = 'test_fullpath'
        full_path_mock = Mock(spec=['full_path'])
        full_path_mock.full_path = test_full_path
        test_parent_mock.find_types.return_value = [full_path_mock]
        idl_node = node.IDLNode(test_classname, test_name, test_parent_mock)
        # test
        test_typ = 'test1'
        ret = idl_node.refine_typename(test_typ)
        self.assertEqual(ret, test_full_path)

    def test_refine_typename_with_sequence(self):
        """test for refine_typename sequence > 0"""
        test_classname = 'test_classname'
        test_name = 'test_name'
        # mock for parent
        test_parent_mock = Mock(spec=['full_path', 'is_root', 'find_types'])
        test_parent_mock.full_path.return_value = 'test_parent'
        test_parent_mock.is_root.return_value = True
        test_parent_mock.find_types.return_value = ''
        idl_node = node.IDLNode(test_classname, test_name, test_parent_mock)
        # test
        test_typ = 'sequence'
        ret = idl_node.refine_typename(test_typ)
        typ_ = test_typ[test_typ.find('<') + 1: test_typ.find('>')]
        self.assertEqual(ret, 'sequence < ' + typ_ + ' >')

    def test_properties(self):
        """test for properties"""
        test_classname = 'test_classname'
        test_name = 'test_name'
        # mock for parent
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path.return_value = 'test_parent'
        idl_node = node.IDLNode(test_classname, test_name, test_parent_mock)
        # test (exept logics)
        self.assertEqual(idl_node.filepath, idl_node._filepath)
        self.assertEqual(idl_node.is_array, test_classname == 'IDLArray')
        self.assertEqual(idl_node.is_void, test_classname == 'IDLVoid')
        self.assertEqual(idl_node.is_struct, test_classname == 'IDLStruct')
        self.assertEqual(idl_node.is_typedef, test_classname == 'IDLTypedef')
        self.assertEqual(idl_node.is_sequence, test_classname == 'IDLSequence')
        self.assertEqual(idl_node.is_primitive,
                         test_classname == 'IDLPrimitive')
        self.assertEqual(idl_node.is_interface,
                         test_classname == 'IDLInterface')
        self.assertEqual(idl_node.is_enum, test_classname == 'IDLEnum')
        self.assertEqual(idl_node.classname, test_classname)
        self.assertEqual(idl_node.name, test_name)
        self.assertEqual(idl_node.parent, test_parent_mock)
        self.assertEqual(idl_node.is_root, test_parent_mock == None)

    def test_properties_basename(self):
        """test for properties basename"""
        test_classname = 'test_classname'
        # mock for parent
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path.return_value = 'test_parent'
        # test (with "::")
        test_name = 'test_name::test1'
        idl_node = node.IDLNode(test_classname, test_name, test_parent_mock)
        self.assertEqual(idl_node.basename,
                         test_name[test_name.rfind('::') + 2:])
        # test (without "::")
        test_name = 'test_nametest1'
        idl_node = node.IDLNode(test_classname, test_name, test_parent_mock)
        self.assertEqual(idl_node.basename, test_name)

    def test_properties_pathname(self):
        """test for properties pathname"""
        test_classname = 'test_classname'
        # mock for parent
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path.return_value = 'test_parent'
        # test (with "::")
        test_name = 'test_name::test1'
        idl_node = node.IDLNode(test_classname, test_name, test_parent_mock)
        self.assertEqual(idl_node.pathname, test_name[:test_name.rfind('::')])
        # test (without "::")
        test_name = 'test_nametest1'
        idl_node = node.IDLNode(test_classname, test_name, test_parent_mock)
        self.assertEqual(idl_node.pathname, '')


if __name__ == '__main__':
    unittest.main()
