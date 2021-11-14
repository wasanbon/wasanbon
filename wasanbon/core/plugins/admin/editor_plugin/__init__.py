import os
import sys
import subprocess
import signal
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest


class Plugin(PluginFunction):
    """ Editor Management Plugin """

    def __init__(self):
        # PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    def get_editor_path(self):
        import yaml
        return admin.environment.path['emacs']

    def edit_rtc(self, rtc, verbose=False):
        editenv = os.environ.copy()
        if not 'HOME' in list(editenv.keys()):
            editenv['HOME'] = wasanbon.get_home_path()
        cmd = [self.get_editor_path()]
        if len(cmd[0]) == 0:
            sys.stdout.write('# Error. Editor can not be found.\n')
            return -1
        cmd = cmd + ['-nw']
        srcs = find_rtc_srcs(rtc.rtcprofile)
        cmd = cmd + srcs  # rtc_obj.packageprofile.getSourceFiles()
        if verbose:
            sys.stdout.write('# Edit RTC command=%s\n' % cmd)
        signal.signal(signal.SIGINT, signal_action)
        subprocess.call(cmd, env=editenv)
        pass


def signal_action(num, frame):
    pass


def find_rtc_srcs(rtcp):
    from wasanbon import util
    [path, _] = os.path.split(rtcp.filename)
    if rtcp.language.kind == 'Python':
        return util.search_file(path, rtcp.basicInfo.name + '.py')
    elif rtcp.language.kind == 'Java':
        return util.search_file(path, rtcp.basicInfo.name + 'Impl.java')
    elif rtcp.language.kind == 'C++':
        hdrs = util.search_file(path, rtcp.basicInfo.name + '.h')
        srcs = util.search_file(path, rtcp.basicInfo.name + '.cpp')
        return hdrs + srcs
