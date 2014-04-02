# Help module for wasanbon
import os, sys, locale, traceback, inspect
import wasanbon


def get_help_dir():
    helpdir = os.path.join(wasanbon.__path__[0],
                           'locale', 'messages',
                           locale.getdefaultlocale()[0])
    if not os.path.isdir(helpdir):
        helpdir = os.path.join(wasanbon.__path__[0],
                           'locale', 'messages',
                            'en_US')
    return helpdir
    
_default_help_message = {'brief' : 'Can not find help message.',
                         'detail' : ['Can not find help message'],
                         'subcommand' : {}}

_invalid_help_message = {'brief' : 'Can not load help message. Your system do not have yaml package',
                         'detail' : ['Can not load help message.', ' Your system do not have yaml package'],
                         'subcommand' : {}}

def get_help_dic(path, cmd):
    module_name = 'wasanbon.core.management.' + path + '.' + cmd
    __import__(module_name)
    doc = sys.modules[module_name].__doc__

    yaml = __import__('yaml')
    dic = yaml.load(doc)
    return dic


def get_help_text(path, cmd, long=False):
    help_dic = get_help_dic(path, cmd)
    loc = locale.getdefaultlocale()[0]
    if loc in help_dic.keys():
        dic = help_dic[loc]
    else:
        dic = help_dic['en_US']

    command_str = "wasanbon-admin.py" if path=='admin' else "mgr.py"

    str = """
[brief]
%s""" % dic['brief'].encode('utf-8')

    if not long:
        str = str + """(add -l for more information)

"""
    if long:
        str = str + """
[detail]
%s
""" % (dic['description'].encode('utf-8'))

    if len(dic['subcommands']) == 0:
        str = """
[Usage]
$ %s %s
""" % (command_str, cmd)+ str
        #str = str + '\n No subcommands are available.\n'
        return str
    str = """
[Usage]
$ %s %s [subcommand]
""" % (command_str, cmd) + str + "[subcommand]"

    if not long:
        str = str + """  (add -l for more information)"""
    for key, doc in dic['subcommands'].items():
        if long:
            str = str + """
 - %s
 %s""" % (key, doc.encode('utf-8'))
        else:
            str = str + """ 
 - %s """ % (key) + ' '*(15-len(key)) + doc[:doc.find('\n')].encode('utf-8')
 

    return str
    try:
        if os.path.isfile(filename):
            return yaml.load(open(filename, 'r'))
        else:
            return _default_help_message
    except:
        traceback.print_exc()
        return _invalid_help_message
    

