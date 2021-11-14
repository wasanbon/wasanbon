# test for wasanbon/core/plugins/admin/idl_plugin/idl_parser/token_buffer.py

import unittest

from wasanbon.core.plugins.admin.idl_plugin.idl_parser import token_buffer


class TestPlugin(unittest.TestCase):

    def test_init(self):
        """test for init"""
        test_lines = ['a', 'b', 'c']
        # test
        tb = token_buffer.TokenBuffer(test_lines)
        self.assertEqual(tb._tokens, test_lines)
        self.assertEqual(tb._token_offset, 0)
        self.assertEqual(tb.t_debug, tb._tokens)

    def test_pop_none(self):
        """test for pop (length = 0)"""
        test_lines = []
        tb = token_buffer.TokenBuffer(test_lines)
        # test
        ret = tb.pop()
        self.assertEqual(ret, None)

    def test_pop(self):
        """test for pop (length not 0)"""
        test_lines = ['a', 'b', 'c']
        tb = token_buffer.TokenBuffer(test_lines)
        # test
        ret = tb.pop()
        self.assertEqual(ret, test_lines[0])
        self.assertEqual(tb._token_offset, 1)


if __name__ == '__main__':
    unittest.main()
