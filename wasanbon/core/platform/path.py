import wasanbon
import os, sys, yaml

def init_tools_path(force=False, verbose=False):
    filename = os.path.join(wasanbon.rtm_home, 'setting.yaml')
    y = yaml.load(open(filename, 'r'))
    y = search_cmd_all(y, verbose=verbose)
    yaml.dump(y, open(filename, 'w'), encoding='utf8', allow_unicode=True, default_flow_style=False)
    

def search_cmd_all(dict, verbose=False):
    for cmd in dict.keys():
        dict[cmd] = search_command(cmd, wasanbon.setting[sys.platform]['hints'][cmd], verbose=verbose)
    return dict


def search_command(cmd, hints, verbose=False):
    if sys.platform == 'win32':
        path_splitter = ';'
        cmd = cmd + '.exe'
    elif sys.platform == 'darwin':
        path_splitter = ':'        
    elif sys.platform == 'linux2':
        path_splitter = ':'
    else:
        raise wasanbon.UnsupportedPlatformError()

    if verbose:
        sys.stdout.write(' - searching command [%s] ' % cmd)

    paths = [os.path.join(p,cmd) for p in os.environ['PATH'].split(path_splitter) \
                 if os.path.isfile(os.path.join(p,cmd))]
    if len(paths) == 0:
        paths = [hint for hint in hints if os.path.isfile(hint)]
        if len(paths) == 0:
            sys.stdout.write(' - %s not found.\n' % cmd)
            return ""

    if verbose:
        sys.stdout.write( ' '*(8-len(cmd)) + 'found in %s. \n' % paths[0])
    return paths[0]
    

