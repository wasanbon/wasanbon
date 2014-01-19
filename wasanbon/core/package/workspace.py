import os, sys, yaml
import wasanbon


def save_workspace(dic):
    ws_file_name = os.path.join(wasanbon.rtm_home(), 'workspace.yaml')
    yaml.dump(dic, open(ws_file_name, 'w'), encoding='utf8', allow_unicode=True, default_flow_style=False)


def load_workspace():
    ws_file_name = os.path.join(wasanbon.rtm_home(), 'workspace.yaml')
    if not os.path.isfile(ws_file_name):
        fout = open(ws_file_name, 'w')
        fout.close()
        pass

    y = yaml.load(open(ws_file_name, 'r'))
    if not y:
        y = {}
    return y
