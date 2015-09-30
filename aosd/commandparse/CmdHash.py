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
            'args': '',
            'desc': 'updates hashes for a specified release type and version'
        }

    @classmethod
    def action(cls, args):
        release_type = args['type']
        version_number = args['version']
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
        print('====================')
