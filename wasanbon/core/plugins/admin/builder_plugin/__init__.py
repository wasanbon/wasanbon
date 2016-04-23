import sys, os, shutil, subprocess, platform
import xml.etree.ElementTree as et


import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):
    """ RT-Component Compile/Build management """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.rtc']


    def build_rtc(self, rtcprofile, verbose=False):
        curdir = os.getcwd()
        if rtcprofile.language.kind == 'C++':
            retval = build_rtc_cpp(rtcprofile, verbose=verbose)
        elif rtcprofile.language.kind == 'Java':
            retval = build_rtc_java(rtcprofile, verbose=verbose)
        elif rtcprofile.language.kind == 'Python':
            retval = build_rtc_python(rtcprofile, verbose=verbose)
        os.chdir(curdir)
        return retval

    def clean_rtc(self, rtcprofile, verbose=False):
        curdir = os.getcwd()
        if rtcprofile.language.kind == 'C++':
            retval = clean_rtc_cpp(rtcprofile, verbose=verbose)
        if rtcprofile.language.kind == 'Java':
            retval = clean_rtc_java(rtcprofile, verbose=verbose)
        if rtcprofile.language.kind == 'Python':
            retval = clean_rtc_python(rtcprofile, verbose=verbose)
        os.chdir(curdir)
        return retval

def getIDE():
    return admin.environment.getIDE()


def build_rtc_cpp(rtcp, verbose=False):
    if verbose: sys.stdout.write('## Building C++ RT-component source\n')
    rtc_name = rtcp.basicInfo.name
    rtc_dir, rtc_xml = os.path.split(rtcp.filename)
    build_dir = os.path.join(rtc_dir, 'build-%s' % sys.platform)
    cmake_path = admin.environment.path['cmake']
    if sys.platform == 'win32':
        msbuild_path = admin.environment.path['msbuild']

    arg = []
    if sys.platform == 'linux2' and platform.architecture()[0] == '64bit':
        if verbose:
            print ' - Detected 64bit linux2. modifying PKG_CONFIG_PATH environ.'
        os.environ['PKG_CONFIG_PATH'] = '/usr/lib64/pkgconfig/:/usr/local/lib64/pkgconfig/'
    elif sys.platform == 'darwin':
        if verbose:
            print ' - Detected Darwin. modifying PKG_CONFIG_PATH environ.'
        os.environ['PKG_CONFIG_PATH'] = '/usr/lib/pkgconfig/:/usr/local/lib/pkgconfig/'
    elif sys.platform == 'win32':
        arg = ['-G', getIDE()]

    current_dir = os.getcwd()
    os.chdir(rtc_dir)
    if not os.path.isdir(build_dir):
        if verbose:
            print ' - Creating build directory : %s' % build_dir
        os.makedirs(build_dir)
    os.chdir(build_dir)
    cmd = [cmake_path, '..'] + arg
    stdout = None if verbose else subprocess.PIPE
    stderr = None if verbose else subprocess.PIPE
    if verbose:
        sys.stdout.write('# Cross Platform Make (CMAKE)\n');
    p = subprocess.Popen(cmd, env=os.environ, stdout=stdout, stderr=stderr)
    std_out = p.communicate()
    ret = p.returncode
    #ret = p.wait()
    if ret != 0:
        sys.stdout.write('# CMake Failed.\n')
        if verbose:
            return (False, None)
        return (False, std_out[0])
    sys.stdout.write('# CMake Success.\n')

    if sys.platform == 'win32':
        sys.stdout.write('# Building in Win32 platform.\n')
        sln = '%s.sln' % rtcp.basicInfo.name
        if sln in os.listdir(os.getcwd()):
            sys.stdout.write('# Visual C++ Solution File is successfully generated.\n')
            cmd = [msbuild_path, sln, '/p:Configuration=Release', '/p:Platform=Win32']
            cmd + ['/clp:ErrorsOnly']
            #stdout = None if verbose else subprocess.PIPE
            #stderr = None if verbose else subprocess.PIPE
            stdout = None # In windows msbuild always must be launched in verbose mode.
            stderr = None
            #stdout = subprocess.PIPE
            sys.stdout.write(' - msbuild %s %s %s\n' % (os.path.basename(sln), '/p:Configuration=Release', '/p:Platform=Win32'))
            env = os.environ
            env['PATH'] = env['PATH'] + ';' + os.path.join(env['OMNI_ROOT'], 'bin', 'x86_win32')
            # print env['PATH']
            p = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, env=env)
            std_out, std_err = p.communicate()
            ret = p.returncode
            errmsg = ""
            if verbose:
                sys.stdout.write('## Return Code = %s\n' % ret)
            else:
                if std_out == None:
                    errmsg = ''
                else:
                    errmsg = std_out
            err_code = (errmsg.find('error') < 0 and errmsg.find('Error') < 0 and ret == 0)
            return (err_code, errmsg)

    elif sys.platform == 'darwin':
        if verbose:
            sys.stdout.write(' - Building with Darwin\n')
        if 'Makefile' in os.listdir(os.getcwd()):
            if verbose:
                sys.stdout.write(' - Makefile is successfully generated.\n')
            cmd = ['make']
            stdout = None if verbose else subprocess.PIPE
            stderr = None if verbose else subprocess.PIPE

            if verbose:
                sys.stdout.write(' - make\n')
            p = subprocess.Popen(cmd, stdout=stdout, stderr=stderr)
            std_out, std_err = p.communicate()
            #p.wait()
            ret = p.returncode
            if verbose:
                sys.stdout.write('## Return Code = %s\n' % ret)
            if not verbose:
                errmsg = std_out
            else:
                errmsg = std_out
            return ((ret == 0), errmsg)

    elif sys.platform == 'linux2':
        if 'Makefile' in os.listdir(os.getcwd()):
            if verbose:
                sys.stdout.write(' - Makefile is successfully generated.\n')
            cmd = ['make']
            stdout = None if verbose else subprocess.PIPE
            stderr = None if verbose else subprocess.PIPE
            if verbose:
                sys.stdout.write(' - make\n')
            p = subprocess.Popen(cmd, stdout=stdout, stderr=stderr)
            std_out, std_err = p.communicate()
            ret = p.returncode
            if verbose:
                sys.stdout.write('## Return Code = %s\n' % ret)

            if not verbose:
                errmsg = std_out
            else:
                errmsg = std_out
            return ((ret == 0), errmsg)
    else:
        sys.stdout.write('# Error. Unknown Platform : %s\n' % sys.platform)
        return -1, 'Unknown Platform (%s)' % sys.platform

def build_rtc_python(rtcp, verbose=False):
    rtc_name = rtcp.basicInfo.name
    rtc_dir, rtc_xml = os.path.split(rtcp.filename)

    current_dir = os.getcwd()
    os.chdir(rtc_dir)

    sys.stdout.write(' - Compiling IDL files')
    if sys.platform == 'darwin' or sys.platform == 'linux2':
        if 'idlcompile.sh' in os.listdir(os.getcwd()):
            cmd = ['sh', 'idlcompile.sh']
            subprocess.call(cmd)
    elif sys.platform == 'win32':
        if 'idlcompile.bat' in os.listdir(os.getcwd()):
            cmd = ['idlcompile.bat']
            subprocess.call(cmd)

    return (True, "")

def build_rtc_java(rtcp, verbose=False):
    rtc_name = rtcp.basicInfo.name
    rtc_dir, rtc_xml = os.path.split(rtcp.filename)
    build_dir = os.path.join(rtc_dir, 'build-%s' % sys.platform)
    src_dir = os.path.join(rtc_dir, 'src')
    cls_dir = os.path.join(build_dir, 'class')
    bin_dir = os.path.join(build_dir, 'bin')
    idl_dir = os.path.join(build_dir, 'idl')
    javac_path = admin.environment.path['javac']
    current_dir = os.getcwd()
    os.chdir(rtc_dir)
    rtm_java_classpath = os.path.join(wasanbon.home_path, 'jar')           

    stdout = None if verbose else subprocess.PIPE
    stderr = None if verbose else subprocess.PIPE

    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)
    if not os.path.isdir(cls_dir):
        os.makedirs(cls_dir)
    if not os.path.isdir(bin_dir):
        os.makedirs(bin_dir)
    if not os.path.isdir(idl_dir):
        os.makedirs(idl_dir)

    need_idlcompile = False
    arg = None
    args = []
    build_script = os.path.join(rtc_dir, 'build_' + rtc_name + ".xml")
    if os.path.isfile(build_script):
        for target in et.parse(build_script).findall('target'):
            if target.attrib['name'] == 'idlcompile':
                need_idlcompile = True
                #arg = et.parse(build_script).findall('arg')
                for a in target.getiterator('arg'):
                    arg = a.attrib['line'].split()[-1][1:-1]
                    args.append(arg)
    if need_idlcompile:
        idlc = os.path.join(os.path.split(javac_path)[0], 'idlj')
        if 'RTM_ROOT' in os.environ.keys():
            rtm_idl_dir = os.path.join(os.environ['RTM_ROOT'], 'rtm', 'idl')
        else:
            rtm_idl_dir = '.'

        for arg in args:
            cmd = [idlc, '-td', src_dir, '-I', rtm_idl_dir, '-I', 'idl', '-fall', arg]

            if verbose: sys.stdout.write(' -- compiling idl with command(%s)\n' % cmd)

            myenv = os.environ
            myenv['LANG'] = 'C'
            subprocess.call(cmd, env=myenv)
            pass
        pass
            

    java_env = os.environ.copy()
    if not "CLASSPATH" in java_env.keys():
        java_env["CLASSPATH"]='.'
    if sys.platform == 'win32':
        sep = ';'
    else:
        sep = ':'
    for jarfile in os.listdir(rtm_java_classpath):
        java_env["CLASSPATH"]=java_env["CLASSPATH"] + sep + os.path.join(rtm_java_classpath, jarfile)
        #if verbose:
        if sys.platform == 'darwin':
            java_env['JAVA_TOOL_OPTIONS']='-Dfile.encoding=UTF-8'
        elif sys.platform == 'win32':
            java_env['JAVA_TOOL_OPTIONS']='-Dfile.encoding=Shift_JIS'
    if os.path.isdir( os.path.join(rtc_dir, 'jar') ):
        
        for jarfile in os.listdir(os.path.join(rtc_dir, 'jar')):
            java_env["CLASSPATH"]=java_env["CLASSPATH"] + sep + os.path.join(rtc_dir, 'jar', jarfile)        

    java_env['LANG'] = 'en'
    java_env['LC_ALL'] = 'en'

    javafiles = []

    # if need_idlcompile:
    #    for root, dirs, files in os.walk(idl_dir):
    #        for f in files:
    #            if f.endswith('.java'):
    #                javafiles.append(os.path.join(root,f))

    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith('.java'):
                javafiles.append(os.path.join(root, f))


    cmd = [javac_path, 
           '-source', '1.7',
           '-target', '1.7',
           '-encoding', 'SJIS',
           '-s', src_dir, '-d', cls_dir]
    for f in javafiles:
        cmd.append(f)
    #print cmd
    if verbose:
        sys.stdout.write(' - build_rtc_java:%s\n' % repr(cmd))
    p = subprocess.Popen(cmd, env=java_env)
    ret = p.wait()

    if ret != 0:
        return (False,  p.stdout.read())

    clsfiles = []
    for root, dirs, files in os.walk(cls_dir):
        for f in files:
            if f.endswith('.class'):
                if verbose:
                    print ' --- cls:', os.path.join(root, f)[len(cls_dir)+1:]
                clsfiles.append(os.path.join(root, f)[len(cls_dir)+1:])
    curdir = os.getcwd()
    os.chdir(cls_dir)
    jarcmd = os.path.join(os.path.split(javac_path)[0], 'jar')
    #cmd = [jarcmd, '-J-Dfile.encoding=UTF-8', 'cfv', os.path.join(bin_dir, rtc_name + '.jar'), '-C ' + os.path.join(build_dir, 'class', '')]
    cmd = [jarcmd,
           #'-J-Dfile.encoding=UTF-8',
           #'cfv', os.path.join(bin_dir, rtc_name + '.jar'), '-C', os.path.join(build_dir, 'class')]
           'cfv', os.path.join(bin_dir, rtc_name + '.jar')]

    #cmd.append('.')
    #cmd.append('*.class')
    for f in clsfiles:
    #    cmd.append(cls_dir)
        cmd.append(f)

    if verbose:
        sys.stdout.write(' - archiving: %s\n' % repr(cmd))


    ret = subprocess.call(cmd, env=java_env, stdout=stdout, stderr=stderr)
    os.chdir(curdir)

    if ret == 0:
        return (True, "")

def clean_rtc_cpp(rtcp, verbose=False):
    rtc_dir, rtc_xml = os.path.split(rtcp.filename)
    build_dir = os.path.join(rtc_dir, 'build-' + sys.platform)
    if os.path.isdir(build_dir):
        if verbose:
            print ' - Removing Building Directory %s' % build_dir
        shutil.rmtree(build_dir, ignore_errors=True )
    for root, dirs, files in os.walk(rtc_dir):
        for file in files:
            if file.endswith('~'):
                fullpath = os.path.join(root, file)
                if fullpath.startswith(os.getcwd()):
                    fullpath = fullpath[len(os.getcwd())+1]
                if verbose:
                    print ' - Removing Emacs backup file %s' % fullpath
                os.remove(os.path.join(root, file))
    return True, None

def clean_rtc_java(rtcp, verbose=False):
    rtc_dir, rtc_xml = os.path.split(rtcp.filename)
    build_dir = os.path.join(rtc_dir, 'build-' + sys.platform)
    if os.path.isdir(build_dir):
        if verbose:
            print ' - Removing Building Directory %s' % build_dir
        shutil.rmtree(build_dir, ignore_errors=True )
    for root, dirs, files in os.walk(rtc_dir):
        for file in files:
            if file.endswith('~'):
                fullpath = os.path.join(root, file)
                if fullpath.startswith(os.getcwd()):
                    fullpath = fullpath[len(os.getcwd())+1]
                if verbose:
                    print ' - Removing Emacs backup file %s' % fullpath
                os.remove(os.path.join(root, file))

    return True, None

def clean_rtc_python(rtcp, verbose=False):
    return True, None
