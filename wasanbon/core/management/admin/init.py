# coding: utf-8
"""
en_US :
 brief : |
  Initialization of wasanbon's environment.

 description : |
  This command must be called first. This will do ...
  1. Install Pip, PyYAML, PyGithub, psutil, and python-bitbucket module if not installed.
  2. Create RTM_HOME directory, where:
    2.1 Create 'rtm' directory in your $HOME.
    2.2 Create 'temp' directory in your $HOME/rtm.
    2.3 Create 'plugins' directory in your $HOME/rtm.
    2.4 Copy 'setting.yaml' file in your $HOME/rtm. This is basic setting file of wasanbon.
  If you need to start wasanbon, you also have to check the dependencies.
  Check wasanbon-admin.py status.
 subcommands: []

ja_JP :
 brief : |
  wasanbonの環境初期化

 description : |
  このコマンドは最初に呼ばれるべきコマンドです．最初に以下の動作をします．
  1. Pip, PyYAML, PyGithub, psutil, and python-bitbucketのPythonモジュールをインストールします
  2. RTM_HOMEディレクトリを作成します．すなわち・・・
    2.1 'rtm'ディレクトリを$HOMEに作成.
    2.2 'temp'ディレクトリを$HOME/rtmに作成
    2.3 'plugins'ディレクトリを$HOME/rtmに作成
    2.4 'setting.yaml'ファイルを$HOME/rtmに作成．これはwasanbonの基本環境情報です．
  このコマンドで環境が整えられた後は，wasanbon-admin.py statusコマンドで依存ライブラリの状態を確認します
 subcommands: []
"""
import sys, traceback
import wasanbon
#from wasanbon.core import platform


def alternative(argv=None):
    return []

def execute_with_argv(args, verbose=False):
    sys.stdout.write(' - Starting wasanbon environment.\n')
    sys.stdout.write(' - Initializing RTM home directory\n')
    __import__('wasanbon.setup')
    setup = sys.modules['wasanbon.setup']

    force = True
    setuptools = setup.try_import_and_install('setuptools', verbose=verbose, force=force)
    pip = setup.try_import_and_install('pip', verbose=verbose, force=force)
    yaml = setup.try_import_and_install('yaml', verbose=verbose, force=force)
    github = setup.try_import_and_install('github', verbose=verbose, force=force)
    psutil = setup.try_import_and_install('psutil', verbose=verbose, force=force)
    requests = setup.try_import_and_install('requests', verbose=verbose, force=force)
    requests_oauth = setup.try_import_and_install('requests_oauthlib', verbose=verbose, force=force)
    bitbucket = setup.try_import_and_install('bitbucket', verbose=verbose, force=force)

    if not all([pip, yaml, github, psutil, bitbucket]):
        sys.stdout.write(' @ Try wasanbon-admin.py init again.\n')
        return False

    __import__('wasanbon.core.platform')
    platform = sys.modules['wasanbon.core.platform']        
    platform.init_rtm_home(verbose=verbose)

    __import__('wasanbon.core.platform.path')
    path = sys.modules['wasanbon.core.platform.path']
    path.init_tools_path(verbose=verbose)
    
    """
    try:
        __import__(pack)
        return sys.modules[pack]
    except ImportError, ex:
        traceback.print_exc()
    """
    return True
