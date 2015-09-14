"""
imports
"""
import os

class utilities(object):
    """
    convenience calls to get paths
    """

    @classmethod
    def getdatapath(cls):
        return os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data/')

    @classmethod
    def getlookupplistpath(cls, name):
        return os.path.join(cls.getdatapath(), name+'.plist')

    @classmethod
    def getreleaseplistpath(cls):
        return cls.getlookupplistpath('releases')

    @classmethod
    def getconfigurationplistpath(cls):
        return cls.getlookupplistpath('aosd')

    @classmethod
    def getcachefile(cls, file_name):
        return os.path.join(cls.getdatapath(), 'cache/'+file_name)

    @classmethod
    def createcachefilename(cls, prefix, version):
        return prefix+'-'+version+'.plist'
