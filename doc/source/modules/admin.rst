===================================
Administration Modules
===================================

Binder Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.binder_plugin.Plugin
    :members:


Builder Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.builder_plugin.Plugin
    :members:


Eclipse Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.eclipse_plugin.Plugin
    :members:
    :exclude-members: launch_eclipse


Editor Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.editor_plugin.Plugin
    :members:


Environment Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.environment_plugin.Plugin
    :members:
    :exclude-members: getIDE, path, setting_path


Example Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.example_plugin.Plugin
    :members:
    :exclude-members: show, echo


Git Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.git_plugin.Plugin
    :members:


Github Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.github_plugin.Plugin


IDL Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.idl_plugin.Plugin
    :members:
    :exclude-members: forEachIDL


IDL Compliler Plugin
======================
.. autoclass:: wasanbon.core.plugins.admin.idlcompiler_plugin.Plugin
    :members:


Make Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.make_plugin.Plugin
    :members: __call__


Nameserver Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.nameserver_plugin.Plugin
    :members:
    :exclude-members: get_nameservers_from_package, get_running_nss_from_pidfile, is_running, launch


Package Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.package_plugin.Plugin
    :members:


Repository Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.repository_plugin.Plugin
    :members:
    :exclude-members: clone_package


RTC Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.rtc_plugin.Plugin
    :members:


RTC Conf Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.rtcconf_plugin.Plugin
    :members:


RTC Profile Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.rtcprofile_plugin.Plugin
    :members:


Self Update Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.selfupdate_plugin.Plugin
    :members:


System Builder Plugin
======================
.. autoclass:: wasanbon.core.plugins.admin.systembuilder_plugin.Plugin
    :members:


System Editor Plugin
======================
.. autoclass:: wasanbon.core.plugins.admin.systemeditor_plugin.Plugin
    :members:


System Installer Plugin
=========================
.. autoclass:: wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin
    :members:


System Launcher Plugin
========================
.. autoclass:: wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin
    :members:
    :exclude-members: exit_all_rtcs


Test Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.test_plugin.Plugin
    :members: __call__


Version Plugin
====================
.. autoclass:: wasanbon.core.plugins.admin.version_plugin.Plugin
    :members: __call__