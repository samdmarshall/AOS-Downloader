import os

class utilities(object):
    
    @classmethod
    def GetLookupPlistPath(cls, name):
        return os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),'data/'+name+'.plist');

    @classmethod
    def GetReleasePlistPath(cls):
        return cls.GetLookupPlistPath('releases');
    
    @classmethod
    def GetConfigurationPlistPath(cls):
        return cls.GetLookupPlistPath('aosd');