#coding: utf-8
"""
en_US:
 brief : |
  Repository Setting Command for wasanbon environment.
 description : |
  This command can setup/update/edit/install repository from internet.
  You must call repository setup command to start wasanbon repository control.
  This command will download default wasanbon_repositories files into your
  RTM_HOME directory. See $HOME/rtm/repositories/sugarsweetrobotics/wasanbon_repositories.
  In the repository directory, you can find two directories, rtcs and packages.
  Both directory can include yaml file that contains repository information of RTC and Package.
 subcommands :
  status : |
   Check Repository Status. This command allows -l option to see more information.
  setup  : |
   Download default repository from www into $RTM_HOME/repositories.
  install : |
   Download specific repository from url.
   ex.,  $ wasanbon-admin.py repository install YOUR_OWN_REPOSITORY_URL
  update : |
   Update repositories.
  create : |
   Create your own repository. You will need to input your information. This will be interactive sequence.
   To use this command, just type, $ wasanbon-admin.py repository create 
  commit : |
   If you add/del your RTC repository information in your own repository, 
   you can commit the changes into your git repository by using this command.
   ex., wasanbon-admin.py repository commit "YOUR_COMMENT"
  push : |
   If your repositoy has additional commit, you can push the commits to upstream server.
   ex., wasanbon-admin.py repository push
  edit : |
   You can manually change your own repository files by this command.
   ex., wasanbon-admin.py repository edit.

ja_JP:
 brief : |
  リポジトリの設定を行います．

 description : |
  このコマンドは，リポジトリの設定，アップデート，編集やインポートを行います．
  repository setupコマンドでは，デフォルトリポジトリのダウンロードとセットアップを行います．
  これにより， $HOME/rtm/repositories/sugarsweetrobotics/wasanbon_repositories.gitにリポジトリが保存されます．
  リポジトリ内には，rtcsとpackagesというディレクトリが作成され，その中のyamlファイルにリポジトリ情報が記入されています．
  repository create独自のリポジトリを作成します．
  repository installでは，リポジトリのインポートを行います．
  repository statusでは，リポジトリの状態を表示できます．
  repository updateでは，リポジトリを最新の状態に更新します．
 subcommands :
  status : |
   リポジトリの状態を表示します．より詳しい情報を得るためには-lオプションを付けます．
  setup  : |
   デフォルトのリポジトリを$HOME/rtm/repositoriesにダウンロードします．
  install : |
   外部のリポジトリをダウンロードします．
   ex.,  $ wasanbon-admin.py repository install YOUR_OWN_REPOSITORY_URL
  update : |
   リポジトリを更新します．
  create : |
   独自のリポジトリを作成します．
   ex., $ wasanbon-admin.py repository create 
  commit : |
   RTCのリポジトリの編集情報をコミットします．
   ex., wasanbon-admin.py repository commit "YOUR_COMMENT"
  push : |
   独自のリポジトリの更新情報をサーバーにアップロードします．
   ex., wasanbon-admin.py repository push
  edit : |
   独自のリポジトリを編集します．
   ex., wasanbon-admin.py repository edit.
"""

import sys, os, yaml, getpass, types, optparse, traceback
import wasanbon
from wasanbon.core import repositories
#from wasanbon.core import package as pack
from wasanbon.util import editor, git

def get_repo_name(path):
    return os.path.basename(os.path.split(path)[0])

def alternative(argv=None):
    repolist_cmd = ['inspect']
    all_cmd =  ['setup', 'status', 'update', 'install', 'create', 'edit', 'commit', 'push'] + repolist_cmd
    if len(argv) >= 3:
        if argv[2] in repolist_cmd:
            from wasanbon.core import package as pack
            repos = pack.get_repositories()
            return [repo.name for repo in repos]
    return all_cmd

def execute_with_argv(argv, force=False, verbose=False, clean=False):
    wasanbon.arg_check(argv, 3)
    usage = "wasanbon-admin.py repository [subcommand] ...\n"
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    parser.add_option('-l', '--long', help='show status in long format', action='store_true', default=False, dest='long_flag')
    parser.add_option('-s', '--service', help='set upstream service',  default='github', metavar='SERVICE', dest='service')

    try:
        options, argv = parser.parse_args(argv[:])
    except:
        traceback.print_exc()
        return
        
    longformat = options.long_flag
    service_name = options.service
          
    if argv[2] == 'setup':
        sys.stdout.write(' - Downloading Repositories.\n')
        if not repositories.download_repositories(verbose=True):
            sys.stdout.write(' - Downloading Failed.\n')

    elif argv[2] == 'update':
        __import__('wasanbon.core.package')
        pack = sys.modules['wasanbon.core.package']
        pack.update_repositories(verbose=verbose)

    elif argv[2] == 'create':
        sys.stdout.write(' - Input %s User Name:' % options.service)
        user, passwd = wasanbon.user_pass()
        sys.stdout.write(' - Creating wasanbon_repositories in your %s\n' % service_name)
        repositories.create_local_repository(user, passwd, verbose=verbose, service=service_name)

    elif argv[2] == 'status':
        #sys.stdout.write(' - Checking Repositories.\n')
        paths = repositories.parse_rtc_repo_dir()

        if len(paths) == 0:
            sys.stdout.write(' @ No repository is downloaded. Do wasanbon-admin.py repository setup\n')
            return
        
        for path in paths:
            owner = False
            owner_name = os.path.basename(os.path.dirname(path))
            mark = '-'
            if owner_name.endswith(repositories.owner_sign):
                owner_name = owner_name[:-len(repositories.owner_sign)]
                owner = True
            sys.stdout.write('  %s/%s :\n' 
                             % (owner_name, os.path.basename(path)))
            sys.stdout.write('    owner: %s\n' % (owner))
            rtcs_dir = os.path.join(path, 'rtcs')
            if os.path.isdir(rtcs_dir):
                sys.stdout.write('    rtcs : \n')
                for file in os.listdir(rtcs_dir):
                    if file.endswith('.yaml'):
                        if not longformat:
                            sys.stdout.write('      - %s\n' % (file))
                        else:
                            #sys.stdout.write('      %s :\n' % (file))
                            y = yaml.load(open(os.path.join(rtcs_dir, file), 'r'))
                            if type(y) == types.DictType:
                                keys = y.keys()
                                keys.sort()
                                for key in keys:
                                    sys.stdout.write('        ' + key + ':\n')
                                    sys.stdout.write('          ' + 'description : "' + y[key]['description'] + '"\n')
            packs_dir = os.path.join(path, 'packages')
            if os.path.isdir(packs_dir):
                sys.stdout.write('    packages : \n')
                for file in os.listdir(packs_dir):
                    if file.endswith('.yaml'):
                        if not longformat:
                            sys.stdout.write('      - %s\n' % (file))
                        else:
                            #sys.stdout.write('      %s :\n' % (file))
                            y = yaml.load(open(os.path.join(packs_dir, file), 'r'))
                            if type(y) == types.DictType:
                                keys = y.keys()
                                keys.sort()
                                for key in keys:
                                    sys.stdout.write('        ' + key + ':\n')
                                    sys.stdout.write('          ' + 'description : "' + y[key]['description'] + '"\n')

    elif argv[2] == 'inspect':
        wasanbon.arg_check(argv, 4)
        from wasanbon.core import package
        repo = package.get_repository(argv[3])
        sys.stdout.write('Repository:\n')
        sys.stdout.write('  name : %s\n' % repo.name)
        sys.stdout.write('  description  : %s\n' % repo.description)
        sys.stdout.write('  url  : %s\n' % repo.url)
        
    elif argv[2] == 'install':
        if len(argv) == 3:
            sys.stdout.write(' @ Need more argument. See help.\n')
        else:
            __import__('wasanbon.core.package')
            pack = sys.modules['wasanbon.core.package']
            sys.stdout.write(' @ Cloning Package Repositories\n')
            pack.download_repositories(verbose=verbose, url=argv[3])


    elif argv[2] == 'commit':
        wasanbon.arg_check(argv, 4)
        paths = repositories.parse_rtc_repo_dir()
        for path in paths:
            owner_name = os.path.basename(os.path.dirname(path))
            if owner_name.endswith(repositories.owner_sign):
                git.git_command(['commit', '-a', '-m', argv[3]], path=path, verbose=verbose)
                return

    elif argv[2] == 'push':
        paths = repositories.parse_rtc_repo_dir()
        for path in paths:
            owner_name = os.path.basename(os.path.dirname(path))
            if owner_name.endswith(repositories.owner_sign):
                git.git_command(['push'], path=path, verbose=verbose)
                return

    elif argv[2] == 'edit':
        paths = repositories.parse_rtc_repo_dir()
        for path in paths:
            owner_name = os.path.basename(os.path.dirname(path))
            if owner_name.endswith(repositories.owner_sign):
                editor.edit_dirs([os.path.join(path, 'rtcs'), os.path.join(path, 'packages')])
                return

            
