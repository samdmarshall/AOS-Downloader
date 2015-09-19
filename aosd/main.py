import sys
import argparse
import readline
import rlcompleter

from .commandparse import InteractiveInput
from .downloader.config import config

from .flags import *

def CheckPassedArgCount(args):
    kDefaultValues = {
        'build': None,
        'diff': None,
        'list': False,
        'package': None,
        'resetcache': False,
        'type': None,
        'buildcache': False,
        'findhash': False,
    }
    # returns the number of arguments that got passed that are not set to default values
    return len(list((item for item in args.keys() if kDefaultValues[item] != args[item])))

def main():
    parser = argparse.ArgumentParser(description='Apple Open Source Package Downloader')
    parser.add_argument(
        '-t',
        '--type',
        help='specify the release type',
        required=False,
        action='store'
    )

    parser.add_argument(
        '-l',
        '--list',
        help='list versions of a package to check out, if no package is specified it lists available packages',
        required=False,
        action='store_true'
    )

    parser.add_argument(
        '-p',
        '--package',
        help='specify the name of a package from a release',
        required=False,
        action='store',
    )

    parser.add_argument(
        '-b',
        '--build',
        help='specify the build number from a package',
        required=False,
        action='store'
    )

    parser.add_argument(
        '-d',
        '--diff',
        help='specify the build number of a package to create diff against',
        required=False,
        action='store',
        nargs=2
    )

    parser.add_argument(
        '-r',
        '--resetcache',
        help='removes currently cached package plist files',
        required=False,
        action='store_true'
    )

    parser.add_argument(
        '-c',
        '--buildcache',
        help='caches the package manifests and builds an index',
        required=False,
        action='store_true'
    )
    
    parser.add_argument(
        '-f',
        '--findhash',
        help='gets the hash for the specified build number of a package of a release type',
        required=False,
        action='store_true'
    )

    args_dict = vars(parser.parse_args())

    if CheckPassedArgCount(args_dict) == 0:
        if config.getFirstRun() == True:
            logging_helper.getLogger().info('This appears to be the first time this has been run, it is highly recommended that you run the "cache setup" command or pass "--buildcache" on the command line. This software can be used without this command being run but some of the autocomplete will not work.')
        if 'libedit' in readline.__doc__:
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
        aosd_shell = InteractiveInput()
        aosd_shell.cmdloop()
    else:
        ParseFlags(args_dict)
    sys.exit()

if __name__ == "__main__":
    main()
