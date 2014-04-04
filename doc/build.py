#!/usr/bin/env python
#coding: utf-8
import os, sys
import subprocess

import yaml
from wasanbon import help
from wasanbon.core.management import application

def check(cmds):
    p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    ret = (p.stdout.read(), p.stderr.read())
    return ret

def get_subcommands():
    ret = check(['wasanbon-admin.py', '-h'])
    y = yaml.load(ret[0][ret[0].find('[subcommands]')+len('[subcommands]'):])
    return y


def main():
    loc = 'ja_JP'
    #loc = 'en_US'
    help_dic = {}
    cmd_help_dic = {}
    admin_subcommands = application.get_subcommand_list('admin')
    for cmd in admin_subcommands:
        if cmd == 'help':
            continue
        help_dic[cmd] = help.get_help_dic('admin', cmd)
    
    admin_index = open('admin_index.html', 'w')
    build_html(help_dic, command='wasanbon-admin.py', loc=loc, link_prex='admin_', stdout=admin_index)

    _subcommands = application.get_subcommand_list('commands')
    for cmd in _subcommands:
        print cmd
        if cmd == 'help':
            continue
        cmd_help_dic[cmd] = help.get_help_dic('commands', cmd)
    
    admin_index = open('command_index.html', 'w')
    build_html(cmd_help_dic, command='mgr.py', link_prex='command_', loc=loc, stdout=admin_index)



def tag(tag, val):
    return '<%s>%s</%s>' % (tag, val, tag)

def h(level, val):
    return tag('h%s' % level, val)

def label(val):
    return '<a name="' + val + '" />'

def link_to_label(link, val):
    return '<a href="' + link + '" >' + val + '</a>'


msg = {
    'cmd_index' : {
        'en_US' : 'Command Index',
        'ja_JP' : u'コマンド一覧',
        },
    'detail' : {
        'en_US' : 'Detail Information',
        'ja_JP' : u'詳細',
        },
    'usage' : {
        'en_US' : 'Usage',
        'ja_JP' : u'使用例' ,
        },
    'description' : {
        'en_US' : 'Description',
        'ja_JP' : u'解説',
        },
    'subcmd' : {
        'en_US' : 'Sub Command',
        'ja_JP' : u'サブコマンド',
        },
    'nosub' : {
        'en_US' : 'No subcommand is available',
        'ja_JP' : u'サブコマンドはありません',
        },
}
    
def build_html(dic, command, link_prex, stdout=sys.stdout, loc='en_US', indent=1):
    def stdout_write(val):
        stdout.write(val.encode('utf-8') + '\n')

    stdout_write(label(link_prex + 'command_index'))
    #stdout_write(h(indent, 'Command Index'))
    stdout_write(h(indent, msg['cmd_index'][loc]))

    cmds = dic.keys()
    cmds = sorted(cmds)
    stdout_write('<ul>')
    for cmd in cmds:
        stdout_write(tag('li', link_to_label('#'+ link_prex + cmd, cmd)))
    stdout_write('</ul>')
        
    #stdout_write(h(indent, 'Detail Information'))
    stdout_write(h(indent, msg['detail'][loc]))
    for i, cmd in enumerate(cmds):
        help = dic[cmd]
        if not i == 0:
            stdout_write('<div align="right">')
            stdout_write(link_to_label('#' + link_prex+'command_index', 'Go to top'))
            stdout_write('</div>')
        stdout_write(label(link_prex + cmd))
        stdout_write(h(indent+1, cmd))
        stdout_write('<div class="description">')
        stdout_write(help[loc]['brief'])
        stdout_write('</div>')
        #stdout_write(h(indent+2, 'Usage'))
        stdout_write(h(indent+2, msg['usage'][loc]))
        stdout_write('<pre class="input">')
        if len(help[loc]['subcommands']) == 0:
            stdout_write(' $ ' + command + ' ' + cmd)
        else:
            stdout_write(' $ ' + command + ' ' + cmd + ' ['+msg['subcmd'][loc]+']')
        stdout_write('</pre>')
        #stdout_write(h(indent+2, 'Description'))
        stdout_write(h(indent+2, msg['description'][loc]))
        stdout_write('<div class="description">')
        stdout_write(help[loc]['description'])
        stdout_write('</div>')
        #stdout_write(h(indent+2, 'Sub Commands'))
        stdout_write(h(indent+2, msg['subcmd'][loc]))

        if len(help[loc]['subcommands']) == 0:
            stdout_write('<div class="description">')
            #stdout_write('No subcommands are available')
            stdout_write(msg['nosub'][loc])
            stdout_write('</div>')
        else:
            for subcmd, help in help[loc]['subcommands'].items():
                stdout_write('<div class="description">')
                stdout_write(h(indent+3, subcmd))
                stdout_write('<div class="subdescription">')
                stdout_write(help)
                stdout_write('</div>')
                stdout_write('</div>')


if __name__ == '__main__':
    main()


