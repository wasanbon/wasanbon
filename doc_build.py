#!/usr/bin/env python
import os, sys
import subprocess

import yaml


def check(cmds):
    p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    ret = (p.stdout.read(), p.stderr.read())
    return ret



def get_subcommands():
    ret = check(['wasanbon-admin.py', '-h'])
    y = yaml.load(ret[0][ret[0].find('subcommand-set'):])
    return y['subcommand-set']


def main():
    help_dic = {}

    for cmd in get_subcommands():
        if cmd == 'help':
            continue
        help_dic[cmd] = yaml.load(check(['wasanbon-admin.py', cmd, '-h'])[0])
    
    build_html(help_dic, command='wasanbon-admin.py', link_prex='admin_')



def tag(tag, val):
    return '<%s>%s</%s>' % (tag, val, tag)

def h(level, val):
    return tag('h%s' % level, val)

def label(val):
    return '<a name="' + val + '" />'

def link_to_label(link, val):
    return '<a href="' + link + '" >' + val + '</a>'

def build_html(dic, command, link_prex, loc='en_US', indent=2):
    print '<ul>'
    for cmd, help in dic.items():
        print tag('li', link_to_label('#'+ link_prex + cmd, cmd))
    print '</ul>'
        
    for cmd, help in dic.items():
        print label(link_prex + cmd)
        print h(indent, cmd)
        print help[loc]['brief']
        print h(indent+1, 'Usage')
        if len(help[loc]['subcommands']) == 0:
            print command + ' ' + cmd
        else:
            print command + ' ' + cmd + ' [SUBCOMMAND]'
        print h(indent+1, 'Description')
        print help[loc]['description']
        print h(indent+1, 'Sub Commands')
        if len(help[loc]['subcommands']) == 0:
            print 'No subcommands are available'
        else:
            for subcmd, help in help[loc]['subcommands'].items():
                print h(indent+2, subcmd)
                print help


if __name__ == '__main__':
    main()


