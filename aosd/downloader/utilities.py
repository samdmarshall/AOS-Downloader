import os

class utilities(object):
    
    @classmethod
    def GetLookupPlistPath(cls, name):
        return os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),'data/'+name+'.plist')

    @classmethod
    def GetReleasePlistPath(cls):
        return cls.GetLookupPlistPath('releases')
    
    @classmethod
    def GetConfigurationPlistPath(cls):
        return cls.GetLookupPlistPath('aosd')
    
    @classmethod
    def GetCacheFile(cls, file_name):
        return os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data/cache/'+file_name)

    @classmethod
    def CreateCacheFileName(cls, prefix, version):
        return prefix+'-'+version+'.plist'