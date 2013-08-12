import os, sys, time, traceback
import rtctree
import omniORB
import wasanbon


from rtshell import rtcryo

def list_available_connections():
    for i in range(0, 3):
        try:
            path, port = rtctree.path.parse_path('/localhost')
            tree = rtctree.tree.RTCTree(paths=path, filter=[path])
            dir_node = tree.get_node(path)
            types = get_port_list(tree, dir_node)
            for type in types.keys():
                for outport in types[type]['DataOutPort']:
                    for inport in types[type]['DataInPort']:
                        msg = ' - Connect   [%s]  ->  [%s]' % (port_full_path(outport), port_full_path(inport))
                        if util.no_yes(msg) == 'yes':
                            sys.stdout.write(' - connecting...')
                            outport.connect([inport])

                            sys.stdout.write(' connected.\n')
            return True
        except omniORB.CORBA.UNKNOWN, e:
            pass
        except Exception, e:
            traceback.print_exc()
            return False
            
    return False


def list_available_configurations():
    for i in range(0, 3):
        try:
            path, port = rtctree.path.parse_path('/localhost')
            tree = rtctree.tree.RTCTree(paths=path, filter=[path])
            dir_node = tree.get_node(path)

            nodes = []
            def func(node, types):
                nodes.append(node)
                pass
            def filt_func(node):
                if node.is_component and not node.parent.is_manager:
                    return True
                return False
            dir_node.iterate(func, nodes, [filt_func])

            while True:
                choices = []
                for i in range(0, len(nodes)):
                    choices.append(comp_full_path(nodes[i]))
                choices.append('quit')
                answer = util.choice(choices, msg='Select RTC to configure')
                if answer == len(nodes):
                    break
                
                while True:
                    sys.stdout.write(comp_full_path(nodes[answer]))
                    sys.stdout.write('\n  ' + nodes[answer].active_conf_set_name + '\n')
                    choices = []
                    active_conf_set = nodes[answer].active_conf_set
                    for key, value in active_conf_set.data.items():
                        choices.append(key + ':' + value)
                    choices.append('quit')
                    answer2 = util.choice(choices, msg='Select Configuration to set')
                    if answer2 == len(choices)-1:
                        break

                    key = active_conf_set.data.keys()[answer2]
                    old_val = active_conf_set.data[key]
                    sys.stdout.write(key + ':')
                    val = raw_input()
                    if util.yes_no('%s: %s ==> %s' % (key, old_val, val)) == 'yes':
                        active_conf_set.set_param(key, val)
                        print 'Updated.'
                    else:
                        print 'Aborted.'

            return True
            
        except omniORB.CORBA.UNKNOWN, e:
            traceback.print_exc()
            pass
        except Exception, e:
            traceback.print_exc()
            return False
    return False

def save_all_system(nameservers, filepath='system/DefaultSystem.xml', verbose=False):
    if verbose:
        sys.stdout.write(" - Saving System on %s to %s\n" % (str(nameservers), filepath))
    try:
        argv = ['--verbose', '-n', 'DefaultSystem01', '-v', '1.0', '-e', 'Sugar Sweet Robotics',  '-o', filepath]
        argv = argv + nameservers
        rtcryo.main(argv=argv)
    except omniORB.CORBA.UNKNOWN, e:
        traceback.print_exc()
        pass
    except Exception, e:
        traceback.print_exc()
        return False


def comp_full_path(comp):
    str = ""
    for p in comp.full_path:
        str = str + p
        if not str.endswith('/') and not str.endswith('.rtc'):
            str = str + '/'
    return str

def port_full_path(port):
    str = ""
    for p in port.owner.full_path:
        str = str + p
        if not str.endswith('/') and not str.endswith('.rtc'):
            str = str + '/'
    str = str+':'+port.name
    return str

def get_port_list(tree, dir_node):
    types = {}
    def func(node, types):
        for dataport in node.inports + node.outports:
            type = dataport.properties['dataport.data_type']
            if not type in types.keys():
                types[type] = {'DataInPort':[],'DataOutPort':[], 'CorbaPort':[] }
            types[type][dataport.porttype].append(dataport)

    def filt_func(node):
        if node.is_component and not node.parent.is_manager:
            return True
        return False

    dir_node.iterate(func, types, [filt_func])
    return types

        


