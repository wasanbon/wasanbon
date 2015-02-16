import os


def clone_package(package_repo, verbose=False, target_path=None):
    print 'clone package %s' % package_repo
    if target_path is None:
        target_path = package_repo.basename
    import wasanbon
    wasanbon.plugins.admin.git.git.git_command(['clone', package_repo.url, target_path], verbose=verbose)
    
    pass
