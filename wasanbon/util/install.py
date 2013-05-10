import os, sys
import subprocess


def install(file):
    if file.endswith(".dmg"):
        return install_dmg(file)
    elif file.endswith(".app"):
        return install_app(file)
    elif file.endswith(".egg"):
        cmd = ['sh', file]
    elif file.endswith(".pkg"):
        cmd = ['installer', '-package', file, '-target', '/Volumes/Macintosh HD']
    elif file.endswith(".msi"):
        cmd = ['msiexec', '/i', file]
    elif file.endswith(".exe"):
        cmd = [file]
    else:
        return

    try:
        if sys.platform == 'win32':
            print 'cmd=%s' % cmd
            ret = subprocess.Popen(cmd, env=os.environ)
            ret.wait()
            
        else:
            ret = subprocess.check_output(cmd)
        sys.stdout.write('Installing %s is successful. Message is below\n' % file)
        sys.stdout.write(ret)
    except:
        sys.stdout.write('Installing %s is failed. Maybe this process must have done by super user.\n' % file)


def install_dmg(dmg):
    cmd = ['hdiutil', 'mount', dmg]
    ret = subprocess.check_output(cmd)
    mountedVolume = [x.strip() for x in ret.split('\t') if x.startswith("/Volumes/")]
    if len(mountedVolume) != 1:
        print 'Error mounting %s' % dmg

    for root, dirs, files in os.walk(mountedVolume[0]):
        for dir in dirs:
            install(os.path.join(root, dir)) # .pkg and .app is directory but installable.
        for file in files:
            install(os.path.join(root, file))
    cmd = ['hdiutil', 'unmount', mountedVolume[0]]
    ret = subprocess.check_output(cmd)

def install_app(app):
    if app.endswith('/'):
        app = app[len(app)-1:]

    cmd = ['cp', '-R', app, '/Applications/']
    try:
        ret = subprocess.check_output(cmd)
        print 'Installing %s is successful. Message is below' % app
        print ret
    except:
        print 'Installing %s is failed. Maybe this process must have done by super user.' % app

