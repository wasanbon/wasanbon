import os
import sys

_parsed_types = []


def generate_converter(parser, verbose=False):
    gm = parser.global_module
    global _parsed_types
    _parsed_types = []
    for m in gm.modules:
        print('-------', m.name, '------')
        code = ''
        for s in m.structs:
            code = code + generate_class_dart(gm, s.full_path) + '\n'
            # self._apply_post_process_dart(code)
            # print code

        code = _apply_post_process_dart(code)
        if not os.path.isdir('dart'):
            os.mkdir('dart')
        if not os.path.isdir('dart/lib'):
            os.mkdir('dart/lib')
        f = open('dart/lib/%s.dart' % (m.name.lower()), 'w')
        comment_code = """/// file: %s
/// generator: wasanbon
///


""" % (m.name.lower() + '.dart')
        f.write(comment_code)
        f.write(code)
        f.close()

    pass


def _apply_post_process_dart(code):
    using_module_name = []
    for token in [t.strip() for t in code.split(' ')]:
        if token.find('::') > 0:
            module_name = token[:token.find('::')]
            if not module_name in using_module_name:
                using_module_name.append(module_name)
        pass

    import_code = ''
    for module_name in using_module_name:
        import_code = import_code + "import '%s.dart' as %s;\n" % (module_name.lower(), module_name)

    code = import_code + '\n\n' + code
    code = code.replace('::', '.')
    code = code.replace('sequence', 'List')

    return code


int_types = ['unsigned long', 'unsigned short', 'unsigned long long', 'unsigned char', 'long', 'short', 'char', 'byte', 'octet', 'wchar']
double_types = ['double', 'long double', 'float']


def _type_filter(n, global_module):
    if n == 'string' or n == 'wstring':
        n = 'String'
    elif n == 'boolean':
        n = 'bool'
    elif n in int_types:
        n = 'int'
    elif n in double_types:
        n = 'double'
    elif n.startswith('sequence'):
        n_ = n[n.find('<') + 1:n.rfind('>')]
        n = 'sequence<%s>' % _type_filter(n_, global_module)
    elif n.find('[') > 0:
        primitive_type = n[:n.find('[')]
        inner_type = primitive_type + n[n.find(']') + 1:]
        num_elem = int(n[n.find('[') + 1:n.find(']')])
        n = 'List<%s>' % _type_filter(inner_type, global_module)
    else:
        typs = global_module.find_types(n)
        if len(typs) > 0:
            if typs[0].is_enum:
                n = 'int'
    return n


def _type_name(m_type, module_name):
    if not m_type.is_primitive:
        if m_type.obj is not None and m_type.obj.is_typedef:
            m_type = m_type.obj.type
    return m_type.basename if m_type.pathname == module_name else m_type.name


def _default_value(n):
    if n.find('[') > 0:
        primitive_type = n[:n.find('[')]
        inner_type = primitive_type + n[n.find(']') + 1:]
        num_elem = int(n[n.find('[') + 1:n.find(']')])
        s = '['
        for i in range(num_elem):
            s = s + _default_value(inner_type)
            if i != num_elem - 1:
                s = s + ', '
        s = s + ']'
        return s
    elif n in double_types:
        return "0.0"
    elif n == 'string' or n == 'wstring':
        return '""'
    elif n == 'boolean':
        return "false"
    else:
        return "0"
    return "__ERROR__"


def generate_class_dart(global_module, typename):
    gm = global_module
    #gm = admin.idl.get_global_module()
    typs = gm.find_types(typename)
    if len(typs) == 0:
        sys.stdout.write('# Error. Type(%s) not found.\n' % typename)
        return None
    typ = typs[0]

    codes = ['']
    global _parsed_types
    #self._parsed_types = []

    #value_dic = self.generate_value_dic(typename, verbose=False)

    def _parse_typedef(typ):
        if not typ.type.is_primitive:
            if typ.type.obj.is_struct:
                _parse_struct(typ.type.obj)
            elif typ.type.obj.is_sequence:
                # print 'hoge', typ.type.obj.inner_type
                if not typ.type.obj.inner_type.is_primitive:
                    _parse_type(typ.type.obj.inner_type.obj)
        pass

    def _parse_struct(typ):
        # print 'Parsing struct ', typ.full_path

        code = ''
        if typ.full_path in _parsed_types:
            return code

        else:
            _parsed_types.append(typ.full_path)

        module_name = typ.full_path
        if module_name.find('::') > 0:
            module_name = module_name[:module_name.rfind('::')]
        # print typ.name
        for m in typ.members:
            # print m.name
            if m.type.is_primitive:
                pass
            elif m.type.is_array:
                pass
            elif m.type.obj is not None:
                if m.type.obj.is_struct:
                    _parse_struct(m.type.obj)
                elif m.type.obj.is_typedef:
                    _parse_typedef(m.type.obj)

        code = code + 'class %s {' % typ.basename + '\n'
        code = code + '  String typeCode = "%s";\n' % typ.full_path.replace('::', '.')
        for m in typ.members:
            m_type = m.type
            n = None
            if not m_type.is_primitive:
                if m_type.obj is not None and m_type.obj.is_typedef:
                    m_type = m.type.obj.type  # = 'typedef'

            n = m_type.basename if m_type.pathname == module_name else m_type.name
            n = _type_filter(n, global_module)
            code = code + '  %s %s;\n' % (n, m.name)

        #int_types = ['unsigned long', 'unsigned short', 'unsigned long long', 'unsigned char', 'long', 'short', 'char', 'byte', 'octet']
        #double_types = ['double', 'long double', 'float']

        # Zero Constructor
        code = code + '\n\n'
        code = code + '  %s.zeros() {\n' % typ.basename
        for m in typ.members:
            m_type = m.type
            n = None
            if not m_type.is_primitive:
                if m_type.obj is not None and m_type.obj.is_typedef:
                    m_type = m.type.obj.type  # = 'typedef'
            n = m_type.basename if m_type.pathname == module_name else m_type.name

            if m_type.name.find('[') > 0:
                code = code + '    %s = %s;\n' % (m.name, _default_value(n))
            elif m_type.is_sequence:
                code = code + '    %s = [];\n' % m.name
            elif m_type.is_primitive:
                code = code + '    %s = %s;\n' % (m.name, _default_value(n))
            elif m_type.obj is not None:
                if m_type.obj.is_struct:
                    code = code + '    %s = new %s.zeros();\n' % (m.name, n)
                elif m_type.obj.is_enum:
                    code = code + '    %s = 0;\n' % (m.name)
            else:
                print(m_type)
        code = code + '  }\n'
        #

        # Constructor
        code = code + '\n\n'
        code = code + '  %s( ' % typ.name
        # Arguments
        for m in typ.members:
            m_type = m.type
            n = None
            if not m_type.is_primitive:
                if  m_type.obj is not None and m_type.obj.is_typedef:
                    m_type = m.type.obj.type  # = 'typedef'
            n = m_type.basename if m_type.pathname == module_name else m_type.name

            n = _type_filter(n, global_module)

            code = code + '%s %s, ' % (n, m.name + '_')
        code = code[:-2]
        code = code + ') {\n'
        # content
        for m in typ.members:
            m_type = m.type
            n = None
            if not m_type.is_primitive:
                if m_type.obj is not None and m_type.obj.is_typedef:
                    m_type = m.type.obj.type  # = 'typedef'
            n = m_type.basename if m_type.pathname == module_name else m_type.name

            code = code + '    %s = %s;\n' % (m.name, m.name + '_')

        code = code + '  }\n'

        code = code + '\n'

        # Serialization Function
        code = code + '  List<String> serialize() {\n'
        code = code + '    var ls = [];\n'

        map = {}
        for m in typ.members:
            map[m.name] = m

        keys_ = [m.name for m in typ.members]
        keys_.sort()

        # for m in typ.members:
        for k in keys_:
            m = map[k]
            m_type = m.type
            if not m_type.is_primitive:
                if m_type.obj is not None and m_type.obj.is_typedef:
                    m_type = m_type.obj.type
            n = _type_name(m_type, module_name)

            if n.find('[') > 0:
                def _serialize_static_list(m_type, n, context, code):
                    primitive_type = n[:n.find('[')]
                    inner_type = primitive_type + n[n.find(']') + 1:]
                    num_elem = int(n[n.find('[') + 1:n.find(']')])

                    for i in range(num_elem):
                        if inner_type.find('[') >= 0:
                            code = _serialize_static_list(m_type, inner_type, context + '[%s]' % i, code)
                        else:
                            code = code + '    ls.add(%s[%s].toString());\n' % (context, i)
                    return code

                code = _serialize_static_list(m_type, n, m.name, code)
                pass
            elif m_type.is_sequence:
                code = code + '    ls.add(%s.length.toString());\n' % m.name
                code = code + '    %s.forEach((var elem) {\n' % m.name
                if m_type.obj.inner_type.is_primitive:
                    code = code + '      ls.add(elem.toString());\n'
                else:
                    code = code + '      ls.add(elem.serialize());\n'
                code = code + '    });\n'
                pass
            elif m_type.is_primitive:
                code = code + '    ls.add(%s.toString());\n' % m.name
            elif m_type.obj is not None and m_type.obj.is_struct:
                code = code + '    ls.addAll(%s.serialize());\n' % (m.name)
        code = code + '    return ls;\n'
        code = code + '  }\n\n'

        # Deserialization Function

        code = code + '  int parse(List<String> ls) {\n'
        code = code + '    int index = 0;\n'
        code = code + '    var len;\n'
        code = code + '    bool cleared = false;\n'

        map = {}
        for m in typ.members:
            map[m.name] = m

        keys_ = [m.name for m in typ.members]
        keys_.sort()

        for k in keys_:
            m = map[k]
            m_type = m.type
            n = None

            if not m_type.is_primitive:
                if m_type.obj is not None and m_type.obj.is_typedef:
                    m_type = m.type.obj.type
            n = m_type.basename if m_type.pathname == module_name else m_type.name
            if n.find('[') > 0:
                def _deserialize(n, context, code):
                    primitive_type = n[:n.find('[')].strip()
                    inner_type = primitive_type + n[n.find(']') + 1:]
                    num_elem = int(n[n.find('[') + 1:n.find(']')])

                    for i in range(num_elem):
                        if inner_type.find('[') >= 0:
                            code = _deserialize(inner_type, context + '[%s]' % i, code)
                        else:
                            if primitive_type == 'boolean':
                                code = code + '    %s[%s] = (ls[index] == "true");\n' % (context, i)
                                code = code + '    index++;\n'
                            elif primitive_type == 'string' or primitive_type == 'wstring':
                                code = code + '    %s[%s] = (ls[index]);\n' % (context, i)
                                code = code + '    index++;\n'
                            elif primitive_type in int_types or primitive_type in double_types:
                                code = code + '    %s[%s] = num.parse(ls[index]);\n' % (context, i)
                                code = code + '    index++;\n'
                            else:
                                code = code + '    index += %s[%s].parse(ls.sublist(index));\n' % (context, i)

                    return code
                code = _deserialize(n, m.name, code)
                pass

            elif m_type.is_sequence:
                code = code + '    len = num.parse(ls[index]);\n'
                code = code + '    index++;\n'
                code = code + '    cleared = len != %s.length;\n' % m.name
                code = code + '    if (cleared) %s.clear();\n' % m.name
                code = code + '    for(int i = 0;i < len;i++) {\n'
                if m_type.inner_type.is_primitive:
                    if m_type.inner_type.name == 'string' or m_type.inner_type.name == 'wstring':
                        code = code + '      if (cleared) %s.add((ls[index]));\n' % m.name
                        code = code + '      else %s[i] = (ls[index]);\n' % m.name
                        code = code + '      index++;\n'
                    elif m_type.inner_type.name == 'boolean':
                        code = code + '      if (cleared) %s.add(ls[index] == "true");\n' % m.name
                        code = code + '      else %s[i] = ls[index] == "true";\n' % m.name
                        code = code + '      index++;\n'
                    else:
                        code = code + '      if (cleared) %s.add(num.parse(ls[index]));\n' % m.name
                        code = code + '      else %s[i] = num.parse(ls[index]);\n' % m.name
                        code = code + '      index++;\n'
                elif m_type.is_struct:
                    code = code + '      if (cleared) {\n'
                    code = code + '        var v = new %s().zeros();\n' % m_type.name
                    code = code + '        index += v.parse(ls.sublist(index));\n'
                    code = code + '        %s.add(v);\n' % m.name
                    code = code + '      } else {\n'
                    code = code + '        index += %s[i].parse(ls.sublist(index));\n'
                    code = code + '      }\n'
                code = code + '    }\n'
                pass
            elif m_type.is_primitive:
                if m_type.name == 'string' or m_type.name == 'wstring':
                    code = code + '    %s = ls[index];\n' % m.name
                    code = code + '    index++;\n'
                elif m_type.name == 'boolean':
                    code = code + '    %s = ls[index] == "true";\n' % m.name
                    code = code + '    index++;\n'
                else:
                    code = code + '    %s = num.parse(ls[index]);\n' % m.name
                    code = code + '    index++;\n'
            elif m_type.obj is not None and m_type.obj.is_struct:
                code = code + '    index += %s.parse(ls.sublist(index));\n' % m.name
        code = code + '    return index;\n'
        code = code + '  }\n\n'

        # To string method
        code = code + '  String toString() {\n'
        code = code + '    String ret = "%s(";\n' % typ.name
        map = {}
        for m in typ.members:
            map[m.name] = m

        keys_ = [m.name for m in typ.members]
        keys_.sort()

        counter = 0
        for k in keys_:
            m = map[k]
            m_type = m.type
            n = None
            if not m_type.is_primitive:
                if m_type.obj is not None and m_type.obj.is_typedef:
                    m_type = m.type.obj.type
            n = m_type.basename if m_type.pathname == module_name else m_type.name

            if m_type.is_sequence:
                code = code + '    ret += "%s = [";\n' % m.name
                code = code + '    for(int i = 0;i < %s.length;i++) {\n' % m.name
                code = code + '      var elem = %s[i];\n' % m.name
                code = code + '      ret += "$elem";\n'
                code = code + '      if (i != %s.length-1) {\n' % m.name
                code = code + '        ret += ", ";\n'
                code = code + '      }\n'
                code = code + '    }\n'
                code = code + '    ret += "]";\n'
                pass
            elif m_type.is_primitive:
                code = code + '    ret += "%s = $%s";\n' % (m.name, m.name)
            elif m_type.obj is not None and m_type.obj.is_struct:
                code = code + '    ret += "%s = $%s";\n' % (m.name, m.name)
            counter = counter + 1
            if counter < len(keys_):
                code = code + '    ret += ", ";\n'
        code = code + '    return ret + ")";\n'
        code = code + '  }\n\n'

        code = code + '}\n\n'
        codes[0] = codes[0] + code
        return code

    def _parse_type(typ):
        # print 'Parsing type ', typ
        if typ.is_struct:
            # print '-struct'
            _parse_struct(typ)
        else:
            # print '-', dir(typ)
            pass

        pass

    _parse_type(typ)

    return codes[0]  # _apply_post_process_dart(codes[0])
