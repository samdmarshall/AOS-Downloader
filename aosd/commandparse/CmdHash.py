"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.Packages import Packages
from ..downloader.Hashes import Hashes
from ..downloader.manager import manager

from ..helpers.logging_helper import logging_helper
from ..helpers.argument_helper import argument_helper

class CmdHash(RootCmd):
    """
    command to operate on existing hashes
    """
    @classmethod
    def usage(cls):
        return {
            'name': 'hash',
            'args': '[update|get]',
            'desc': 'updates hashes for a specified release type and version'
        }

    
    @classmethod
    def valid_values(cls):
        """
        arguments that this command takes
        """
        return ['update', 'get']

    @classmethod
    def query(cls, args):
        """
        validates the argument passed to this command
        """
        # only use the first value
        if len(args) > 0:
            return (args[0] in cls.valid_values(), args[0])
        else:
            return (False, None)
    
    @classmethod
    def action(cls, args):
        release_type = args[1]['type']
        if args[0] == 'update':
            version_number = args[1]['version']
            package_list = Packages.get(release_type, version_number)
            for package_name in package_list:
                build_number = Packages.resolveNumberFromVersion(release_type, version_number, package_name)
                recorded_hash = Hashes.get(release_type, package_name, build_number)
                if recorded_hash == '':
                    output_file = manager.DownloadPackageTarball(release_type, package_name, build_number, False)
                    if output_file != '':
                        new_hash = Hashes.calculate(output_file)
                        Hashes.add(release_type, package_name, build_number, new_hash)
                    else:
                        print('Missing package! If there was an error before this please check to see if the url exists and file a radar on the missing tarball!')
        if args[0] == 'get':
            package_name = args[1]['package']
            build_number = args[1]['build']
            print(Hashes.get(release_type, package_name, build_number))
        print('====================')
    
    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        arguments = argument_helper.parse(line_text)
        result = cls.query(arguments)
        if result[0] == True:
            cls.action((result[1], context))
        else:
            ret_val = 'Fatal error, cannot process hashes!'
            logging_helper.getLogger().error(ret_val)
        return ret_val
