# test for wasanbon/core/plugins/admin/systemeditor_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.admin.systemeditor_plugin import Plugin


class TestPlugin(unittest.TestCase):

    class FunctionList:
        pass

    def setUp(self):
        self.plugin = Plugin()

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment'], self.plugin.depends())

    def test_get_active_configuration_data_1(self):
        """get_active_configuration_data normal case
        rtc has attribute 'configuration_sets'
        """
        ### setting ###
        rtc = self.FunctionList()
        conf1 = self.FunctionList()
        conf2 = self.FunctionList()
        setattr(conf1, 'id', 'not_id')
        setattr(conf2, 'id', 'id')
        setattr(rtc, 'active_configuration_set', 'id')
        setattr(rtc, 'configuration_sets', [conf1, conf2])
        setattr(conf2, 'configuration_data', 'test_configuration_data')
        ### test ###
        self.assertEqual('test_configuration_data', self.plugin.get_active_configuration_data(rtc))

    def test_get_active_configuration_data_2(self):
        """get_active_configuration_data normal case
        rtc has no attribute 'configuration_sets'
        """
        ### test ###
        self.assertEqual([], self.plugin.get_active_configuration_data('rtc'))

    def test_get_connectable_pairs(self):
        """get_connectable_pairs normal case"""
        ### setting ###
        nameserver = self.FunctionList()
        outport = self.FunctionList()
        setattr(outport, 'properties', {'dataport.data_type': 'dataport.data_type'})

        def dataports(port_type, verbose, data_type=None):
            if data_type == None:
                return [outport]
            return ['inport']
        setattr(nameserver, 'dataports', dataports)
        provport = self.FunctionList()
        interface1 = self.FunctionList()
        interface2 = self.FunctionList()
        setattr(interface1, 'polarity_as_string', lambda flag: 'hoge')
        setattr(interface2, 'polarity_as_string', lambda flag: 'Provided')
        setattr(provport, 'interfaces', [interface1, interface2])
        setattr(interface2, 'type_name', 'test_type_name')

        def svcports(polarity, interface_type=None):
            if interface_type == None:
                return [provport]
            return ['reqport']
        setattr(nameserver, 'svcports', svcports)
        pairs = []
        pairs.append([outport, 'inport'])
        pairs.append([provport, 'reqport'])
        ### test ###
        self.assertEqual(pairs, self.plugin.get_connectable_pairs([nameserver]))

    @mock.patch('rtshell.rtcryo.main')
    def test_save_to_file(self, mock_rtcryo_main):
        """save_to_file normal case"""
        ### setting ###
        nameservers = self.FunctionList()
        setattr(nameservers, 'path', ['test_path'])
        ### test ###
        self.assertEqual(0, self.plugin.save_to_file([nameservers], 'filepath'))
        mock_rtcryo_main.assert_called_once()

    @mock.patch('sys.stdout.write')
    @mock.patch('rtshell.rtcryo.main')
    def test_save_to_file_v(self, mock_rtcryo_main, mock_write):
        """save_to_file normal case with verbose option"""
        ### setting ###
        nameservers = self.FunctionList()
        setattr(nameservers, 'path', ['test_path'])
        ### test ###
        self.assertEqual(0, self.plugin.save_to_file([nameservers], 'filepath', verbose=True))
        mock_rtcryo_main.assert_called_once()
        mock_write.assert_called_once()


if __name__ == '__main__':
    unittest.main()
