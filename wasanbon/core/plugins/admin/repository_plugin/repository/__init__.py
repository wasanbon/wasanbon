import os, sys

plugin_obj = None

def clone_package(package_repo, path=None, verbose=False):
    if verbose: sys.stdout.write('# Cloning package %s\n' % package_repo)

    if path is None:
        path = package_repo.basename
    url = package_repo.url

    import wasanbon
    #package = wasanbon.plugins.admin.package.package
    package = plugin_obj.admin.package.package
    try:
        p = package.get_package(path, verbose=verbose)
        raise wasanbon.PackageAlreadyExistsException()
    except:
        pass

    #import wasanbon
    #wasanbon.plugins.admin.git.
    git = plugin_obj.admin.git.git
    git.git_command(['clone', url, path], verbose=verbose)
    
    #import package
    package.create_package(path, verbose=verbose, force_create=True, overwrite=False)
    pack = package.get_package(path, verbose=verbose)
    package.validate_package(pack, verbose=verbose, autofix=True, ext_only=True)

    current_dir = os.getcwd()
    try:
        os.chdir(pack.get_rtcpath())

        repos = get_rtc_repositories_from_package(pack, verbose=verbose)
        for repo in repos:
            clone_rtc(repo, verbose=verbose)
            pass
    except Exception, ex:
        raise ex
    finally:
        os.chdir(current_dir)


def clone_rtc(rtc_repo, verbose=False):
    import wasanbon
    #git = wasanbon.plugins.admin.git.git
    git = plugin_obj.admin.git.git
    git.git_command(['clone', rtc_repo.url, rtc_repo.name], verbose=verbose)

def get_rtc_repositories_from_package(package_obj, verbose=False):
    if verbose: sys.stdout.write('# Loading Repository File from package(%s)\n' % (package_obj.name))
    repos = []
    import wasanbon
    import yaml
    dict_ = yaml.load(open(package_obj.rtc_repository_file, 'r'))
    if dict is not None:
        #binder = wasanbon.plugins.admin.binder.binder
        binder = plugin_obj.admin.binder.binder
        for name, value in dict_.items():

            if 'git' in value.keys():
                typ = 'git'

            if verbose: sys.stdout.write('## Loading Repository (name=%s, url=%s)\n'%(name, value[typ]))

            repo = binder.Repository(name=name, type=typ, url=value[typ], platform=wasanbon.platform(), description=value['description'])
            repos.append(repo)
        pass

    return repos
