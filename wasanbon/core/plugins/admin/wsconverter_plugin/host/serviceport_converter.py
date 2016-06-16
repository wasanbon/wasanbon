import os, sys, subprocess, traceback
from common_converter import *

module_names = []

_header_template = """

import yaml, traceback, json
import RTC

reload(RTC)
import OpenRTM_aist

_port = OpenRTM_aist.CorbaPort("$NAME")
"""

_consumer_header_template = """
_consumer_$CONSUMERNAME = OpenRTM_aist.CorbaConsumer(interfaceType=$INTERFACETYPE)
"""

_function_template = """          
def execute(comp, webSocketSender):
"""

_consumer_register_template = """
  _port.registerConsumer("$CONSUMERNAME", "$CONSUMERTYPENAME", _consumer_$CONSUMERNAME)
"""

_add_port_template = """
  comp.addPort(_port)
"""


_consumer_method_template= """
def $CONSUMERNAME_call_$METHODNAME($ARGLIST):
"""

_tolist_converter_template = """
def _$TYPENAME_tolist(data):
$CODE
  return d_list
"""

_fromlist_converter_template = """
def _$TYPENAME_fromlist(d_list):
  data = $CONSTRUCTOR
  it = iter(d_list)
$CODE
  return data
"""

converted_types = []


def create_returns_converter(parser, name, return_typs, verbose=False, indent = '  '):
    output = indent + 'return ('
    for i, return_type in enumerate(return_typs):
        rtype = return_type
        if rtype.is_primitive:
            output = output + '[str(%s)], ' % (name + '[%s]' % i)

        if rtype.obj.is_typedef:
            rtype = return_type.obj.type

        if rtype.is_primitive:
            output = output + '[str(%s)], ' % (name + '[%s]' % i)

        elif rtype.obj.is_enum:
            output = output + '[str(%s._v)], ' % (name + '[%s]' % i)
        else:
            output = output + '_%s_tolist(%s), ' % (return_type.name.split('::')[-1], (name + '[%s]' % i))
    return output[:-2] + ',)\n'

    
def create_argument_converter(parser, arg, verbose=False, indent = '  '):
    output = ''
    arg_typ = arg.type
    if arg_typ.is_typedef:
        arg_typ = arg.type.obj.inner_type
        
    if arg_typ.is_primitive:
        output = indent + '%s_ = %s[0]\n' % (arg.name, arg.name)
    elif arg_typ.obj.is_enum:
        output = indent + '%s_ = %s[0]\n' % (arg.name, arg.name)
    else:
        output = indent + '%s_ = _%s_fromlist(%s)\n' % (arg.name, arg.type.name.split('::')[-1], arg.name)

    return output

def create_typefromlist_converter(parser, typ, verbose=False):
    # print 'create_typefromlist_converter : %s\n' % typ.name
    global_module = parser.global_module
    converter_code = ''
    arg_typ = typ
    if arg_typ.is_typedef:
        arg_typ = typ.obj.inner_type

    if not arg_typ.is_primitive:
        if arg_typ.obj.is_enum:
            return converter_code
        if not typ.name in converted_types:
            import value_dic as vd
            value_dic = vd.generate_value_dic(global_module, arg_typ.name, root_name='data', verbose=verbose)
            
            converted_types.append(typ.name)
            converter_code = _fromlist_converter_template
            converter_code = converter_code.replace('$TYPENAME', typ.name.split('::')[-1])
            converter_code = converter_code.replace('$CONSTRUCTOR', parser.generate_constructor_python(typ.obj))
            code = create_fromlist_converter(value_dic, list_name='d_list', indent = '  ')
            converter_code = converter_code.replace('$CODE', code)
    return converter_code

def create_typetolist_converter(parser, typ, verbose=False):
    # print 'create_typetolist_converter : %s\n' % typ.name
    global_module = parser.global_module
    converter_code = ''
    arg_typ = typ

    if arg_typ.is_primitive:
        return ''

    if arg_typ.obj.is_typedef:
        arg_typ = arg_typ.obj.type

    if arg_typ.is_primitive:
        return ''

        #return create_typetolist_converter(parser, arg_typ, verbose=verbose)
        
    if arg_typ.obj.is_sequence:
        inner_type = arg_typ.obj.inner_type
        ## Add Innter type converter first.
        converter_code = create_typetolist_converter(parser, inner_type, verbose=verbose)

        if not inner_type.is_primitive:
            if inner_type.obj.is_typedef:
                inner_type  = inner_type.obj.type


        if inner_type.is_primitive:
            code = """
  d_list = []
  for d in data:
    d_list.append(str(d))
"""
            converter_code = converter_code + _tolist_converter_template
            converter_code = converter_code.replace('$TYPENAME', typ.name.split('::')[-1])
            converter_code = converter_code.replace('$CONSTRUCTOR', parser.generate_constructor_python(typ.obj))
            converter_code = converter_code.replace('$CODE', code)
            return converter_code
        else:
            if inner_type.obj.is_enum:
                code = """
  d_list = []
  for d in data:
    d_list.append(str(d._v))
"""
            else:
                code = """
  d_list = []
  for d in data:
    d_list = d_list + _%s_tolist(d)
""" % inner_type.name.split('::')[-1]

            converter_code = converter_code + _tolist_converter_template
            converter_code = converter_code.replace('$TYPENAME', typ.name.split('::')[-1])
            converter_code = converter_code.replace('$CONSTRUCTOR', parser.generate_constructor_python(typ.obj))
            #code = create_tolist_converter(value_dic, list_name='d_list', indent = '  ')
            converter_code = converter_code.replace('$CODE', code)
            return converter_code


    if arg_typ.obj.is_enum:
        return converter_code
    if not arg_typ.name in converted_types:
        import value_dic as vd
        value_dic = vd.generate_value_dic(global_module, arg_typ.name, root_name='data', verbose=verbose)
        print arg_typ.name, value_dic
        converted_types.append(arg_typ.name)
        converter_code = _tolist_converter_template
        converter_code = converter_code.replace('$TYPENAME', typ.name.split('::')[-1])
        converter_code = converter_code.replace('$CONSTRUCTOR', parser.generate_constructor_python(arg_typ.obj))
        code = create_tolist_converter(value_dic, list_name='d_list', indent = '  ')
        converter_code = converter_code.replace('$CODE', code)
        print converter_code
            # print typ, 'cc', converter_code
    return converter_code

def create_argtype_converter(parser, arg, verbose=False):
    return create_typefromlist_converter(parser, arg.type, verbose=verbose)


def create_method_code(parser, typ, consumerName, method, verbose=False):
    indent = '  '
    output = _consumer_method_template
    output = output.replace('$CONSUMERNAME', consumerName)
    output = output.replace('$METHODNAME', method.name)

    return_typs = []
    if not method.returns.is_void:
        return_typs.append(method.returns)

    converter = ''
    arg_list = ''
    converted_arg_list = ''
    for arg in method.arguments:
        if arg.direction == 'in' or arg.direction == 'inout':
            arg_list = arg_list + arg.name + ', '
            converted_arg_list = converted_arg_list + arg.name + '_' + ', '
            converter = converter + create_argtype_converter(parser, arg, verbose=verbose)
            output = output + create_argument_converter(parser, arg, verbose=verbose)
        else: # out
            arg_typ = arg.type
            if arg_typ.is_typedef:
                arg_typ = arg.type.obj.inner_type

            return_typs.append(arg_typ)

    converted_arg_list = converted_arg_list[:-2]
    callstr = indent + 'return_value = _consumer_%s._ptr().%s(%s)\n' % (consumerName, method.name, converted_arg_list)
    output = output + callstr

    arg_list = arg_list[:-2]
    output = output.replace('$ARGLIST', arg_list)

    output = output + '\n  # return ' + str([r.name for r in return_typs]) + '\n'

    output = output + create_returns_converter(parser, 'return_value', return_typs, verbose=verbose)
    for return_type in return_typs:
        converter = converter + create_typetolist_converter(parser, return_type, verbose=verbose)
        pass
    
    return output, converter

def create_consumer_converter_code(parser, name, consumer, verbose=False):
    global_module = parser.global_module
    consumerName, consumerType = consumer.split('.')
    typs = global_module.find_types(consumerType)
    if len(typs) == 0:
        print 'Invalid Type Name (%s)' % consumer
        raise InvalidDataTypeException()
    if not typs[0].is_interface:
        print 'Invalid Type Specified (not interface) (%s)' % consumer
        raise InvalidDataTypeException()
    
    module_name = typs[0].parent.name
    if not module_name in module_names:
        module_names.append(module_name)
    copy_idl_and_compile(parser, typs[0].filepath)

    output = ""
    converter = ""
    for m in typs[0].methods:
        _code, _conv = create_method_code(parser, typs[0], consumerName, m, verbose=verbose)
        output = output + _code
        converter = converter + _conv

    return output + converter

def create_consumer_header_code(parser, name, consumer, verbose=False):
    global_module = parser.global_module
    consumerName, consumerType = consumer.split('.')
    typs = global_module.find_types(consumerType)
    if len(typs) == 0:
        print 'Invalid Type Name (%s)' % consumer
        raise InvalidDataTypeException()
    if not typs[0].is_interface:
        print 'Invalid Type Specified (not interface) (%s)' % consumer
        raise InvalidDataTypeException()
    
    module_name = typs[0].parent.name
    copy_idl_and_compile(parser, typs[0].filepath)
    output = _consumer_header_template
    output = output.replace('$INTERFACETYPE', typs[0].full_path.replace('::', '.'))
    output = output.replace('$CONSUMERNAME', consumerName)
    return output

def create_consumer_register_code(parser, name, consumer, verbose=False):
    global_module = parser.global_module
    consumerName, consumerType = consumer.split('.')
    typs = global_module.find_types(consumerType)
    if len(typs) == 0:
        print 'Invalid Type Name (%s)' % consumer
        raise InvalidDataTypeException()
    if not typs[0].is_interface:
        print 'Invalid Type Specified (not interface) (%s)' % consumer
        raise InvalidDataTypeException()
    
    module_name = typs[0].parent.name
    copy_idl_and_compile(parser, typs[0].filepath)
    output = _consumer_register_template
    
    output = output.replace('$CONSUMERNAME', consumerName)
    output = output.replace('$CONSUMERTYPENAME', typs[0].full_path)
    return output


def create_serviceport_converter_module(parser, name, consumers, providers, verbose=False):
    module_dir = 'modules'
    if not os.path.isdir(module_dir):
        os.mkdir(module_dir)

    global_module = parser.global_module

    filename = '%s_CorbaPort.py' % (name)
    f = open(os.path.join(module_dir, filename), 'w')
    output = _header_template
    for c in consumers:
        header_code = create_consumer_header_code(parser, name, c, verbose=verbose)
        output = output + header_code

    output = output + _function_template

    for c in consumers:
        register_code = create_consumer_register_code(parser, name, c, verbose=verbose)
        output = output + register_code
    
    output = output + _add_port_template

    for c in consumers:
        consumer_code = create_consumer_converter_code(parser, name, c, verbose=verbose)
        output = output + consumer_code

    """
    import value_dic as vd
    value_dic = vd.generate_value_dic(global_module, typename, root_name='data', verbose=verbose)

    code = create_tolist_converter(value_dic, list_name='d_list', indent = '  ')
    """
    output = output.replace('$NAME', name)
    #typs = global_module.find_types(c)
    #output = output.replace('$CONSTRUCTOR', parser.generate_constructor_python(typs[0]))
    #output = output.replace('$CODE', code)

    for module_name in module_names:
        output = 'import %s\n' % module_name + output

    f.write(output)
    f.close()
