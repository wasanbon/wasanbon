# test for wasanbon/core/plugins/admin/idlcompiler_plugin/dart_converter.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

from wasanbon.core.plugins.admin.nameserver_plugin import NameServer


class TestPlugin(unittest.TestCase):

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    def test_NameServer_properties(self, mock_RTCTree, mock_parse_path):
        """NameServer properties test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')

        self.assertEqual('localhost:2809', ns.path)
        self.assertEqual('localhost', ns.address)
        self.assertEqual('2809', ns.port)
        rtcs = ns.rtcs
        mock_parse_path.assert_called_once_with('/localhost:2809')
        mock_RTCTree.assert_called_once_with(paths='localhost', filter=['localhost'])
        get_node.assert_called_once_with('localhost')
        self.assertEqual([node], rtcs)

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    def test_NameServer_properties_2(self, mock_RTCTree, mock_parse_path):
        """NameServer properties tree is None test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = None

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        self.assertEqual(None, ns.rtcs)

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    def test_refresh_1(self, mock_write, mock_RTCTree, mock_parse_path):
        """NameServer refresh normal test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns.refresh(verbose=True, force=False)
        mock_write.assert_any_call('## Success.\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    def test_refresh_2(self, mock_print_exc, mock_write, mock_RTCTree, mock_parse_path):
        """NameServer refresh exception test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = None

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns.refresh(verbose=True, force=False)
        mock_write.assert_any_call('Failed. Exception occured.\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    def test_refresh_3(self, mock_print_exc, mock_write, mock_RTCTree, mock_parse_path):
        """NameServer refresh OBJECT_NOT_EXIST test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        import omniORB
        mock_RTCTree.side_effect = omniORB.CORBA.OBJECT_NOT_EXIST

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns.refresh(verbose=True, force=False)
        mock_write.assert_any_call('Failed. Exception occured.\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    def test_refresh_4(self, mock_print_exc, mock_write, mock_RTCTree, mock_parse_path):
        """NameServer refresh OBJECT_NOT_EXIST_NoMatch test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        import omniORB
        mock_RTCTree.side_effect = omniORB.OBJECT_NOT_EXIST_NoMatch

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns.refresh(verbose=True, force=False)
        mock_write.assert_any_call('Failed. Exception occured.\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    def test_dataports_1(self, mock_write, mock_RTCTree, mock_parse_path):
        """NameServer dataports normal test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        inport = MagicMock()
        type(inport).properties = {'dataport.data_type': 'DataInPort'}
        type(node).inports = [inport]

        outport = MagicMock()
        type(outport).properties = {'dataport.data_type': 'DataOutPort'}
        type(node).outports = [outport]

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        self.assertEqual([inport, outport], ns.dataports(data_type="any", port_type=[
                         'DataInPort', 'DataOutPort'], try_count=5, polarity="any", verbose=True))

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('traceback.print_exc')
    @mock.patch('time.sleep')
    @mock.patch('sys.stdout.write')
    def test_dataports_2(self, mock_write, mock_sleep, mock_print_exc, mock_RTCTree, mock_parse_path):
        """NameServer dataports exception test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        mock_RTCTree.side_effect = Exception()

        inport = MagicMock()
        type(inport).properties = {'dataport.data_type': 'DataInPort'}
        type(node).inports = [inport]

        outport = MagicMock()
        type(outport).properties = {'dataport.data_type': 'DataOutPort'}
        type(node).outports = [outport]

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        self.assertEqual([], ns.dataports(data_type="any", port_type=['DataInPort', 'DataOutPort'], try_count=5, polarity="any", verbose=True))

    @mock.patch('sys.stdout.write')
    def test__print_conf_set_1(self, mock_write):
        """_print_conf_set startswith('__') 1"""

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns._print_conf_set(name='__name', conf_set=None, long=False, detail=False, tablevel=2)
        mock_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    def test__print_conf_set_2(self, mock_write):
        """_print_conf_set startswith('__') 2"""

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns._print_conf_set(name='__name', conf_set=None, long=True, detail=False, tablevel=2)
        mock_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    def test__print_conf_set_3(self, mock_write):
        """_print_conf_set startswith('__') 1"""

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns._print_conf_set(name='name', conf_set=None, long=False, detail=False, tablevel=2)
        mock_write.assert_any_call('     - name\n')

    @mock.patch('sys.stdout.write')
    def test__print_conf_set_4(self, mock_write):
        """_print_conf_set long """

        data = {'key1': 'value1', 'key2': 'value2'}
        conf_set = MagicMock()
        type(conf_set).data = data

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns._print_conf_set(name='name', conf_set=conf_set, long=True, detail=False, tablevel=2)
        mock_write.assert_any_call('    name : \n')
        mock_write.assert_any_call('      key1 : value1\n')
        mock_write.assert_any_call('      key2 : value2\n')

    @mock.patch('sys.stdout.write')
    def test__print_conf_set_5(self, mock_write):
        """_print_conf_set long """

        data = {}
        conf_set = MagicMock()
        type(conf_set).data = data

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns._print_conf_set(name='name', conf_set=conf_set, long=True, detail=False, tablevel=2)
        mock_write.assert_any_call('    name : \n')
        mock_write.assert_any_call('      {}\n')

    @mock.patch('sys.stdout.write')
    def test__print_conf_set_5(self, mock_write):
        """_print_conf_set long detail """

        data = {'key1': 'value1', 'key2': 'value2'}
        conf_set = MagicMock()
        type(conf_set).data = data

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns._print_conf_set(name='name', conf_set=conf_set, long=True, detail=True, tablevel=2)
        mock_write.assert_any_call('    name : \n')
        mock_write.assert_any_call('      key1 : value1\n')
        mock_write.assert_any_call('      key2 : value2\n')

    @mock.patch('sys.stdout.write')
    def test__print_conf_set_6(self, mock_write):
        """_print_conf_set long detail"""

        data = {}
        conf_set = MagicMock()
        type(conf_set).data = data

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns._print_conf_set(name='name', conf_set=conf_set, long=True, detail=True, tablevel=2)
        mock_write.assert_any_call('    name : \n')
        mock_write.assert_any_call('      {}\n')

    @mock.patch('sys.stdout.write')
    def test_print_port_1(self, mock_write):
        """_print_port normal """

        port = MagicMock()
        type(port).name = 'port_name'

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns._print_port(port=port, long=False, detail=False, tablevel=2)
        mock_write.assert_any_call('     - port_name\n')

    @mock.patch('sys.stdout.write')
    def test_print_port_2(self, mock_write):
        """_print_port long """

        port = MagicMock()
        type(port).name = 'port_name'
        type(port).properties = {'dataport.data_type': 'any', 'port.port_type': 'CorbaPort'}

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns._print_port(port=port, long=True, detail=False, tablevel=2)
        mock_write.assert_any_call('    port_name : \n')
        mock_write.assert_any_call('      type : any\n')

    @mock.patch('sys.stdout.write')
    def test_print_port_3(self, mock_write):
        """_print_port long detail connections is 0"""

        port = MagicMock()
        type(port).name = 'port_name'
        type(port).properties = {'dataport.data_type': 'any', 'port.port_type': 'CorbaPort'}

        intf = MagicMock()
        type(intf).instance_name = 'intf_instance_name'
        type(intf).type_name = 'intf_type_name'
        type(intf).polarity_as_string = MagicMock(return_value='intf_polarity')
        type(port).interfaces = [intf]

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns._print_port(port=port, long=True, detail=True, tablevel=2)
        mock_write.assert_any_call('    port_name : \n')
        mock_write.assert_any_call('      interfaces : \n')
        mock_write.assert_any_call('        ServiceInterface : \n')
        mock_write.assert_any_call('          instance_name : intf_instance_name\n')
        mock_write.assert_any_call('          type_name : intf_type_name\n')
        mock_write.assert_any_call('          polarity : intf_polarity\n')
        mock_write.assert_any_call('      properties : \n')
        mock_write.assert_any_call('        dataport.data_type : "any"\n')
        mock_write.assert_any_call('        port.port_type : "CorbaPort"\n')
        mock_write.assert_any_call('      connections :\n')
        mock_write.assert_any_call('        {}\n')

    @mock.patch('sys.stdout.write')
    def test_print_port_4(self, mock_write):
        """_print_port long detail"""

        port = MagicMock()
        type(port).name = 'port_name'
        type(port).properties = {'dataport.data_type': 'any', 'port.port_type': 'CorbaPort'}

        intf = MagicMock()
        type(intf).instance_name = 'intf_instance_name'
        type(intf).type_name = 'intf_type_name'
        type(intf).polarity_as_string = MagicMock(return_value='intf_polarity')
        type(port).interfaces = [intf]

        con = MagicMock()
        type(con).name = 'con_name'
        type(con).id = 'con_id'
        pp = MagicMock()
        type(pp).name = 'prefix.pp_name'
        owner = MagicMock()
        type(owner).full_path_str = 'full_path_str'
        type(pp).owner = owner
        con_port = ('con_port_path', pp)
        type(con).ports = [con_port]
        type(con).properties = {'prop1_key': 'prop1_val'}
        type(port).connections = [con]

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns._print_port(port=port, long=True, detail=True, tablevel=2)
        mock_write.assert_any_call('    port_name : \n')
        mock_write.assert_any_call('      interfaces : \n')
        mock_write.assert_any_call('        ServiceInterface : \n')
        mock_write.assert_any_call('          instance_name : intf_instance_name\n')
        mock_write.assert_any_call('          type_name : intf_type_name\n')
        mock_write.assert_any_call('          polarity : intf_polarity\n')
        mock_write.assert_any_call('      properties : \n')
        mock_write.assert_any_call('        dataport.data_type : "any"\n')
        mock_write.assert_any_call('        port.port_type : "CorbaPort"\n')
        mock_write.assert_any_call('      connections :\n')
        mock_write.assert_any_call('        con_name : \n')
        mock_write.assert_any_call('          id   : con_id\n')
        mock_write.assert_any_call('          ports :\n')
        mock_write.assert_any_call('             - full_path_str:pp_name\n')
        mock_write.assert_any_call('          properties :\n')
        mock_write.assert_any_call('            prop1_key : "prop1_val"\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    def test_yaml_dump_1(self, mock_write, mock_RTCTree, mock_parse_path):
        """yaml_dump is_nameserver case"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        parent = MagicMock()
        type(parent).children = [node]
        get_node = MagicMock(return_value=parent)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        type(node).is_nameserver = True
        type(node).full_path = ['/full_path0', '/full_path1']

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns.yaml_dump(long=True, detail=True, verbose=True)
        mock_write.assert_any_call('"localhost:2809":\n')
        mock_write.assert_any_call('  "full_path1":\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    def test_yaml_dump_2(self, mock_write, mock_RTCTree, mock_parse_path):
        """yaml_dump is_manager case"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        parent = MagicMock()
        type(parent).children = [node]
        get_node = MagicMock(return_value=parent)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        type(node).is_nameserver = False
        type(node).is_manager = True
        type(node).name = 'node_name'

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns.yaml_dump(long=True, detail=True, verbose=True)
        mock_write.assert_any_call('"localhost:2809":\n')
        mock_write.assert_any_call('  node_name: {}\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    def test_yaml_dump_3(self, mock_write, mock_RTCTree, mock_parse_path):
        """yaml_dump is_directory case"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        parent = MagicMock()
        type(parent).children = [node]
        get_node = MagicMock(return_value=parent)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        type(node).is_nameserver = False
        type(node).is_manager = False
        type(node).is_directory = True
        type(node).name = 'node_name'

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns.yaml_dump(long=True, detail=True, verbose=True)
        mock_write.assert_any_call('"localhost:2809":\n')
        mock_write.assert_any_call('  node_name:\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    def test_yaml_dump_4(self, mock_write, mock_RTCTree, mock_parse_path):
        """yaml_dump is_zombie case"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        parent = MagicMock()
        type(parent).children = [node]
        get_node = MagicMock(return_value=parent)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        type(node).is_nameserver = False
        type(node).is_manager = False
        type(node).is_directory = False
        type(node).is_zombie = True
        type(node).name = 'node_name'

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns.yaml_dump(long=True, detail=True, verbose=True)
        mock_write.assert_any_call('"localhost:2809":\n')
        mock_write.assert_any_call('  node_name* : {}\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    def test_yaml_dump_5(self, mock_write, mock_RTCTree, mock_parse_path):
        """yaml_dump is_component not long and not detail case"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        parent = MagicMock()
        type(parent).children = [node]
        get_node = MagicMock(return_value=parent)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        type(node).is_nameserver = False
        type(node).is_manager = False
        type(node).is_directory = False
        type(node).is_zombie = False
        type(node).is_component = True
        type(node).name = 'node_name'

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns.yaml_dump(long=False, detail=False, verbose=True)
        mock_write.assert_any_call('"localhost:2809":\n')
        mock_write.assert_any_call('  node_name\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    def test_yaml_dump_5(self, mock_write, mock_RTCTree, mock_parse_path):
        """yaml_dump is_component long and detail empty case"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        parent = MagicMock()
        type(parent).children = [node]
        get_node = MagicMock(return_value=parent)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        type(node).is_nameserver = False
        type(node).is_manager = False
        type(node).is_directory = False
        type(node).is_zombie = False
        type(node).is_component = True
        type(node).name = 'node_name'
        type(node).get_state_string = MagicMock(return_value='node_state')

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns.yaml_dump(long=True, detail=True, verbose=True)
        # mock_write.assert_not_called()
        mock_write.assert_any_call('"localhost:2809":\n')
        mock_write.assert_any_call('  node_name:\n')
        mock_write.assert_any_call('    DataOutPorts:\n')
        mock_write.assert_any_call('      {}\n')
        mock_write.assert_any_call('    DataInPorts:\n')
        mock_write.assert_any_call('      {}\n')
        mock_write.assert_any_call('    ServicePorts:\n')
        mock_write.assert_any_call('      {}\n')
        mock_write.assert_any_call('    ConfigurationSets:\n')
        mock_write.assert_any_call('      {}\n')
        mock_write.assert_any_call('    properties:\n')
        mock_write.assert_any_call('    state : node_state\n')
        mock_write.assert_any_call('    exec_cxts:\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.NameServer._print_port')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.NameServer._print_conf_set')
    def test_yaml_dump_6(self, mock_print_conf_set, mock_print_port, mock_write, mock_RTCTree, mock_parse_path):
        """yaml_dump is_component long and detail case"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        parent = MagicMock()
        type(parent).children = [node]
        get_node = MagicMock(return_value=parent)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        type(node).is_nameserver = False
        type(node).is_manager = False
        type(node).is_directory = False
        type(node).is_zombie = False
        type(node).is_component = True
        type(node).name = 'node_name'
        type(node).get_state_string = MagicMock(return_value='node_state')

        inport = MagicMock()
        type(node).inports = [inport]

        outport = MagicMock()
        type(node).outports = [outport]

        svcport = MagicMock()
        type(node).svcports = [svcport]

        conf_set = MagicMock()
        type(node).conf_sets = {'cs': conf_set}

        type(node).properties = {'properties_key': 'properties_value'}

        ec = MagicMock()
        type(ec).properties = {'ec_properties_key': 'ec_properties_value'}
        type(node).owned_ecs = [ec]

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        ns.yaml_dump(long=True, detail=True, verbose=True)
        mock_print_port.assert_has_calls([call(outport, True, True, 4), call(inport, True, True, 4), call(svcport, True, True, 4)])
        mock_print_conf_set.assert_has_calls([call('cs', conf_set, True, True, 4)])
        mock_write.assert_any_call('"localhost:2809":\n')
        mock_write.assert_any_call('  node_name:\n')
        mock_write.assert_any_call('    DataOutPorts:\n')
        mock_write.assert_any_call('    DataInPorts:\n')
        mock_write.assert_any_call('    ServicePorts:\n')
        mock_write.assert_any_call('    ConfigurationSets:\n')
        mock_write.assert_any_call('    properties:\n')
        mock_write.assert_any_call('      properties_key : "properties_value"\n')
        mock_write.assert_any_call('    state : node_state\n')
        mock_write.assert_any_call('    exec_cxts:\n')
        mock_write.assert_any_call('      properties:\n')
        mock_write.assert_any_call('        ec_properties_key : "ec_properties_value"\n')

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    def test_svcports_1(self, mock_write, mock_RTCTree, mock_parse_path):
        """NameServer svcports normal test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        port = MagicMock()
        type(port).name = 'port_name'

        intf = MagicMock()
        type(intf).instance_name = 'intf_instance_name'
        type(intf).type_name = 'intf_type_name'
        type(intf).polarity_as_string = MagicMock(return_value='intf_polarity')
        type(port).interfaces = [intf]
        type(node).svcports = [port]

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        self.assertEqual([port], ns.svcports(interface_type='intf_type_name', try_count=5, polarity='intf_polarity', verbose=True))

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('traceback.print_exc')
    @mock.patch('time.sleep')
    @mock.patch('sys.stdout.write')
    def test_svcports_2(self, mock_write, mock_sleep, mock_print_exc, mock_RTCTree, mock_parse_path):
        """NameServer svcports exception test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        mock_RTCTree.side_effect = Exception()

        port = MagicMock()
        type(port).name = 'port_name'

        intf = MagicMock()
        type(intf).instance_name = 'intf_instance_name'
        type(intf).type_name = 'intf_type_name'
        type(intf).polarity_as_string = MagicMock(return_value='intf_polarity')
        type(port).interfaces = [intf]
        type(node).svcports = [port]

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        self.assertEqual([], ns.svcports(interface_type='intf_type_name', try_count=5, polarity='intf_polarity', verbose=True))

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    def test_components_1(self, mock_write, mock_RTCTree, mock_parse_path):
        """NameServer components normal test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        mock_RTCTree.return_value = tree

        type(node).instanceName = 'node_instanceName'

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        self.assertEqual([node], ns.components(instanceName='node_instanceName', try_count=5, verbose=True))

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('traceback.print_exc')
    @mock.patch('time.sleep')
    @mock.patch('sys.stdout.write')
    def test_components_2(self, mock_write, mock_sleep, mock_print_exc, mock_RTCTree, mock_parse_path):
        """NameServer components exception test"""

        mock_parse_path.return_value = ('localhost', 2809)
        tree = MagicMock()
        node = MagicMock()
        type(node).is_component = True
        parent = MagicMock()
        type(parent).is_manager = False
        type(node).parent = parent
        get_node = MagicMock(return_value=node)
        type(tree).get_node = get_node
        mock_RTCTree.side_effect = Exception()

        type(node).instanceName = 'node_instanceName'

        def iterate(self, func, rtcs, filter_funcs):
            for filter_func in filter_funcs:
                if filter_func(self):
                    func(self, rtcs)

        type(node).iterate = iterate

        ### test ###
        ns = NameServer(path='/localhost', pidFilePath='pid')
        self.assertEqual([], ns.components(instanceName='node_instanceName', try_count=5, verbose=True))


if __name__ == '__main__':
    unittest.main()
