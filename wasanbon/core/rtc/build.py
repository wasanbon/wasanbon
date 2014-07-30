import sys, os, shutil, subprocess, platform
import xml.etree.ElementTree as et

import wasanbon


def build_rtc_cpp(rtcp, verbose=False):
    rtc_name = rtcp.basicInfo.name
    rtc_dir, rtc_xml = os.path.split(rtcp.filename)
    build_dir = os.path.join(rtc_dir, 'build-%s' % sys.platform)

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
        arg = ['-G', wasanbon.IDE]

    current_dir = os.getcwd()
    os.chdir(rtc_dir)
    if not os.path.isdir(build_dir):
        if verbose:
            print ' - Creating build directory : %s' % build_dir
        os.makedirs(build_dir)
    os.chdir(build_dir)
    cmd = [wasanbon.setting()['local']['cmake'], '..'] + arg
    stdout = None if verbose else subprocess.PIPE
    stderr = None if verbose else subprocess.PIPE
    if verbose:
        sys.stdout.write(' - Cross Platform Make (CMAKE)\n');
    p = subprocess.Popen(cmd, env=os.environ, stdout=stdout, stderr=stderr)
    ret = p.wait()
    if ret != 0:
        sys.stdout.write(' - Failed.\n')
        if verbose:
            return (False, None)
        return (False, p.stderr.read())

    if sys.platform == 'win32':
        sln = '%s.sln' % rtcp.basicInfo.name
        if sln in os.listdir(os.getcwd()):
            sys.stdout.write(' - Visual C++ Solution File is successfully generated.\n')
            cmd = [wasanbon.setting()['local']['msbuild'], sln, '/p:Configuration=Release', '/p:Platform=Win32']
            #stdout = None if verbose else subprocess.PIPE
            stdout = None # In windows msbuild always must be launched in verbose mode.
            stderr = None
            sys.stdout.write(' - msbuild %s %s %s\n' % (os.path.basename(sln), '/p:Configuration=Release', '/p:Platform=Win32'))
            p = subprocess.Popen(cmd, stdout=stdout, stderr=stderr)
            p.wait()
            if not verbose:
                errmsg = p.stderr.read()
            else:
                errmsg = ""
            return ((errmsg.find('error') < 0 and errmsg.find('Error') < 0), errmsg)

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
            p.wait()
            if not verbose:
                errmsg = p.stderr.read()
            else:
                errmsg = ""
            return ((errmsg.find('error') < 0 and errmsg.find('Error') < 0), errmsg)

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
            p.wait()
            if not verbose:
                errmsg = p.stderr.read()
            else:
                errmsg = ""
            return ((errmsg.find('error') < 0 and errmsg.find('Error') < 0), errmsg)

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
    current_dir = os.getcwd()
    os.chdir(rtc_dir)
    rtm_java_classpath = os.path.join(wasanbon.rtm_home(), 'jar')           

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
    build_script = os.path.join(rtc_dir, 'build_' + rtc_name + ".xml")
    if os.path.isfile(build_script):
        for target in et.parse(build_script).findall('target'):
            if target.attrib['name'] == 'idlcompile':
                need_idlcompile = True
                #arg = et.parse(build_script).findall('arg')
                arg = target.getiterator('arg')[0].attrib['line'].split()[-1][1:-1]
    if need_idlcompile:
        if verbose:
            sys.stdout.write(' -- IDLCOMPILE\n')
        idlc = os.path.join(os.path.split(wasanbon.setting()['local']['javac'])[0], 'idlj')
        cmd = [idlc, '-td', src_dir, '-fall', arg]
        print cmd
        myenv = os.environ
        myenv['LANG'] = 'C'
        subprocess.call(cmd, env=myenv)
            

    java_env = os.environ.copy()
    if not "CLASSPATH" in java_env.keys():
        java_env["CLASSPATH"]='.'
    if sys.platform == 'win32':
        sep = ';'
    else:
        sep = ':'
    for jarfile in os.listdir(rtm_java_classpath):
        java_env["CLASSPATH"]=java_env["CLASSPATH"] + sep + os.path.join(rtm_java_classpath, jarfile)
        if verbose:
            java_env['JAVA_TOOL_OPTIONS']='-Dfile.encoding=UTF-8'
    if os.path.isdir( os.path.join(rtc_dir, 'jar') ):
        
        for jarfile in os.listdir(os.path.join(rtc_dir, 'jar')):
            java_env["CLASSPATH"]=java_env["CLASSPATH"] + sep + os.path.join(rtc_dir, 'jar', jarfile)        
                                  
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


    cmd = [wasanbon.setting()['local']['javac'], 
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
        return (False,  p.stderr.read())

    clsfiles = []
    for root, dirs, files in os.walk(cls_dir):
        for f in files:
            if f.endswith('.class'):
                if verbose:
                    print ' --- cls:', os.path.join(root, f)[len(cls_dir)+1:]
                clsfiles.append(os.path.join(root, f)[len(cls_dir)+1:])
    curdir = os.getcwd()
    os.chdir(cls_dir)
    jarcmd = os.path.join(os.path.split(wasanbon.setting()['local']['javac'])[0], 'jar')
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

