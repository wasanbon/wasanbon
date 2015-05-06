import os


plugin_obj = None

class RTCPackage(object):
    def __init__(self, path, verbose=False):
        self._path = path
        self._rtcprofile_path = os.path.join(path, 'RTC.xml')
        import wasanbon
        if not os.path.isfile(self._rtcprofile_path):
            raise wasanbon.RTCProfileNotFoundException()

        self._rtcprofile = None

    @property
    def path(self):
        return self._path


    @property
    def rtcprofile(self):
        if self._rtcprofile is None:
            #rtcprofile = plugin_obj.admin.rtcprofile.rtcprofile
            from __init__ import admin
            rtcprofile = admin.rtcprofile.rtcprofile
            self._rtcprofile = rtcprofile.RTCProfile(self._rtcprofile_path)
        return self._rtcprofile
    


def get_rtcs_from_package(package, verbose=False):
    import wasanbon
    rtcs = []

    for rtc_dir in os.listdir(package.get_rtcpath()):
        rtc_fullpath = os.path.join(package.get_rtcpath(), rtc_dir)
        if not os.path.isdir(rtc_fullpath):
            continue
        try:
            rtc = RTCPackage(rtc_fullpath, verbose=verbose)
            rtcs.append(rtc)
        except wasanbon.RTCProfileNotFoundException, ex:
            pass
    return rtcs
