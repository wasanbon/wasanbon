import os, sys
from common_converter import *
_template = """
import yaml, traceback
import RTC
import OpenRTM_aist

_data = $CONSTRUCTOR
_port = OpenRTM_aist.OutPort("$NAME", _data)


def convert(data, d_list):
  it = iter(d_list)
$CODE
  print 'converted:', data
  return data
  

def _sendData(d_list):
  convert(_data, d_list)
  _port.write()
          
def execute(comp, webSocketSender):
    comp.addOutPort("$NAME", _port)
    webSocketSender.outports[u"$NAME"] = _sendData
          
"""



def create_outport_converter_module(parser, name, typename, verbose=False):

    module_dir = 'modules'
    if not os.path.isdir(module_dir):
        os.mkdir(module_dir)
    global_module = parser.global_module

    typs = global_module.find_types(typename)
    if len(typs) == 0:
        print 'Invalid Type Name (%s)' % typename
        raise InvalidDataTypeException()
    
    module_name = typs[0].parent.name
    copy_idl_and_compile(parser, typs[0].filepath)

    filename = '%s_OutPort_%s.py' % (name, typename.replace('::', '_').strip())
    f = open(os.path.join(module_dir, filename), 'w')
    import value_dic as vd
    value_dic = vd.generate_value_dic(global_module, typename, root_name='data', verbose=verbose)
    #if verbose:
    #    print '-------value-------'
    #    import yaml
    #    print yaml.dump(value_dic, default_flow_style=False)
    #import inport_converter as ip
    global _template
    output = "%s" % _template
    code = create_fromlist_converter(value_dic, list_name='d_list', indent = '  ')
    if verbose:
        print '------data to list-----'
        print code
    output = output.replace('$NAME', name)
    typs = global_module.find_types(typename)
    output = output.replace('$CONSTRUCTOR', parser.generate_constructor_python(typs[0]))
    output = output.replace('$CODE', code)
    
    #import outport_converter as op
    #code = op.create_converter(value_dic)
    #print '------list to data-----'
    #print code

    output = 'import %s\n' % module_name + output
    
    f.write(output)
    f.close()


