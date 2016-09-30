
import wasanbon

import os, sys
import xml.etree.ElementTree as etree
import urllib2
import pysftp

_uploadhost = 'ysuga.net'
_host ='http://sugarsweetrobotics.com'
_subdir = '/pub/wasanbon/web/applications/'
_url = _host + _subdir
_dir = '/home/ysuga/www/ssr/www2' + _subdir
_list_page = 'application_list.html'

def test(usr=None, ps=None):
    update_cache(url=_url + _list_page)
    upload(sys.argv[1], usr, ps, _list_page, hostname=_uploadhost, dir=_dir)
    #add_version('hoge', '0.0.2')
    #usr, passwd = wasanbon.user_pass(usr, ps)
    #upload(usr, passwd)

def upload(filepath, user, password, list_filename, hostname, dir, description=""):
    if not os.path.isfile(filepath):
        raise FileNotFoundError()
    filename = os.path.basename(filepath)
    appname, version = filename[:-4].split('-')
    add_version(appname, version, filename=list_filename, description=description)
    usr, psswd = wasanbon.user_pass(user, password)
    upload_list(usr, psswd, filename=list_filename, hostname=hostname, dir=dir)
    upload_file(usr, psswd, filepath, hostname=hostname, dir=dir)
    
def update_cache(url, target=None, verbose=False):
    if verbose: sys.stdout.write('# Update Cache in %s\n' % url)
    if target is None:
        target = os.path.join(wasanbon.get_wasanbon_home(), 'web')
    if not os.path.isdir(target):
        os.mkdir(target)

    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    page_content = response.read()
    
    if verbose: sys.stdout.write('############### Content #################\n')
    if verbose: sys.stdout.write(page_content)
    if verbose: sys.stdout.write('############### Content #################\n')
    target_file = os.path.join(target, _list_page)
    open(target_file, 'w').write(page_content)


def cache_to_dict(target=None):
    if target is None:
        target = os.path.join(wasanbon.get_wasanbon_home(), 'web')

    if not os.path.isdir(target):
        os.mkdir(target)

    target_file = os.path.join(target, _list_page)


    dic = {}
    root =  etree.fromstring(open(target_file, 'r').read())
    body = root.find('body')
    listtop = body.find('ul')
    
    for item in listtop.findall('li'):
        appname = item.text.strip()
        if appname in dic.keys():
            sys.stdout.write(' -- Application (%s) is doubled.\n' % appname)
            return {}

        dic[appname] = {}

        app_version_listtop = item.find('ul')
        for version_item in app_version_listtop.findall('li'):
            a_item = version_item.find('a')
            d_item = version_item.find('span')
            version_text = a_item.text.strip()
            url = a_item.get('href').strip()
            
            dic[appname][version_text] = {'url': url, 'description' : d_item.text.strip() }
            #dic[appname]['description'] = d_item.text.strip()

    return dic


def add_version(appname, version, target=None, filename=None, description=""):
    if not target:
        target = os.path.join(wasanbon.get_wasanbon_home(), 'web')

    if not os.path.isdir(target):
        os.mkdir(target)

    if not filename:
        target_file = os.path.join(target, _list_page)
    else:
        target_file = os.path.join(target, filename)
    target_file_backup = target_file + wasanbon.timestampstr()

    dic = {}
    root =  etree.fromstring(open(target_file, 'r').read())
    body = root.find('body')
    listtop = body.find('ul')

    app_item = None
    for item in listtop.findall('li'):
        appname_ = item.text.strip()
        if appname_ == appname:
            app_item = item
            break

    if app_item is None:
        app_item = etree.Element('li')
        app_item.text = appname

        app_version_listtop = etree.Element('ul')

        app_item.extend([app_version_listtop])
        listtop.extend([app_item])
        

    app_version_listtop = app_item.find('ul')
    for version_item in app_version_listtop.findall('li'):
        a_item = version_item.find('a')
        version_text = a_item.text.strip()
        url = a_item.get('href').strip()
                
        if version_text == version:
            sys.stdout.write('App (%s) Version(%s) is already registered.\n' % (appname, version))
            return 
        pass
            # Can not find version. OKay
    version_item = etree.Element('li')
    filename = appname + '-' + version + '.zip'
    a_item = etree.Element('a', href=filename)
    a_item.text = version
    d_item = etree.Element('span')
    d_item.text = description
    version_item.extend([a_item, d_item])
    app_version_listtop.extend([version_item])
    found = True

    os.rename(target_file, target_file_backup)
    xmlstr = etree.tostring(root)
    open(target_file, 'w').write(xmlstr)


def upload_file(usr, passwd, filepath, hostname, dir):
    with pysftp.Connection(hostname, username=usr, password=passwd) as sftp:
        with sftp.cd(dir):              # temporarily chdir to public
            sftp.put(filepath)  # upload file to public/ on remote
    
def upload_list(usr, passwd, target=None, filename=None, hostname=None, dir=None):
    if not target:
        target = os.path.join(wasanbon.get_wasanbon_home(), 'web')
    if not os.path.isdir(target):
        os.mkdir(target)
    if not filename:
        target_file = os.path.join(target, _list_page)
    else:
        target_file = os.path.join(target, filename)

    upload_file(usr, passwd, target_file, hostname, dir=dir)
    
if __name__ == '__main__':
    test()
