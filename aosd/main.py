import sys
import argparse

from .commandparse import InteractiveInput
from .downloader.config import config
from .downloader.manager import manager
from .helpers.logging_helper import logging_helper

kFLAGNAME_build = 'build'
kFLAGNAME_diff = 'diff'
kFLAGNAME_list = 'list'
kFLAGNAME_package = 'package'
kFLAGNAME_resetcache = 'resetcache'
kFLAGNAME_type = 'type'
kFLAGNAME_buildcache = 'buildcache'
kFLAGNAME_findhash = 'findhash'
kFLAGNAME_version = 'version'

def CheckPassedArgCount(args):
    kDefaultValues = {
        kFLAGNAME_build: None,
        kFLAGNAME_diff: None,
        kFLAGNAME_list: False,
        kFLAGNAME_package: None,
        kFLAGNAME_resetcache: False,
        kFLAGNAME_type: None,
        kFLAGNAME_buildcache: False,
        kFLAGNAME_findhash: False,
        kFLAGNAME_version: False,
    }
    # returns the number of arguments that got passed that are not set to default values
    return len(list((item for item in args.keys() if kDefaultValues[item] != args[item])))

def ParseFlags(args_dict):
    # command line flag parsing
    console_commands = []
    
    has_version = args_dict.get(kFLAGNAME_version, False)
    if has_version == True:
        console_commands.append('info')
    else:
        has_reset_cache = args_dict.get(kFLAGNAME_resetcache, False)
        if has_reset_cache == True:
            console_commands.append('cache clear_all')
    
        has_build_cache = args_dict.get(kFLAGNAME_buildcache, False)
        if has_build_cache == True:
            console_commands.append('cache setup')
    
        release_type = args_dict.get(kFLAGNAME_type, None)
        if release_type != None:
            console_commands.append('type '+release_type)
    
        package_name = args_dict.get(kFLAGNAME_package, None)
        if package_name != None:
            console_commands.append('package '+package_name)
    
        list_action = args_dict.get(kFLAGNAME_list, False)
        if list_action == True:
            console_commands.append('list')
        else:
            build_number = args_dict.get(kFLAGNAME_build, None)
            if build_number != None:
                console_commands.append('build '+build_number)
    
                has_hash = args_dict.get(kFLAGNAME_findhash, False)
                if has_hash == True:
                    console_commands.append('hash get')
                else:
                    console_commands.append('download')
            else:
                diff_numbers = args_dict.get(kFLAGNAME_diff, None)
                if diff_numbers != None:
                    console_commands.append('diff '+diff_numbers[0]+' '+diff_numbers[1])
    
    return console_commands

def main():
    parser = argparse.ArgumentParser(description='Apple Open Source Package Downloader')
    parser.add_argument(
        '-t',
        '--'+kFLAGNAME_type,
        help='specify the release type',
        required=False,
        action='store'
    )

    parser.add_argument(
        '-l',
        '--'+kFLAGNAME_list,
        help='list versions of a package to check out, if no package is specified it lists available packages',
        required=False,
        action='store_true'
    )

    parser.add_argument(
        '-p',
        '--'+kFLAGNAME_package,
        help='specify the name of a package from a release',
        required=False,
        action='store',
    )

    parser.add_argument(
        '-b',
        '--'+kFLAGNAME_build,
        help='specify the build number from a package',
        required=False,
        action='store'
    )

    parser.add_argument(
        '-d',
        '--'+kFLAGNAME_diff,
        help='specify the build number of a package to create diff against',
        required=False,
        action='store',
        nargs=2
    )

    parser.add_argument(
        '-r',
        '--'+kFLAGNAME_resetcache,
        help='removes currently cached package plist files',
        required=False,
        action='store_true'
    )

    parser.add_argument(
        '-c',
        '--'+kFLAGNAME_buildcache,
        help='caches the package manifests and builds an index',
        required=False,
        action='store_true'
    )
    
    parser.add_argument(
        '-f',
        '--'+kFLAGNAME_findhash,
        help='gets the hash for the specified build number of a package of a release type',
        required=False,
        action='store_true'
    )
    
    parser.add_argument(
        '-v',
        '--'+kFLAGNAME_version,
        help='prints the version information',
        required=False,
        action='store_true'
    )

    args_dict = vars(parser.parse_args())
    
    flag_commands = ParseFlags(args_dict)
    
    if config.getFirstRun() == True and 'cache setup' not in flag_commands and 'info' not in flag_commands:
        logging_helper.getLogger().info('This appears to be the first time this has been run, you should run the "cache setup" command or pass "--'+kFLAGNAME_buildcache+'" on the command line. This command will download several megabytes of plist files from "'+manager.CreateAppleURL()+'" so that packages can be looked up without querying the server.\n')
    
    aosd_shell = InteractiveInput()
    
    if CheckPassedArgCount(args_dict) != 0:
        for command in flag_commands:
            result = aosd_shell.onecmd(command)
            if result != None:
                break
        aosd_shell.onecmd('quit')
    InteractiveInput.quitOnError = False
    aosd_shell.cmdloop()

if __name__ == "__main__":
    main()
