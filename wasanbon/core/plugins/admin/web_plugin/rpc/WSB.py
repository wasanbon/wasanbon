
import os, subprocess, yaml, types, time, sys
import wasanbon
from plugin import *


def getRtcRepositoryList(pkg):
    try:
        dir = __check_output('package', 'directory', pkg).strip()
    except:
        return ""

    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['repository', 'list', '-l'] 
    strval = ""
    try:
        stdout = __check_mgr_output(*sub)
        strval = stdout
    except:
        pass
    os.chdir(cwd)
    return strval
   

def getRepositoryRTC(rtc):
    stdout = __check_output('repository', 'rtc', rtc)
    return yaml.load(stdout)


    
def getRepositories():
    stdout = __check_output('repository', 'status', '-l')
    return yaml.load(stdout)

def getRunningPackages():
    stdout = __check_output('package', 'list', '-l', '-r')
    return stdout #yaml.load(stdout.read())

def getPackageAlternative(pkg, sub):

    dir = __check_output('package', 'directory', pkg).strip()

    cwd = os.getcwd()
    os.chdir(dir)
    try:
        sub = ['-a'] 
        stdout = __check_mgr_output(*sub)
        #str = stdout.read().split()
        str = stdout.split()
    except:
        str = ""

    os.chdir(cwd)
    return str


def getRTCLongList(pkg):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'list', '-l'] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    d = yaml.load(stdout.strip())
    return d

def getRTCProfile(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtcprofile', 'dump', rtc] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    return stdout.strip()
    #d = yaml.load(str)

    
def getSystemList(pkg):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'list', '-l'] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    return stdout.strip()
    #d = yaml.load(str)
    #return d

def getRTSProfile(pkg, filename):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'dump', '-f', filename] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    return stdout.strip()


def getPackageRTC(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'profile', rtc] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    d = yaml.load(stdout.strip())
    return d

def runDefaultSystem(pkg):
    return -1

def terminateSystem(pkg):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'terminate'] 
    stdout = __check_mgr_output(*sub)
    os.chdir(cwd)
    #str = stdout.read()
    str = stdout.strip()
    start_time = time.time()
    timeout = 15
    while True:
        running = getRunningPackages()
        print 'Running Packages are ', running
        if running:
            if pkg in running:
                sys.stdout.write(' pkg(%s) is still running\n' % pkg)
                continue
            else:
                sys.stdout.write(' pkg(%s) stopped\n' % pkg)
                return 0
        else:
            sys.stdout.write(' No pkgs are running.\n')
            return 0
        diff_time = time.time() - start_time
        if diff_time > timeout:
            return -2
    return -1
    



def getRTCConfList(pkg):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtcconf', 'show', '-l']
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data
    
def updateSystemFile(pkg, filename, content):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'cat', '-f', filename, content]
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data

def updateRTCProfile(pkg, rtc, content):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    filename = os.path.join(dir, 'temp_' + rtc + '_RTC.xml')
    if os.path.isfile(filename):
        os.remove(filename)
    f = open(filename, 'w')
    f.write(content)
    f.close()
    #sub = ['rtcprofile', 'cat', rtc, content]
    sub = ['rtcprofile', 'cat', rtc, '-i', filename]
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    print std_out_data
    return std_out_data

def syncRTCProfile(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['rtc', 'update_profile', rtc]
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return 'Success'
    
def copySystem(pkg, src, dst):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'copy', src, dst, '-f']
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data

def deleteSystem(pkg, filename):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['system', 'delete', filename, '-f']
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data

def pullRTCRepository(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['repository', 'pull', rtc, '-v']
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data.strip()

def pushRTCRepository(pkg, rtc):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['repository', 'push', rtc, '-v']
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data.strip()

def commitRTCRepository(pkg, rtc, comment):
    dir = __check_output('package', 'directory', pkg).strip()
    cwd = os.getcwd()
    os.chdir(dir)
    sub = ['repository', 'commit', rtc, comment]
    p = __mgr_call(*sub)
    std_out_data, std_err_data = p.communicate()
    os.chdir(cwd)
    return std_out_data.strip()


def sendCode(code):
    code_dir = 'codes'
    if not os.path.isdir(code_dir):
        os.mkdir(code_dir)
    codeName = 'code' + wasanbon.timestampstr() + '.py'
    fileName = os.path.join(code_dir, codeName)
    f = open(fileName, 'w')
    f.write(code)
    f.close()
    return fileName

def startCode(filename):
    args = {}
    args['env'] = os.environ.copy()
    #args['preexec_fn'] = None if sys.platform == 'win32' else disable_sig
    args['stdout'] = subprocess.PIPE
    args['stdin'] = subprocess.PIPE
    if sys.platform == 'win32':
        args['creationflags'] = 512
    if sys.platform == 'win32':
        for path in sys.path:
            if os.path.isfile(os.path.join(path, 'python.exe')):
                exe = os.path.join(path, 'python.exe')
                cmd = [exe, filename]
                break
    else:
        cmd = ['python', filename]
    p = subprocess.Popen(cmd, **args)
    return p.pid
    
