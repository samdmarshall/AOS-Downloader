"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.update import update

class CmdUpdate(RootCmd):
    """
    command for fetching updates to the releases plist
    """

    @classmethod
    def usage(cls):
        """
        command usage
        """
        return {
            'name': 'update',
            'args': '',
            'desc': 'updates the current open source manifests'
        }

    @classmethod
    def action(cls, args):
        """
        calls to perform the update
        """
        update.fetch()
        print('====================')
