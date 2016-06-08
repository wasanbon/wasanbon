import subprocess, os, sys, types

wellknown_idls = ['BasicDataType.idl', 'InterfaceDataTypes.idl', 'ExtendedDataTypes.idl']
int_types = ['long', 'long long', 'unsigned long', 'short', 'unsigned short', 'char', 'unsigned char', 'byte', 'unsigned byte', 'octet']
float_types = ['float', 'double', 'long double']

def copy_idl_and_compile(parser, idl_path):
    idl_dir = os.path.join('modules', 'idl')
    if not os.path.isdir(idl_dir):
        os.mkdir(idl_dir)

    copy_idl(parser, idl_path, idl_dir)
    compile_idl(parser, idl_dir)
    pass

def copy_idl(parser, idl_path, idl_dir):
    if os.path.basename(idl_path) in wellknown_idls:
        return True
    import shutil
    shutil.copy(idl_path, os.path.join(idl_dir, os.path.basename(idl_path)))

    included_paths = parser.includes(idl_path)
    for p in included_paths:
        copy_idl(parser, p, idl_dir)

def compile_idl(parser, idl_dir):
    cmd = ['omniidl', '-bpython']
    for dir in parser.dirs:
        if os.path.isdir(dir):
            cmd.append('-I%s' % dir)
        pass

    for p in os.listdir(idl_dir):
        if p.endswith('.idl'):
            cmd.append(os.path.join('idl', p))
    print cmd
    cwd = os.getcwd()
    os.chdir('modules')
    subprocess.call(cmd)
    os.chdir(cwd)
    


def create_tolist_converter(value_dic, list_name= '_d_list', indent = '', context = ''):
    #def generate_inport_converter_python(self, value_dic, list_name= '_d_list', indent = '', context = ''):
    """ serialize to list
    """
    indent_ = '' + indent
    
    code = '%s%s = []\n' % (indent, list_name)
    import yaml
    # code = code + '# %s\n' % yaml.dump(value_dic)
    keys_ = value_dic.keys()
    keys_.sort()
    #for key, value in value_dic.items():
    for key in keys_:
        value = value_dic[key]
        if key.find(']') >= 0: # Sequence
            root_name = key[:key.find('[')]
            root_name = context + '.' + root_name if len(context) > 0 else root_name
            code = code + '%s%s.append(str(len(%s)))\n' % (indent_, list_name, root_name)
            if type(value) is types.StringType:
                code = code + '%sfor elem in %s:\n' % (indent_, root_name)
                if value == 'octet':
                    code = code + '%s%s.append(str(ord(elem)))\n' % (indent_ + '  ', list_name)
                else:
                    code = code + '%s%s.append(str(elem))\n' % (indent_ + '  ', list_name)
            else:
                code = code + 'for elem in %s:\n' % (root_name)
                code = code + create_tolist_converter(value, list_name=list_name, indent=indent_ + '  ', context = 'elem')
                pass
        else:
            context_name = context + '.' + key if len(context) > 0 else key
            context_name = context_name.replace('(', '[')
            context_name = context_name.replace(')', ']')

            code = code + '%s%s.append(str(%s))\n' % (indent_, list_name, context_name) 
            pass
    return code
    


def create_fromlist_converter(value_dic, list_name= '_d_list', indent = '', context = ''):
    #print '-----' * 5
    #print value_dic
    #print '-----' * 5
    indent_ = '' + indent
    code = ''
    keys_ = value_dic.keys()
    keys_.sort()
    #for key, value in value_dic.items():
    for key in keys_:

        value = value_dic[key]
        if key.find(']') > 0: # Sequence
            context_name = context + '.' + key if len(context) > 0 else key
            context_name = context_name[:context_name.find('[')]
            type_name = key[key.find('<')+1:key.rfind('>')]
            if type(value) is types.StringType:
                if value == 'octet':
                    code = code + '%s%s = ""\n' % (indent_, context_name)
                else:
                    code = code + '%s%s = []\n' % (indent_, context_name)
            #code = code + '%slen = int(%s[index_])\n' % (indent_, list_name)
            code = code + '%slen = int(it.next())\n' % (indent_)#, list_name)
            #code = code + '%sindex_ = index_ + 1\n' % (indent_)
            code = code + '%sfor i in range(len):\n' % (indent_)
            if type(value) is types.StringType:
                if value == 'double' or value == 'float':
                    code = code + '%s%s.append(float(it.next()))\n' % (indent_ + '  ', context_name)
                elif value == 'octet':
                    code = code + '%s%s = %s + chr(int(it.next()))\n' % (indent_ + '  ', context_name, context_name)
                elif value in int_types:
                    code = code + '%s%s.append(int(it.next()))\n' % (indent_ + '  ', context_name)
                    #code = code + '%sindex_ = index_ + 1\n' % (indent_ + '  ')
            else:
                constructor_code = admin.idl.generate_constructor_python(type_name)[0]
                code = code + '%s%s.append(%s)\n' % (indent_+'  ', context_name, constructor_code)
                code = code + self.generate_outport_converter_python(value, list_name, '  ', context_name + '[i]')
                """
                root_name = key[:key.find('[')]
                root_name = context + '.' + root_name if len(context) > 0 else root_name
                code = code + '%s%s.append(len(%s))\n' % (indent_, list_name, root_name)
                if type(value) is types.StringType:
                    code = code + '%sfor elem in %s:\n' % (indent_, root_name)
                    code = code + '%s%s.apend(elem)\n' % (indent_ + '  ', list_name)
                else:
                    code = code + 'for elem in %s:\n' % (root_name)
                    code = code + self.generate_inport_converter_python(value, list_name=list_name, indent=indent_ + '  ', context = 'elem')
                    """
                pass
        else:
            context_name = context + '.' + key if len(context) > 0 else key
            context_name = context_name.replace('(', '[')
            context_name = context_name.replace(')', ']')
            if value in int_types:
                code = code + '%s%s = int(it.next())\n' % (indent_, context_name)
            elif value in float_types:
                code = code + '%s%s = float(it.next())\n' % (indent_, context_name)
            else:
                code = code + '%s%s = (it.next())\n' % (indent_, context_name)
            #code = code + '%sindex_ = index_ + 1\n' % (indent_)
                #code = code + '%s%s.append(%s)\n' % (indent_, list_name, context_name) 
            pass
    return code
