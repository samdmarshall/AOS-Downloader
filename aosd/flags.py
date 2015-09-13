import sys

from .downloader import packages
from .downloader.manager import manager
from .downloader.diff import diff
from .downloader import releases
from .downloader import config
from .downloader.cacher import cacher
from .downloader.builds import builds
from .logging_helper import logging_helper

def ParseFlags(args_dict):
    # command line flag parsing

    release_type = args_dict.get('type', None)
    has_type = release_type != None

    list_action = args_dict.get('list', False)
    has_list = list_action == True

    package_name = args_dict.get('package', None)
    has_package = package_name != None

    build_number = args_dict.get('build', None)
    has_build = build_number != None

    diff_numbers = args_dict.get('diff', None)
    has_diff = diff_numbers != None

    has_other_flags = has_list or has_package or has_build or has_diff

    has_reset_cache = args_dict.get('reset_cache', False)

    has_build_cache = args_dict.get('build_cache', False)

    if has_reset_cache == True:
        cacher.flush(None, None)

    if has_build_cache == True:
        cacher.clean()

    if config.getFirstRun() == True:
        logging_helper.getLogger().info(': You cannot use the command line interface without first building an index. Please run with only the "--build_cache" flag first.')

    if has_type == True and has_other_flags == True:
        # ok, check the type
        type_list = releases.get()
        has_valid_type = release_type in type_list
        if has_valid_type == True:
            if has_list == True:
                # list is a terminal action
                if has_package == True:
                    # list the builds
                    has_valid_package = package_name in packages.list(release_type)
                    if has_valid_package == True:
                        print('Builds for package '+package_name+':')
                        print(builds.get(release_type, package_name))
                    else:
                        logging_helper.getLogger().error(': Invalid package name! Please use the "--list" flag to see available packages.')
                else:
                    # list the packages
                    print('Packages for '+release_type+':')
                    print(packages.list(release_type))
            else:
                # check other actions
                if has_package == True:
                    has_valid_package = package_name in packages.list(release_type)
                    if has_valid_package == True:
                        # now check the build number
                        if has_build == True:
                            # check to see if the build number is valid
                            manager.ValidateAndDownload(release_type, package_name, build_number)
                        else:
                            # if we don't supply a build number we will then check to see if we should diff
                            if has_diff == True:
                                if len(diff_numbers) == 2:
                                    # have both numbers
                                    diff.perform(release_type, package_name, diff_numbers)
                                else:
                                    logging_helper.getLogger().error(': Please supply TWO build numbers to perform a diff.')
                            else:
                                logging_helper.getLogger().info(': Missing additional arguments!')
                    else:
                        logging_helper.getLogger().error(': Invalid package name! Please use the "--list" flag to see available packages.')
                else:
                    logging_helper.getLogger().error(': No package was specified!')
        else:
            logging_helper.getLogger().error(': The type "'+release_type+'" was not found in the valid types: %s', type_list)
    else:
        if has_other_flags == True: # has_type is implicitly "False"
            logging_helper.getLogger().error(': The "type" argument must be supplied to use any of the other flags!')
