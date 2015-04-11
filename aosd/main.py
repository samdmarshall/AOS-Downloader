import sys
import argparse
import readline
import rlcompleter

from .commandparse import *
from .downloader import *

def CheckPassedArgCount(args):
    kDefaultValues = {
        'build': None,
        'diff': None,
        'list': False,
        'package': None,
        'resetcache': False,
        'type': None,
        'version': None
    };
    # returns the number of arguments that got passed that are not set to default values
    return len(filter(lambda key: kDefaultValues[key] != args[key], args.keys()));

def main():
    parser = argparse.ArgumentParser(description='Apple Open Source Package Downloader');
    parser.add_argument(
        '-t', 
        '--type', 
        help='specify the release type "mac", "ios", "server", "dev"', 
        required=False,
        action='store'
    );
    
    parser.add_argument(
        '-l', 
        '--list', 
        help='list versions of a package to check out, if no package is specified it lists available packages', 
        required=False,
        action='store_true'
    );
    
    parser.add_argument(
        '-v', 
        '--version', 
        help='specify the version number from a release type', 
        required=False,
        action='store'
    );
    
    parser.add_argument(
        '-p', 
        '--package', 
        help='specify the name of a package from a release', 
        required=False,
        action='store', 
    );
    
    parser.add_argument(
        '-b', 
        '--build', 
        help='specify the build number from a package', 
        required=False,
        action='store'
    );
    
    parser.add_argument(
        '-d', 
        '--diff', 
        help='specify the build number of a package to create diff against', 
        required=False,
        action='store', 
        nargs=2
    );
    
    parser.add_argument(
        '-r', 
        '--resetcache', 
        help='removes currently cached package plist files', 
        required=False,
        action='store_true'
    );
    
    args_dict = vars(parser.parse_args());
    
    aosd_instance = AOSD();
    if CheckPassedArgCount(args_dict) == 0:
        if 'libedit' in readline.__doc__:
            readline.parse_and_bind("bind ^I rl_complete");
        else:
            readline.parse_and_bind("tab: complete");
        aosd_shell = input();
        aosd_shell.AOSD = aosd_instance;
        aosd_shell.cmdloop();
    else:
        print 'pass args';
    

if __name__ == "__main__":
    main();