from ..downloader.packages import packages
from ..downloader.builds import builds

class CmdPackage(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'package',
            'args': '<package name>',
            'desc': 'selects a package by name from the current release type'
        }
    
    @classmethod
    def valid_values(cls, release_type, release_version):
        return packages.get(release_type, release_version)
    
    @classmethod
    def query(cls, release_type, version, args):
        # only use the first value
        if len(args) > 0:
            input = args[0]
            build_number = None
            if version != None:
                build_number = packages.resolveNumberFromVersion(release_type, version, input)
            return (input in cls.valid_values(release_type, version), [input, build_number])
        else:
            return (False, None)
    
    @classmethod
    def action(cls, args):
        return