#from distutils.core import setup
from setuptools import setup
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
import os
import sys
import subprocess

class osx_install_data(install_data):
    # On MacOS, the platform-specific lib dir is /System/Library/Framework/Python/.../
    # which is wrong. Python 2.5 supplied with MacOS 10.5 has an Apple-specific fix
    # for this in distutils.command.install_data#306. It fixes install_lib but not
    # install_data, which is why we roll our own install_data class.

    def finalize_options(self):
        # By the time finalize_options is called, install.install_lib is set to the
        # fixed directory, so we set the installdir to install_lib. The
        # install_data class uses ('install_data', 'install_dir') instead.
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        install_data.finalize_options(self)

if sys.platform == "darwin":
    cmdclasses = {'install_data': osx_install_data}
else:
    cmdclasses = {'install_data': install_data}

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils not to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
wasanbon_dir = 'wasanbon'

for dirpath, dirnames, filenames in os.walk(wasanbon_dir):
    # Ignore dirnames that start with '.'
    #for i, dirname in enumerate(dirnames):
    #    if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append((dirpath.replace('\\', '/'), [os.path.join(dirpath, f).replace('\\', '/') for f in filenames]))

# Small hack for working with bdist_wininst.
# See http://mail.python.org/pipermail/distutils-sig/2004-August/004134.html
if len(sys.argv) > 1 and sys.argv[1] == 'bdist_wininst':
    for file_info in data_files:
        file_info[0] = '\\PURELIB\\%s' % file_info[0]

# Dynamically calculate the version based on django.VERSION.
def _get_version():
    f = open('wasanbon/__init__.py', 'r')
    for line in f:
        if line.startswith('_version'):
            tokens = [t.strip() for t in line.split(" ")]
            if tokens[1] == '=':
                return tokens[2][1:-1]
    sys.stdout.write('Invalid File wasanbon/__init__.py\n')
    raise Exception('Invalid File wasanbon/__init__.py\n')
version = _get_version()
name = "wasanbon"
short_description = '`wasanbon` is a framework for Robotic Software Development with Robotic Technology Middleware (RT-middleware).'

long_description = """\
`wasanbon` is a framework for Robotic Software Developers with Robotic Technology Middleware (RT-middleware).

Robotic Technology Middleware is a standard for Robotic Softwares. In RTM, each software element (like actuator, sensor, algorithm, and so on) is regarded as Robotic Technology Component (RTC). Using RTM, developers can create their robot software with constructing of those software components. 

Each RTC has ports as data-trasnporting endpoints, and a statemachine. To construct RT-system, connection between ports, and state activation is indispensable. To launch multiple RTCs also disturbs developers. `wasanbon` automates multiple RTC development in some aspects. 


Requirements
------------
* Python 2.7

Features
--------
* Repository and Package Management
* Semi-automated Build in Command Line
* Automatical Launch Configuration
* Automatic Launch, Configuration, Connection, and Activation of the RT-System


Setup
-----
::

   $ easy_install wasanbon

History
-------
1.0.0b (2015-7-30)
~~~~~~~~~~~~~~~~~~
* first release

"""

scripts = ['wasanbon/bin/wasanbon-admin.py']
if sys.platform == 'win32':
    scripts.append('wasanbon/bin/wasanbon-cd.bat')

setup(
    name = name,
    version = version,
    url = 'http://www.sugarsweetrobotics.com/',
    author = 'ysuga',
    author_email = 'ysuga@ysuga.net',
    description = 'Development Framework for Robotics Technology Middleware (RTM)',
    download_url = 'https://github.com/sugarsweetrobotics/wasanbon.git',
    packages = packages,
    cmdclass = cmdclasses,
    data_files = data_files,
    scripts = scripts,
    license = 'GPLv3',
    install_requires = open('requirements.txt').read().splitlines(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        #'Framework :: wasanbon',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Desktop Environment',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development',
   ],
)

