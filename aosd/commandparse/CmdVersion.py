"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.versions import versions
from ..downloader.cacher import cacher

class CmdVersion(RootCmd):
    """
    command to assign a release version
    """

    @classmethod
    def usage(cls):
        """
        usage for this command
        """
        return {
            'name': 'version',
            'args': '<version name>',
            'desc': 'selects the current release version'
        }

    @classmethod
    def valid_values(cls, release_type):
        """
        returns the versions available for this release type
        """
        return versions.get(release_type)

    @classmethod
    def query(cls, release_type, args):
        """
        Validate that what was passed to the command
        """
        # only use the first value
        if len(args) > 0:
            return (args[0] in cls.valid_values(release_type), args[0])
        else:
            return (False, None)

    @classmethod
    def action(cls, args):
        """
        pre-fetch the manifest for this version
        """
        cacher.fetch(args['type'], args['version'])
        print('====================')
