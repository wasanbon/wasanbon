import sys, types

def generate_value_dic(global_module, typename, root_name='_d_data', verbose=False):
    import yaml
    
    typs = global_module.find_types(typename)
    if len(typs) == 0:
        sys.stdout.write('# Error. Type(%s) not found.\n' % typename)
        return None

    typ = typs[0]
    
    typ_dic = typ.to_simple_dic(full_path=True, recursive=True)
    # print 'dump:', yaml.dump(typ_dic)
    if verbose: sys.stdout.write(yaml.dump(typ_dic, default_flow_style=False) + '\n')

    value_names_ = {}
    
    def _parse_array(value_names, value, context):
        kakko_index = value.find('[')
        kokka_index = kakko_index + value[value.find('['):].find(']')
        size = int(value[kakko_index+1 : kokka_index])
        next_value = value[:kakko_index] + value[kokka_index+1:]
        typename = value.split(' ')[0]
        for i in range(size):
            n = context + '(%s)' % i
            if next_value.find('[') >= 0:
                _parse_array(value_names, next_value, n)
            else:
                value_names[n] = typename
            
    def _parse_dic(value_names, dic, context, prev_type=''):
        for name, value in dic.items():

            if name.startswith('typedef'):

                if type(value) is types.StringType:
                    if value.find('[') >= 0:
                        _parse_array(value_names, value, context)
                    pass
                else:
                    _parse_dic(value_names, value, context)
            elif name.strip().startswith('sequence'):
                elems_ = []
                tn = name[name.find('<')+1:name.rfind('>')]
                _parse_sequence(value_names, value, context, prev_type=tn)
                #_parse_sequence(elems_, value, '')
                #_parse_list(elems_, value, context)
            else:
                vn = name.split(' ')[-1]
                tn = name[:name.rfind(vn)]
                c_ = context+ '.' + vn if len(context) > 0 else vn
                if type(value) is types.ListType:
                    _parse_list(value_names, value, c_)
                elif type(value) is types.DictType:
                    _parse_dic(value_names, value, c_, prev_type=tn)

    def _parse_sequence(value_names, s, context, prev_type=''):
        if type(s) == types.StringType: # Primitive
            value_names[context + '[_index_]<%s>' % s] = s
            pass
        elif type(s) == types.ListType:
            #_parse_dic
            v = {}
            value_names[context + '[_index_]<%s>' % prev_type] = v
            _parse_list(v, s, '')

    def _parse_str(value_names, s, context):
        vn = s.split(' ')[-1]
        n_ = context + '.' + vn if len(context) > 0 else vn
        value_names[n_] = s[:s.rfind(vn)].strip()
        

    def _parse_list(value_names, values, context): # Value must list type
        for value in values:
            if type(value) == types.DictType:
                _parse_dic(value_names, value, context)
            elif type(value) == types.StringType:
                _parse_str(value_names, value, context)
            else:
                #print '=' * 20
                #print value, type(value)
                pass


    for name, values in typ_dic.items():
        for value in values:
            if type(value) is types.StringType:
                if value.startswith('typedef'):
                    
                    pass
                else:
                    vn = value.split(' ')[-1]
                    tn = value[:value.rfind(vn)]
                    n_ = root_name + '.' + vn if len(root_name) > 0 else vn
                    value_names_[n_] = value[:value.find(vn)].strip()
            elif type(value) is types.DictType:
                _parse_dic(value_names_, value, root_name)

    
    if verbose:
        print '---' * 10
        print '---', 'value_dic', '---'
        print yaml.dump(value_names_, default_flow_style=False)
        print '---' * 10
    
    return value_names_



def generate_header(value_dic, indent_=' '):
    code = ''
    keys_ = value_dic.keys()
    keys_.sort()
    for key in keys_:
        value = value_dic[key]
        if type(value) is types.StringType:
            code = code + '%s%s: %s\n' % (indent_, key, value)
        else:
            code = code + '%s%s:\n' % (indent_, key)
            code = code + generate_header(value, indent_ + '  ')
    return code
        
