"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.Packages import Packages
from ..downloader.Builds import Builds

from ..helpers.logging_helper import logging_helper
from ..helpers.argument_helper import argument_helper

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
                package_list = Packages.list(release_type)
                has_valid_package = package_name in package_list
                if has_valid_package == True:
                    print('Builds for package '+package_name+':')
                    for build_number in Builds.get(release_type, package_name):
                        print(build_number)
                else:
                    if len(package_list) > 0:
                        logging_helper.getLogger().error('Invalid package name!')
                    else:
                        logging_helper.getLogger().error('The package list has not been built yet, please run "cache rebuild" to rebuild it. If that does not resolve this please run "cache setup".')
            else:
                print('Packages for '+release_type+':')
                for package_name in Packages.list(release_type):
                    print(package_name)
        else:
            logging_helper.getLogger().info('Please select a release type before using the "list" command for packages, or please select a release type and package before using the "list" command for build numbers.')
        print('====================')

    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        arguments = argument_helper.parse(line_text)
        result = cls.query(arguments)
        if result[0] == True:
            cls.action(context)
        else:
            ret_val = 'Fatal error, could not list!'
            logging_helper.getLogger().error(ret_val)
        return ret_val