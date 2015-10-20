"""
imports
"""
from .RootCmd import RootCmd
from ..logging_helper import logging_helper
from ..downloader.Packages import Packages
from ..downloader.Hashes import Hashes
from ..downloader.manager import manager

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
