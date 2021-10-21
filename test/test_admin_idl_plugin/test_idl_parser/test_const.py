# test for wasanbon/core/plugins/admin/idl_plugin/idl_parser/const.py

import unittest
from unittest.mock import Mock

from wasanbon.core.plugins.admin.idl_plugin.idl_parser import const


class TestPlugin(unittest.TestCase):

    def test_init(self):
        """test for init"""
        test_name = 'test_hoge'
        test_typename = 'test_type'
        test_value = 123
        # mock for parent
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path.return_value = 'test_parent'
        test_filepath = 'hogehoge.txt'
        # test
        idl_const = const.IDLConst(test_name, test_typename, test_value, test_parent_mock, test_filepath)
        self.assertEqual(idl_const._typename, test_typename)
        self.assertEqual(idl_const._value, test_value)
        self.assertEqual(idl_const._filepath, test_filepath)

    def test_to_simple_dic_case_true(self):
        """test for simple_dic(quiet=True, full_path=True)"""
        test_name = 'test_hoge'
        test_typename = 'test_type'
        test_value = 123
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        test_filepath = 'hogehoge.txt'
        idl_const = const.IDLConst(test_name, test_typename, test_value, test_parent_mock, test_filepath)
        # test
        ret = idl_const.to_simple_dic(True, True)
        self.assertEqual(ret, 'const %s %s = %s' % (test_typename, idl_const.full_path, test_value))

    def test_to_simple_dic_case_false(self):
        """test for simple_dic(quiet=False, full_path=False)"""
        test_name = 'test_hoge'
        test_typename = 'test_type'
        test_value = 123
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        test_filepath = 'hogehoge.txt'
        idl_const = const.IDLConst(test_name, test_typename, test_value, test_parent_mock, test_filepath)
        # test
        ret = idl_const.to_simple_dic(False, False)
        expected_dic = {'const %s' % test_name: {'type': test_typename,
                                   'value': test_value}}
        self.assertEqual(ret, expected_dic)

    def test_to_dic(self):
        """test for to_dic"""
        test_name = 'test_hoge'
        test_typename = 'test_type'
        test_value = 123
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        test_filepath = 'hogehoge.txt'
        idl_const = const.IDLConst(test_name, test_typename, test_value, test_parent_mock, test_filepath)
        # test
        ret = idl_const.to_dic()
        expected_dic = {'name': test_name,
                        'filepath': test_filepath,
                        'classname': idl_const._classname,
                        'typename': test_typename,
                        'value': test_value}
        self.assertEqual(ret, expected_dic)

    def test_properties(self):
        """test for properties"""
        test_name = 'test_hoge'
        test_typename = 'test_type'
        test_value = 123
        # mock for parent
        test_parent = 'test_parent'
        test_parent_mock = Mock(spec=['full_path'])
        test_parent_mock.full_path = test_parent
        test_filepath = 'hogehoge.txt'
        idl_const = const.IDLConst(test_name, test_typename, test_value, test_parent_mock, test_filepath)
        # test
        self.assertEqual(idl_const.typename, test_typename)
        self.assertEqual(idl_const.value, test_value)
        self.assertEqual(idl_const.full_path, test_parent+const.sep+test_name)


if __name__ == '__main__':
    unittest.main()
