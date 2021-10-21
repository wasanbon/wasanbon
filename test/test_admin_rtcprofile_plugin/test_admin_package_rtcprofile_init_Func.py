# test for wasanbon/core/plugins/admin/rtcprofile_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

import wasanbon


class TestPlugin(unittest.TestCase):

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.admin.rtcprofile_plugin as m
        self.test = m

    def get_rtcp(self, prefix, not_check_sv):
        basicInfo = MagicMock()
        type(basicInfo).name = PropertyMock(return_value='test_name' + prefix)
        type(basicInfo).category = PropertyMock(return_value='test_category' + prefix)
        type(basicInfo).vendor = PropertyMock(return_value='test_vendor' + prefix)
        type(basicInfo).version = PropertyMock(return_value='test_version' + prefix)
        type(basicInfo).description = PropertyMock(return_value='test_description' + prefix)

        dataport = MagicMock()
        type(dataport).name = PropertyMock(return_value='dataport_name' + prefix)
        type(dataport).portType = PropertyMock(return_value='dataport_porttype' + prefix)
        type(dataport).type = PropertyMock(return_value='dataport_type' + prefix)
        type(dataport).prefix = PropertyMock(return_value=prefix)

        serviceInterface = MagicMock()
        type(serviceInterface).name = PropertyMock(return_value='serviceInterface_name' + prefix)
        type(serviceInterface).type = PropertyMock(return_value='serviceInterface_type' + prefix)
        type(serviceInterface).instanceName = PropertyMock(return_value='serviceInterface_instanceName' + prefix)
        type(serviceInterface).direction = PropertyMock(return_value='serviceInterface_direction' + prefix)
        type(serviceInterface).prefix = PropertyMock(return_value=prefix)
        serviceport = MagicMock()
        type(serviceport).name = PropertyMock(return_value='serviceport_name' + prefix)
        type(serviceport).serviceInterfaces = PropertyMock(return_value=[serviceInterface])
        type(serviceport).prefix = PropertyMock(return_value=prefix)

        data = {'key1': 'value1' + prefix, 'key2': 'value2' + prefix}
        conf_set = MagicMock()
        type(conf_set).name = PropertyMock(return_value='conf_set_name' + prefix)
        type(conf_set).type = PropertyMock(return_value='conf_set_type' + prefix)
        type(conf_set).defaultValue = PropertyMock(return_value='conf_set_defaultValue' + prefix)
        type(conf_set).data = data
        type(conf_set).prefix = PropertyMock(return_value=prefix)

        rtcprofile = MagicMock()
        type(rtcprofile).basicInfo = PropertyMock(return_value=basicInfo)
        type(rtcprofile).dataports = PropertyMock(return_value=[dataport])
        type(rtcprofile).serviceports = PropertyMock(return_value=[serviceport])
        type(rtcprofile).configurationSet = MagicMock()
        type(rtcprofile).configurationSet.configurations = [conf_set]

        def equals(self, target):
            return prefix == target.prefix

        type(dataport).equals = equals
        type(serviceInterface).equals = equals
        if not not_check_sv:
            type(serviceport).equals = equals
        type(conf_set).equals = equals

        return rtcprofile

    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.RTCProfileBuilder')
    @mock.patch('sys.stdout.write')
    def test_compare_rtcprofile_1(self, mock_write, mock_RTCProfileBuilder):
        """compare_rtcprofile not modified case """

        rtcp = self.get_rtcp('_1', False)
        rtcp_real = self.get_rtcp('_1', False)

        builder = MagicMock()
        mock_RTCProfileBuilder.return_value = builder
        type(builder).setBasicInfo = MagicMock()
        type(builder).removeDataPort = MagicMock()
        type(builder).appendDataPort = MagicMock()
        type(builder).removeServiceInterfaceFromServicePort = MagicMock()
        type(builder).removeServicePort = MagicMock()
        type(builder).appendServiceInterfaceToServicePort = MagicMock()
        type(builder).appendServicePort = MagicMock()
        type(builder).removeConfiguration = MagicMock()
        type(builder).appendConfiguration = MagicMock()

        ### test ###
        self.test.compare_rtcprofile(rtcp, rtcp_real, verbose=True)
        mock_write.assert_any_call('Not Modified.\n')
        builder.setBasicInfo.assert_not_called()
        builder.removeDataPort.assert_not_called()
        builder.appendDataPort.assert_not_called()
        builder.removeServiceInterfaceFromServicePort.assert_not_called()
        builder.removeServicePort.assert_not_called()
        builder.appendServiceInterfaceToServicePort.assert_not_called()
        builder.appendServicePort.assert_not_called()
        builder.removeConfiguration.assert_not_called()
        builder.appendConfiguration.assert_not_called()

    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.RTCProfileBuilder')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.util.yes_no', return_value='yes')
    def test_compare_rtcprofile_2(self, mock_yes_no, mock_write, mock_RTCProfileBuilder):
        """compare_rtcprofile modified case """

        rtcp = self.get_rtcp('_1', True)
        rtcp_real = self.get_rtcp('_2', True)

        builder = MagicMock()
        mock_RTCProfileBuilder.return_value = builder
        type(builder).setBasicInfo = MagicMock()
        type(builder).removeDataPort = MagicMock()
        type(builder).appendDataPort = MagicMock()
        type(builder).removeServiceInterfaceFromServicePort = MagicMock()
        type(builder).removeServicePort = MagicMock()
        type(builder).appendServiceInterfaceToServicePort = MagicMock()
        type(builder).appendServicePort = MagicMock()
        type(builder).removeConfiguration = MagicMock()
        type(builder).appendConfiguration = MagicMock()

        ### test ###
        self.test.compare_rtcprofile(rtcp, rtcp_real, verbose=True)
        mock_write.assert_any_call('Modified.\n')
        builder.setBasicInfo.assert_has_calls([call('test_name_2', 'test_category_2', 'test_vendor_2', 'test_version_2', 'test_description_2')])
        builder.removeDataPort.assert_has_calls([call(rtcp.dataports[0])])
        builder.appendDataPort.assert_has_calls([call('dataport_porttype_2', 'dataport_type_2', 'dataport_name_2')])
        builder.removeServiceInterfaceFromServicePort.assert_has_calls([call('serviceport_name_1', 'serviceInterface_name_1')])
        builder.removeServicePort.assert_not_called()
        builder.appendServiceInterfaceToServicePort.assert_has_calls(
            [call('serviceport_name_2', '', '', 'serviceInterface_type_2', 'serviceInterface_direction_2', 'serviceInterface_name_2')])
        builder.appendServicePort.assert_not_called()
        builder.removeConfiguration.assert_has_calls([call('conf_set_name_1')])
        builder.appendConfiguration.assert_has_calls([call('conf_set_type_2', 'conf_set_name_2', 'conf_set_defaultValue_2')])

    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.RTCProfileBuilder')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.util.yes_no', return_value='yes')
    def test_compare_rtcprofile_3(self, mock_yes_no, mock_write, mock_RTCProfileBuilder):
        """compare_rtcprofile modified case """

        rtcp = self.get_rtcp('_1', False)
        rtcp_real = self.get_rtcp('_2', False)

        builder = MagicMock()
        mock_RTCProfileBuilder.return_value = builder
        type(builder).setBasicInfo = MagicMock()
        type(builder).removeDataPort = MagicMock()
        type(builder).appendDataPort = MagicMock()
        type(builder).removeServiceInterfaceFromServicePort = MagicMock()
        type(builder).removeServicePort = MagicMock()
        type(builder).appendServiceInterfaceToServicePort = MagicMock()
        type(builder).appendServicePort = MagicMock()
        type(builder).removeConfiguration = MagicMock()
        type(builder).appendConfiguration = MagicMock()

        ### test ###
        self.test.compare_rtcprofile(rtcp, rtcp_real, verbose=True)
        mock_write.assert_any_call('Modified.\n')
        builder.setBasicInfo.assert_has_calls([call('test_name_2', 'test_category_2', 'test_vendor_2', 'test_version_2', 'test_description_2')])
        builder.removeDataPort.assert_has_calls([call(rtcp.dataports[0])])
        builder.appendDataPort.assert_has_calls([call('dataport_porttype_2', 'dataport_type_2', 'dataport_name_2')])
        builder.removeServiceInterfaceFromServicePort.assert_not_called()
        builder.removeServicePort.assert_has_calls([call(rtcp.serviceports[0])])
        builder.appendServiceInterfaceToServicePort.assert_has_calls(
            [call('serviceport_name_2', '', '', 'serviceInterface_type_2', 'serviceInterface_direction_2', 'serviceInterface_name_2')])
        builder.appendServicePort.assert_has_calls([call('serviceport_name_2')])
        builder.removeConfiguration.assert_has_calls([call('conf_set_name_1')])
        builder.appendConfiguration.assert_has_calls([call('conf_set_type_2', 'conf_set_name_2', 'conf_set_defaultValue_2')])


if __name__ == '__main__':
    unittest.main()
