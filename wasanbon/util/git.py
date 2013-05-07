import wasanbon

def clone_and_setup(url):
    y = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))
    url = setting['common']['git'][key]
    cmd = [y['git_path'], 'clone', url, wasanbon.rtm_temp]
    subprocess.call(command)

    crrdir = os.getcwd()
    os.chdir(os.path.join(rtm_temp, key))
    command = ['python', 'setup.py', 'install', '--record', 'installed_files.txt']
    subprocess.call(command)
    os.chdir(crrdir)

