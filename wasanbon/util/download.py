import os, sys
import urllib

class DownloadReport(object):
    def __init__(self, verbose=True):
        self.verbose
        pass

    def __call__(self, read_blocks, block_size, total_bytes):
        if not self.verbose:
            return
        end = read_blocks * block_size / float(total_bytes) * 100.0
        if end > 100.0:
            end = 100.0
        sys.stdout.write('\r - Progress %3.2f [percent] ended' % end)
        sys.stdout.flush()

def download(url, dist="", force=False, verbose=False):

    if len(dist) == 0:
        dist = os.path.basename(url)
    if force and os.path.isfile(dist):
        os.remove(dist)
    if not os.path.isfile(dist):
        if os.path.isfile(dist + '.part'):
            os.remove(dist+'.part')
        if verbose:
            sys.stdout.write("Downloading from URL: %s\n" % url)
        urllib.urlretrieve(url, dist+'.part', DownloadReport(verbose=verbose))
        os.rename(dist+'.part', dist)
        if verobse:
            sys.stdout.write("Saved in Directory  :%s\n" % dist)
    pass

