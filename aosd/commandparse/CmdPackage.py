"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.Packages import Packages

class CmdPackage(RootCmd):

    @classmethod
    def usage(cls):
        return {
            'name': 'package',
            'args': '<package name>',
            'desc': 'selects a package by name from the current release type'
        }

    @classmethod
    def valid_values(cls, release_type, release_version):
        return Packages.get(release_type, release_version)

    @classmethod
    def query(cls, release_type, version, args):
        # only use the first value
        if len(args) > 0:
            build_number = None
            if version != None:
                build_number = Packages.resolveNumberFromVersion(release_type, version, args[0])
            return (args[0] in cls.valid_values(release_type, version), [args[0], build_number])
        else:
            return (False, None)
