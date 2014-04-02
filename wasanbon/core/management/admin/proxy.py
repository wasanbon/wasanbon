# coding: utf-8
"""
en_US :
 brief : |
  This command simply set the proxy setting for git command

 description : |
  This command simply set the proxy setting for git command

 subcommands: []

ja_JP :
 brief : |
  gitコマンドのプロキシサーバ設定

 description : |
  gitコマンドのプロキシサーバ設定をします．
  wasanbon-admin.py proxy YOUR_PROXY_SERVER
  設定を削除する場合は，
  wasanbon-admin.py proxy

 subcommands: []
"""


import wasanbon
from wasanbon import util

def alternative(argv=None):
    return []

def execute_with_argv(argv, verbose=False, clean=False):
    if len(argv) >= 3:
        host, port = argv[2].split(':')
        util.set_proxy(host, port, verbose=True)
        return
    else:
        util.omit_proxy(verbose=True)
        return

