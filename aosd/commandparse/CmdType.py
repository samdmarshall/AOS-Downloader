"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.releases import releases

class CmdType(RootCmd):

    @classmethod
    def usage(cls):
        return {
            'name': 'type',
            'args': '['+'|'.join(releases.get())+']',
            'desc': 'selects the current release type'
        }

    @classmethod
    def valid_values(cls):
        return releases.get()

    @classmethod
    def query(cls, args):
        # only use the first value
        if len(args) > 0:
            return (args[0] in cls.valid_values(), args[0])
        else:
            return (False, None)

