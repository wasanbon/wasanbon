import sys
import wasanbon
import wasanbon.core.package as pack


def alternative():
    repos = pack.get_repositories()
    return [repo.name for repo in repos]

def execute_with_argv(args, verbose):
    wasanbon.arg_check(args,3)
    sys.stdout.write(' @ Cloning Package from Repository %s\n' % args[2])
    repo = pack.get_repository(args[2], verbose=verbose)
    _package = repo.clone(verbose=verbose)
