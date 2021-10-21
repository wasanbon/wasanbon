# test for wasanbon/core/plugins/admin/systembuilder_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import sys
sys.path.append('../../')


class TestPlugin(unittest.TestCase):

    class FunctionList:
        pass

    def setUp(self):
        import wasanbon.core.plugins.admin.systembuilder_plugin as m
        self.plugin = m.Plugin()

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.systembuilder_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment'], self.plugin.depends())

    def test_get_component_full_path(self):
        """get_component_full_path normal case"""
        ### setting ###
        comp = self.FunctionList()
        setattr(comp, 'full_path', ['a', 'b/', 'c.rtc'])
        ### test ###
        self.assertEqual('a/b/c.rtc', self.plugin.get_component_full_path(comp))

    @mock.patch('wasanbon.core.plugins.admin.systembuilder_plugin.Plugin.get_component_full_path')
    def test_get_port_full_path(self, mock_get_component_full_path):
        """get_port_full_path normal path"""
        ### setting ###
        port = self.FunctionList()
        setattr(port, 'owner', '')
        setattr(port, 'name', 'name')
        mock_get_component_full_path.return_value = 'component_full_path'
        ### test ###
        self.assertEqual('component_full_path:name', self.plugin.get_port_full_path(port))

    def test_connect_ports(self):
        """connect_ports normal case"""
        ### setting ###
        port1 = self.FunctionList()

        def connect(port, props):
            pass
        setattr(port1, 'connect', connect)
        port1.connect = MagicMock()
        ### test ###
        self.assertEqual(0, self.plugin.connect_ports(port1, 'port2'))
        port1.connect.assert_any_call(['port2'], props={})

    @mock.patch('wasanbon.core.plugins.admin.systembuilder_plugin.Plugin.get_port_full_path')
    @mock.patch('sys.stdout.write')
    def test_connect_ports_v(self, mock_write, mock_get_port_full_path):
        """connect_ports normal case with verbose option"""
        ### setting ###
        port1 = self.FunctionList()

        def connect(port, props):
            pass
        setattr(port1, 'connect', connect)
        port1.connect = MagicMock()
        ### test ###
        self.assertEqual(0, self.plugin.connect_ports(port1, 'port2', verbose=True))
        port1.connect.assert_any_call(['port2'], props={})
        mock_write.assert_called_once()

    def test_set_active_configuration_data(self):
        """set_active_configuration_date normal case"""
        ### setting ###
        rtc = self.FunctionList()
        conf1 = self.FunctionList()
        conf2 = self.FunctionList()
        conf_data1 = self.FunctionList()
        conf_data2 = self.FunctionList()
        setattr(conf_data1, 'name', 'key')
        setattr(conf_data2, 'name', 'not_key')
        setattr(conf1, 'id', 'id')
        setattr(conf2, 'id', 'not_id')
        setattr(conf_data1, 'data', 'hoge')
        setattr(conf_data2, 'data', 'hoge')
        setattr(conf1, 'configuration_data', [conf_data1, conf_data2])
        setattr(rtc, 'configuration_sets', [conf1, conf2])
        setattr(rtc, 'active_configuration_set', 'id')
        self.plugin.set_active_configuration_data(rtc, 'key', 'value')
        ### test ###
        self.assertEqual('value', rtc.configuration_sets[0].configuration_data[0].data)
        self.assertEqual('hoge', rtc.configuration_sets[0].configuration_data[1].data)

    @mock.patch('time.sleep')
    @mock.patch('rtshell.rtresurrect.main')
    def test_build_system_1(self, mock_rtresurrect, mock_sleep):
        """build_system normal case
        system_file = None
        verbose = False
        """
        ### setting ###
        package = self.FunctionList()
        setattr(package, 'default_system_filepath', 'default_system_filepath')
        mock_rtresurrect.side_effect = [1, 0]
        ### test ###
        self.assertEqual(0, self.plugin.build_system(package))
        mock_rtresurrect.assert_called_with(['default_system_filepath'])
        mock_sleep.assert_called_once()

    @mock.patch('sys.stdout.write')
    @mock.patch('time.sleep')
    @mock.patch('rtshell.rtresurrect.main')
    def test_build_system_2(self, mock_rtresurrect, mock_sleep, mock_write):
        """build_system normal case
        system_file = 'system_file'
        verbose = True
        """
        ### setting ###
        package = self.FunctionList()
        setattr(package, 'default_system_filepath', 'default_system_filepath')
        mock_rtresurrect.side_effect = [1, 0]
        ### test ###
        self.assertEqual(0, self.plugin.build_system(package, system_file='system_file', verbose=True))
        mock_rtresurrect.assert_called_with(['system_file'])
        mock_sleep.assert_called_once()
        mock_write.assert_called()

    @mock.patch('time.sleep')
    @mock.patch('rtshell.rtresurrect.main')
    def test_build_system_errer(self, mock_rtresurrect, mock_sleep):
        """build_system error case
        raise wasanbon.BuildSystemException()
        """
        ### setting ###
        package = self.FunctionList()
        setattr(package, 'default_system_filepath', 'default_system_filepath')
        mock_rtresurrect.return_value = 1
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.BuildSystemException):
            self.assertEqual(0, self.plugin.build_system(package))
            mock_rtresurrect.assert_called_with(['default_system_filepath'])
            mock_sleep.assert_called()

    @mock.patch('time.sleep')
    @mock.patch('rtshell.rtstart.main')
    def test_activate_system_1(self, mock_rtstart, mock_sleep):
        """activate_system normal case
        system_file = None
        verbose = False
        """
        ### setting ###
        package = self.FunctionList()
        setattr(package, 'default_system_filepath', 'default_system_filepath')
        mock_rtstart.side_effect = [1, 0]
        ### test ###
        self.assertEqual(0, self.plugin.activate_system(package))
        mock_rtstart.assert_called_with(['default_system_filepath'])
        mock_sleep.assert_called_once()

    @mock.patch('sys.stdout.write')
    @mock.patch('time.sleep')
    @mock.patch('rtshell.rtstart.main')
    def test_activate_system_2(self, mock_rtstart, mock_sleep, mock_write):
        """activate_system normal case
        system_file = 'system_file'
        verbose = True
        """
        ### setting ###
        package = self.FunctionList()
        setattr(package, 'default_system_filepath', 'default_system_filepath')
        mock_rtstart.side_effect = [1, 0]
        ### test ###
        self.assertEqual(0, self.plugin.activate_system(package, system_file='system_file', verbose=True))
        mock_rtstart.assert_called_with(['system_file'])
        mock_sleep.assert_called_once()
        mock_write.assert_called()

    @mock.patch('time.sleep')
    @mock.patch('rtshell.rtstart.main')
    def test_activate_system_errer(self, mock_rtstart, mock_sleep):
        """activate_system error case
        raise wasanbon.BuildSystemException()
        """
        ### setting ###
        package = self.FunctionList()
        setattr(package, 'default_system_filepath', 'default_system_filepath')
        mock_rtstart.return_value = 1
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.BuildSystemException):
            self.assertEqual(0, self.plugin.activate_system(package))
            mock_rtstart.assert_called_with(['default_system_filepath'])
            mock_sleep.assert_called()

    @mock.patch('time.sleep')
    @mock.patch('rtshell.rtstop.main')
    def test_deactivate_system_1(self, mock_rtstop, mock_sleep):
        """deactivate_system normal case
        system_file = None
        verbose = False
        """
        ### setting ###
        package = self.FunctionList()
        setattr(package, 'default_system_filepath', 'default_system_filepath')
        mock_rtstop.side_effect = [1, 0]
        ### test ###
        self.assertEqual(0, self.plugin.deactivate_system(package))
        mock_rtstop.assert_called_with(['default_system_filepath'])
        mock_sleep.assert_called_once()

    @mock.patch('sys.stdout.write')
    @mock.patch('time.sleep')
    @mock.patch('rtshell.rtstop.main')
    def test_deactivate_system_2(self, mock_rtstop, mock_sleep, mock_write):
        """deactivate_system normal case
        system_file = 'system_file'
        verbose = True
        """
        ### setting ###
        package = self.FunctionList()
        setattr(package, 'default_system_filepath', 'default_system_filepath')
        mock_rtstop.side_effect = [1, 0]
        ### test ###
        self.assertEqual(0, self.plugin.deactivate_system(package, system_file='system_file', verbose=True))
        mock_rtstop.assert_called_with(['system_file'])
        mock_sleep.assert_called_once()
        mock_write.assert_called()

    @mock.patch('time.sleep')
    @mock.patch('rtshell.rtstop.main')
    def test_deactivate_system_errer(self, mock_rtstop, mock_sleep):
        """deactivate_system error case
        raise wasanbon.BuildSystemException()
        """
        ### setting ###
        package = self.FunctionList()
        setattr(package, 'default_system_filepath', 'default_system_filepath')
        mock_rtstop.return_value = 1
        ### test ###
        import wasanbon
        with self.assertRaises(wasanbon.BuildSystemException):
            self.assertEqual(0, self.plugin.deactivate_system(package))
            mock_rtstop.assert_called_with(['default_system_filepath'])
            mock_sleep.assert_called()


if __name__ == '__main__':
    unittest.main()
