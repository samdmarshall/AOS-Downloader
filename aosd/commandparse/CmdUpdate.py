"""
imports
"""
from ..downloader.update import update

class CmdUpdate(object):
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
    def valid_values(cls):
        """
        empty
        """
        return []

    @classmethod
    def query(cls, args):
        """
        always true
        """
        return (True, None)

    @classmethod
    def action(cls, args):
        """
        calls to perform the update
        """
        update.fetch()
        print('====================')
