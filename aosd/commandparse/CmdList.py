"""
imports
"""
from .RootCmd import RootCmd
from ..logging_helper import logging_helper
from ..downloader.Packages import Packages
from ..downloader.Builds import Builds

class CmdList(RootCmd):
    """
    command to display available versions
    """
    @classmethod
    def usage(cls):
        return {
            'name': 'list',
            'args': '',
            'desc': 'displays available versions based on selected release type and package'
        }

    @classmethod
    def action(cls, args):
        release_type = args.get('type', None)
        package_name = args.get('package', None)
        if release_type != None:
            if package_name != None:
                has_valid_package = package_name in Packages.list(release_type)
                if has_valid_package == True:
                    print('Builds for package '+package_name+':')
                    for build_number in Builds.get(release_type, package_name):
                        print(build_number)
                else:
                    logging_helper.getLogger().error('Invalid package name!')
            else:
                print('Packages for '+release_type+':')
                for package_name in Packages.list(release_type):
                    print(package_name)
        else:
            logging_helper.getLogger().info('Please select a release type before using the "list" command for packages, or please select a release type and package before using the "list" command for build numbers.')
        print('====================')
