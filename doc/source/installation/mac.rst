====================================
Environment Setup on Mac
====================================
Setup guide for Mac OS10.14.


Install Homebrew
=====================
Hit following command in terminal.

.. code::

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


Install OpenRTM
=====================
1. Get OpenRTM for homebrew from github

.. code::

    git clone https://github.com/openrtm/homebrew-openrtm /usr/local/Homebrew/Library/Taps/openrtm/homebrew-openrtm --origin=origin
    git clone https://github.com/openrtm/homebrew-omniorb /usr/local/Homebrew/Library/Taps/openrtm/homebrew-omniorb --origin=origin

2. Install homebrew-omniorb

.. code::

    brew install openrtm/homebrew-omniorb/omniorb-ssl-py38
    brew link omniorb-ssl-py38
    brew install openrtm/homebrew-omniorb/omniorbpy-py38
    brew link omniorbpy-py38

3. Overwrite ``/usr/local/Homebrew/Library/Taps/openrtm/homebrew-openrtm/openrtm-aist-py38.rb``

* change L.28 to ``sha256 cellar: :any, catalina: "7e751f843aa18db7edcab1574e1379fa6b88332294763842c42a2d0303b9dba7"``
* delete L.26

.. note::

    If ``openrtm-aist-py38`` is installed in ``/usr/local/Cellar/openrtm-aist-py38/1.2.2.reinstall/``,
    please reinstall ``openrtm-aist-py38`` or Link ``/usr/local/Cellar/openrtm-aist-py38/1.2.2.reinstall/`` to ``/usr/local/Cellar/openrtm-aist-py38/1.2.2/``

4. Install OpenRTM(C++)

.. code::

    brew install openrtm/homebrew-openrtm/openrtm-aist-py38
    brew link openrtm-aist-py38

5. Install OpenRTM(Python)

.. code::

    brew install openrtm/homebrew-openrtm/openrtm-aist-python-py38
    brew link openrtm-aist-python-py38

6. Install AdoptOpenJDK

.. code::

    brew tap homebrew/cask-versions
    brew install --cask adoptopenjdk8

7. Install OpenRTM(Java)

.. code::

    brew install openrtm/homebrew-openrtm/openrtm-aist-java

8. Install OpenRTP

.. code::

    brew tap openrtm/openrtm
    brew install openrtp

9. Install RtShell

.. code::

    sudo pip3 install rtshell-aist

10. Install Cmake

.. code::

    brew install cmake

11. Install doxygen

.. code::

    brew install doxygen


Install Other Dependencies
=================================
1. Install Emacs and TortoiseHg

.. code::

    brew install emacs
    brew install tortoisehg

2. Install Hg

.. code::

    sudo pip3 install mercurial

.. note::

    Do not install by brew because it make dependency with Python3.9


Setup Environment
==================================
1. Change zsh to bash

.. code::

    chsh -s /bin/bash

2. To setup environment variables, add following variables in ``~/.bash_profile``

.. code::

    export RTM_ROOT=/usr/local/include/openrtm-1.2
    export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
    export PYTHONPATH=$PYTHONPATH:/usr/local/lib:/usr/local/lib/python3.8/site-packages:/usr/local/lib/python3.8/site-packages/OpenRTM_aist/RTM_IDL:/usr/local/lib/python3.8/site-packages/OpenRTM_aist
    export CMAKE_PREFIX_PATH=/usr/local/lib/openrtm-1.2/cmake:$CMAKE_PREFIX_PATH
    export RTM_JAVA_ROOT=/usr/local/lib/openrtm-1.2/


Next, see :ref:`wasanbon_installation`.
