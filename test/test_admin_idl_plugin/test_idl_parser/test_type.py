# test for wasanbon/core/plugins/admin/idl_plugin/idl_parser/type.py

import unittest
from unittest import mock
from unittest.mock import Mock, call

from wasanbon.core.plugins.admin.idl_plugin.idl_parser import type


class TestPlugin(unittest.TestCase):

    def test_is_primitive(self):
        """test for is_primitive"""
        ret = type.is_primitive('char')
        self.assertTrue(ret)
        ret = type.is_primitive('aaaa')
        self.assertFalse(ret)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLSequence')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLArray')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLPrimitive')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLBasicType')
    def test_IDLType(self, basic_mock, primitive_mock, array_mock, seq_mock):
        """test for IDLType"""
        test_name = 'void'
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        self.assertIsInstance(type.IDLType(
            test_name, test_parent_mock), type.IDLVoid)
        test_name = 'sequence'
        self.assertEqual(type.IDLType(
            test_name, test_parent_mock), seq_mock())
        test_name = '['
        self.assertEqual(type.IDLType(
            test_name, test_parent_mock), array_mock())
        test_name = 'char'
        self.assertEqual(type.IDLType(
            test_name, test_parent_mock), primitive_mock())
        test_name = 'aaaa'
        self.assertEqual(type.IDLType(
            test_name, test_parent_mock), basic_mock())

    def test_idl_type_base_init(self):
        """test for IDLTypeBase.__init__"""
        test_name = 'test_name'
        test_classname = 'test_classname'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        # test
        idl_type_base = type.IDLTypeBase(
            test_classname, test_name, test_parent_mock)
        self.assertEqual(idl_type_base._is_sequence, False)
        self.assertEqual(idl_type_base._is_primitive, False)
        # test property
        self.assertEqual(idl_type_base.is_sequence, idl_type_base._is_sequence)
        self.assertEqual(idl_type_base.is_primitive,
                         idl_type_base._is_primitive)
        # test str
        self.assertEqual('{}'.format(idl_type_base), test_name)

    def test_idl_type_void_init(self):
        """test for IDLVoid.__init__"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        # test
        idl_type_void = type.IDLVoid(test_name, test_parent_mock)
        self.assertEqual(idl_type_void._verbose, True)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_sequence_init(self, idl_type_mock):
        """test for IDLSequence.__init__"""
        test_name = 'test_sequence'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        # test
        idl_seq = type.IDLSequence(test_name, test_parent_mock)
        idl_type_mock.assert_has_calls(
            [call(test_name[:-1], test_parent_mock)])
        self.assertEqual(idl_seq._verbose, True)
        self.assertEqual(idl_seq._type, idl_type_mock())
        self.assertEqual(idl_seq._is_primitive, False)
        self.assertEqual(idl_seq._is_sequence, True)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_sequence_init_invalid(self, idl_type_mock):
        """test for IDLSequence.__init__ invalid name"""
        test_name = 'test_'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        # test
        with self.assertRaises(SyntaxError):
            type.IDLSequence(test_name, test_parent_mock)
        idl_type_mock.assert_not_called()

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_sequence_to_simple_dic(self, _):
        """test for IDLSequence.simple_dic"""
        test_name = 'test_sequence'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        idl_seq = type.IDLSequence(test_name, test_parent_mock)
        # test (quiet)
        ret = idl_seq.to_simple_dic(True)
        self.assertEqual(ret, 'sequence<%s>' % str(idl_seq.inner_type))
        # test (recursive, primitive)
        idl_seq._type.is_primitive = True
        ret = idl_seq.to_simple_dic(quiet=False, recursive=True)
        self.assertEqual(ret, {'sequence<%s>' %
                               str(idl_seq.type): str(idl_seq.type)})
        # test (recursive, not primitive)
        idl_seq._type.is_primitive = False
        ret = idl_seq.to_simple_dic(False, recursive=True)
        expected_dic = {'sequence<%s>' % str(
            idl_seq.type): idl_seq.type.obj.to_simple_dic(recursive=True, member_only=True)}
        self.assertEqual(ret, expected_dic)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_sequence_to_dic(self, _):
        """test for IDLSequence.to_dic"""
        test_name = 'test_sequence'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        idl_seq = type.IDLSequence(test_name, test_parent_mock)
        # test
        ret = idl_seq.to_dic()
        expected_dic = {'name': test_name,
                        'classname': idl_seq.classname,
                        'type': str(idl_seq.type)}
        self.assertEqual(ret, expected_dic)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_sequence_properties(self, _):
        """test for IDLSequence's properties"""
        test_name = 'test_sequence'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        root_node_mock1 = Mock(spec=['root_node'])
        root_node_mock2 = Mock(spec=['full_path'])
        root_node_mock2.full_path = test_parent
        root_node_mock1.root_node = root_node_mock2
        test_parent_mock.root_node = root_node_mock1
        idl_seq = type.IDLSequence(test_name, test_parent_mock)
        # test
        self.assertEqual(idl_seq.inner_type, idl_seq._type)
        self.assertEqual(idl_seq.obj, idl_seq)
        self.assertEqual(idl_seq.type, idl_seq._type)
        self.assertEqual(idl_seq.full_path, test_parent + type.sep + test_name)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_array_init(self, idl_type_mock):
        """test for IDLArray.__init__"""
        test_name = 'test_[1]'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        # test
        idl_seq = type.IDLArray(test_name, test_parent_mock)
        idl_type_mock.assert_has_calls([call('test_', test_parent_mock)])
        self.assertEqual(idl_seq._verbose, True)
        self.assertEqual(idl_seq._type, idl_type_mock())
        self.assertEqual(idl_seq._size, 1)
        self.assertEqual(idl_seq._is_primitive, False)
        self.assertEqual(idl_seq._is_sequence, False)
        self.assertEqual(idl_seq._is_array, True)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_array_init_invalid(self, idl_type_mock):
        """test for IDLArray.__init__ invalid name"""
        test_name = 'test_'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        # test
        with self.assertRaises(SyntaxError):
            type.IDLArray(test_name, test_parent_mock)
        idl_type_mock.assert_not_called()

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_array_to_simple_dic(self, _):
        """test for IDLArray.simple_dic"""
        test_name = 'test_[1]'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        idl_seq = type.IDLArray(test_name, test_parent_mock)
        # mock for type
        type_mock = Mock(spec=['is_array', 'primitive_type', 'name'])
        type_mock.name = 'type_name'
        type_mock.primitive_type = 'type_primitive'
        type_mock.is_array = False
        idl_seq._type = type_mock
        # test
        ret = idl_seq.to_simple_dic(True)
        self.assertEqual(ret, '{}'.format(idl_seq))

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_array_to_dic(self, _):
        """test for IDLArray.to_dic"""
        test_name = 'test_[1]'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        idl_seq = type.IDLArray(test_name, test_parent_mock)
        # test
        ret = idl_seq.to_dic()
        expected_dic = {'name': test_name,
                        'classname': idl_seq.classname,
                        'type': str(idl_seq.type)}
        self.assertEqual(ret, expected_dic)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.type.IDLType')
    def test_idl_array_properties(self, _):
        """test for IDLArray's properties"""
        test_name = 'test_[1]'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        root_node_mock1 = Mock(spec=['root_node'])
        root_node_mock2 = Mock(spec=['full_path'])
        root_node_mock2.full_path = test_parent
        root_node_mock1.root_node = root_node_mock2
        test_parent_mock.root_node = root_node_mock1
        idl_seq = type.IDLArray(test_name, test_parent_mock)
        # test (preimitive type array)
        test_primitive_type = 'test_primitive'
        type_mock = Mock(spec=['is_array', 'primitive_type'])
        type_mock.is_array = True
        type_mock.primitive_type = test_primitive_type
        idl_seq._type = type_mock
        self.assertEqual(idl_seq.inner_type, idl_seq._type)
        self.assertEqual(idl_seq.obj, idl_seq)
        self.assertEqual(idl_seq.size, idl_seq.size)
        self.assertEqual(idl_seq.type, idl_seq._type)
        self.assertEqual(idl_seq.full_path, test_parent + type.sep + test_name)
        self.assertEqual(idl_seq.primitive_type, test_primitive_type)
        # test (preimitive type not array)
        type_mock.is_array = False
        idl_seq._type = type_mock
        self.assertEqual(idl_seq.primitive_type, type_mock)

    def test_idl_primitive_init(self):
        """test for IDLPrimitive.__init__"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        # test
        idl_primitive = type.IDLPrimitive(test_name, test_parent_mock)
        self.assertEqual(idl_primitive._verbose, True)
        self.assertEqual(idl_primitive._is_primitive, True)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.node.IDLNode.refine_typename')
    def test_idl_basic_type_init(self, idl_node_mock):
        """test for IDLBasicType.__init__"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        # node mock setting
        idl_node_mock.return_value = test_name
        # test
        idl_basic_type = type.IDLBasicType(test_name, test_parent_mock)
        self.assertEqual(idl_basic_type._verbose, True)
        self.assertEqual(idl_basic_type._name, test_name)

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.node.IDLNode.root_node')
    def test_idl_basic_type_obj(self, idl_node_mock):
        """test for IDLBasicType.obj"""
        test_name = 'test_name'
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path', 'root_node'])
        test_parent_mock.full_path = test_parent
        idl_basic_type = type.IDLBasicType(test_name, test_parent_mock)
        # test (None)
        idl_node_mock.find_types.return_value = []
        self.assertEqual(idl_basic_type.obj, None)
        # test (not None)
        test_type = 'test_type'
        idl_node_mock.find_types.return_value = [test_type]
        self.assertEqual(idl_basic_type.obj, test_type)


if __name__ == '__main__':
    unittest.main()
