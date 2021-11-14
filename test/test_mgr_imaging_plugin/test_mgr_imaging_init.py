# test for wasanbon/core/plugins/mgr/admin_plugin/__init__.py

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
        import wasanbon.core.plugins.mgr.imaging_plugin as m
        self.admin_mock = MagicMock(spec=['rtc'])
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()
        self.func = m

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.mgr.imaging_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.rtc'], self.plugin.depends())

    def test_get_num_ports_1(self):
        """get_num_ports left < right case"""

        rtcprof = MagicMock()
        outports = [1, 2, 3]
        inports = [1, 2]

        serviceInterface_provider = MagicMock()
        type(serviceInterface_provider).direction = 'Provided'
        serviceInterface_consumer = MagicMock()
        type(serviceInterface_consumer).direction = 'Required'

        serviceport1 = MagicMock()
        type(serviceport1).serviceInterfaces = [serviceInterface_consumer]
        serviceport2 = MagicMock()
        type(serviceport2).serviceInterfaces = [serviceInterface_provider]

        type(rtcprof).outports = outports
        type(rtcprof).inports = inports
        type(rtcprof).serviceports = [serviceport1, serviceport2]

        ### test ###
        num_port, num_rightside_port, num_leftside_port = self.plugin.get_num_ports(rtcprof)
        self.assertEqual(5, num_port)
        self.assertEqual(5, num_rightside_port)
        self.assertEqual(4, num_leftside_port)

    def test_get_num_ports_2(self):
        """get_num_ports left > right case"""

        rtcprof = MagicMock()
        outports = [1, 2, 3]
        inports = [1, 2, 3, 4]

        serviceInterface_provider = MagicMock()
        type(serviceInterface_provider).direction = 'Provided'
        serviceInterface_consumer = MagicMock()
        type(serviceInterface_consumer).direction = 'Required'

        serviceport1 = MagicMock()
        type(serviceport1).serviceInterfaces = [serviceInterface_consumer]
        serviceport2 = MagicMock()
        type(serviceport2).serviceInterfaces = [serviceInterface_provider]

        type(rtcprof).outports = outports
        type(rtcprof).inports = inports
        type(rtcprof).serviceports = [serviceport1, serviceport2]

        ### test ###
        num_port, num_rightside_port, num_leftside_port = self.plugin.get_num_ports(rtcprof)
        self.assertEqual(6, num_port)
        self.assertEqual(5, num_rightside_port)
        self.assertEqual(6, num_leftside_port)

    @mock.patch('wasanbon.core.plugins.mgr.imaging_plugin.Plugin.get_num_ports', return_value=(0, 0, 0))
    def test_get_image_height_1(self, mock_get_num_ports):
        """get_image_height no port case"""

        ### test ###
        rtcconf = MagicMock()
        img_height = self.plugin.get_image_height(rtcconf, port_height=10)
        mock_get_num_ports.assert_called_once_with(rtcconf)
        self.assertEqual(60, img_height)

    @mock.patch('wasanbon.core.plugins.mgr.imaging_plugin.Plugin.get_num_ports', return_value=(5, 5, 4))
    def test_get_image_height_2(self, mock_get_num_ports):
        """get_image_height with port case"""

        ### test ###
        rtcconf = MagicMock()
        img_height = self.plugin.get_image_height(rtcconf, port_height=10)
        mock_get_num_ports.assert_called_once_with(rtcconf)
        self.assertEqual(150, img_height)

    @mock.patch('wasanbon.core.plugins.mgr.imaging_plugin.Plugin.write_rtc_image')
    def test_get_image(self, mock_write_rtc_image):
        """get_image normal case"""

        ### test ###
        rtcconf = MagicMock()
        result = self.plugin.get_image(rtcconf, port_height=10,
                                       fill_color=(0, 0, 0, 0), line_color=(1, 1, 1, 1), background_color=(2, 2, 2, 2))
        from PIL import Image
        im = Image.new('RGBA', (800, 70), (2, 2, 2, 2))
        mock_write_rtc_image.assert_called_once_with(im, rtcconf, (375.0, 10), 10, (1, 1, 1, 1), (0, 0, 0, 0))
        self.assertEqual(im, result)

    @mock.patch('wasanbon.core.plugins.mgr.imaging_plugin.Plugin.get_num_ports', return_value=(0, 0, 0))
    @mock.patch('PIL.ImageDraw.Draw')
    @mock.patch('PIL.ImageFont.truetype')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    def test_write_rtc_image_1(self, mock_platform, mock_truetype, mock_Draw, mock_get_num_ports):
        """write_rtc_image check font win32"""

        draw = MagicMock()
        type(draw).rectangle = MagicMock()
        type(draw).textsize = MagicMock(return_value=(100, 100))
        mock_Draw.return_value = draw

        ### test ###
        rtcconf = MagicMock()
        im = MagicMock()
        result = self.plugin.write_rtc_image(im, rtcconf, (375.0, 10), 10, (1, 1, 1, 1), (0, 0, 0, 0))
        mock_truetype.assert_any_call('C:\\Windows\\Fonts\\cour.ttf', 14)
        mock_truetype.assert_any_call('C:\\Windows\\Fonts\\cour.ttf', 20)

    @mock.patch('wasanbon.core.plugins.mgr.imaging_plugin.Plugin.get_num_ports', return_value=(0, 0, 0))
    @mock.patch('PIL.ImageDraw.Draw')
    @mock.patch('PIL.ImageFont.truetype')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    def test_write_rtc_image_2(self, mock_platform, mock_truetype, mock_Draw, mock_get_num_ports):
        """write_rtc_image check font darwin"""

        draw = MagicMock()
        type(draw).rectangle = MagicMock()
        type(draw).textsize = MagicMock(return_value=(100, 100))
        mock_Draw.return_value = draw

        ### test ###
        rtcprof = MagicMock()
        im = MagicMock()
        result = self.plugin.write_rtc_image(im, rtcprof, (375.0, 10), 10, (1, 1, 1, 1), (0, 0, 0, 0))
        mock_truetype.assert_any_call('/System/Library/Fonts/Supplemental/Courier New.ttf', 14)
        mock_truetype.assert_any_call('/System/Library/Fonts/Supplemental/Courier New.ttf', 20)

    @mock.patch('wasanbon.core.plugins.mgr.imaging_plugin.Plugin.get_num_ports', return_value=(0, 0, 0))
    @mock.patch('PIL.ImageDraw.Draw')
    @mock.patch('PIL.ImageFont.truetype', return_value='font')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    def test_write_rtc_image_3(self, mock_platform, mock_truetype, mock_Draw, mock_get_num_ports):
        """write_rtc_image normal case"""

        draw = MagicMock()
        type(draw).rectangle = MagicMock()
        type(draw).textsize = MagicMock(return_value=(100, 100))
        type(draw).text = MagicMock()
        mock_Draw.return_value = draw

        ### test ###
        rtcprof = MagicMock()
        outport = MagicMock()
        type(outport).name = 'outport_name'
        type(outport).type = 'outport_type'
        outports = [outport]
        inport = MagicMock()
        type(inport).name = 'inport_name'
        type(inport).type = 'inport_type'
        inports = [inport]

        serviceInterface_provider = MagicMock()
        type(serviceInterface_provider).direction = 'Provided'
        type(serviceInterface_provider).type = 'Provided_type'
        serviceInterface_consumer = MagicMock()
        type(serviceInterface_consumer).direction = 'Required'
        type(serviceInterface_consumer).type = 'Required_type'

        serviceport1 = MagicMock()
        type(serviceport1).name = 'serviceport1_name'
        type(serviceport1).serviceInterfaces = [serviceInterface_consumer]
        serviceport2 = MagicMock()
        type(serviceport2).name = 'serviceport2_name'
        type(serviceport2).serviceInterfaces = [serviceInterface_provider]

        type(rtcprof).name = 'rtcprof_name'
        type(rtcprof).outports = outports
        type(rtcprof).inports = inports
        type(rtcprof).serviceports = [serviceport1, serviceport2]

        ### test ###
        im = MagicMock()
        result = self.plugin.write_rtc_image(im, rtcprof, (375.0, 10), 10, (1, 1, 1, 1), (0, 0, 0, 0))
        mock_truetype.assert_any_call('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 14)
        mock_truetype.assert_any_call('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 20)
        draw.rectangle.assert_called_once_with(((375.0, 10), (425.0, 40)), fill=(0, 0, 0, 0), outline=(1, 1, 1, 1))
        draw.textsize.assert_has_calls([call('rtcprof_name', font='font'), call('inport_name(inport_type)', font='font'),
                                       call('Required_type', font='font'), call('serviceport1_name', font='font')])
        draw.text.assert_has_calls([call((350.0, 90.0), 'rtcprof_name', font='font', fill=(1, 1, 1, 1)), call((430.0, 15.0), 'outport_name(outport_type)', fill=(1, 1, 1, 1), font='font'),
                                    call((455.0, 55.0), 'Provided_type', fill=(1, 1, 1, 1), font='font'), call(
                                        (430.0, 35.0), 'serviceport2_name', fill=(1, 1, 1, 1), font='font'),
                                    call((270.0, 15.0), 'inport_name(inport_type)', fill=(1, 1, 1, 1), font='font'),
                                    call((245.0, 55.0), 'Required_type', fill=(1, 1, 1, 1), font='font'),
                                    call((270.0, 35.0), 'serviceport1_name', fill=(1, 1, 1, 1), font='font')])

    @mock.patch('wasanbon.core.plugins.mgr.imaging_plugin.Plugin.write_rtc_image')
    @mock.patch('sys.stdout.write')
    def test_get_rtsp_image(self, mock_write, mock_write_rtc_image):
        """get_rtsp_image normal case"""

        package = MagicMock()
        rtcprof = MagicMock()
        outport = MagicMock()
        type(outport).name = 'outport_name'
        type(outport).type = 'outport_type'
        outports = [outport]
        inport = MagicMock()
        type(inport).name = 'inport_name'
        type(inport).type = 'inport_type'
        inports = [inport]

        serviceInterface_provider = MagicMock()
        type(serviceInterface_provider).direction = 'Provided'
        type(serviceInterface_provider).type = 'Provided_type'
        serviceInterface_consumer = MagicMock()
        type(serviceInterface_consumer).direction = 'Required'
        type(serviceInterface_consumer).type = 'Required_type'

        serviceport1 = MagicMock()
        type(serviceport1).name = 'serviceport1_name'
        type(serviceport1).serviceInterfaces = [serviceInterface_consumer]
        serviceport2 = MagicMock()
        type(serviceport2).name = 'serviceport2_name'
        type(serviceport2).serviceInterfaces = [serviceInterface_provider]

        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'

        type(rtcprof).name = 'rtcprof_name'
        type(rtcprof).basicInfo = basicInfo
        type(rtcprof).outports = outports
        type(rtcprof).inports = inports
        type(rtcprof).serviceports = [serviceport1, serviceport2]
        rtc = MagicMock()
        type(rtc).rtcprofile = rtcprof

        get_rtc_from_package = MagicMock(return_value=rtc)
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        rtsp = MagicMock()
        comp = MagicMock()
        type(comp).id = 'comp_id:vender:ver:comp_name'
        type(comp).instance_name = 'comp_instance_name'
        rtsp.components = [comp]

        ### test ###
        from PIL import Image
        im = Image.new('RGBA', (1600, 300), (255, 255, 255, 255))
        result = self.plugin.get_rtsp_image(package, rtsp, verbose=True)
        self.assertEqual(result, im)
        mock_write.assert_any_call('# Get RTSP Image.\n')
        mock_write.assert_any_call('# ROW = 3\n'),
        mock_write.assert_any_call('rtc_name')
        mock_write.assert_any_call('# Component comp_instance_name\n')
        mock_write.assert_any_call('# Column 1 height = 220\n')
        mock_write.assert_any_call(' - RTC (rtc_name)\n')


if __name__ == '__main__':
    unittest.main()
