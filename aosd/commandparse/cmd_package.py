from ..downloader.packages import *

class cmd_package(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'package',
            'args': '<package name>',
            'desc': 'selects a package by name from the current release type'
        };
    
    @classmethod
    def validValues(cls, release_type, release_version):
        return packages.GetPackages(release_type, release_version);
    
    @classmethod
    def query(cls, release_type, version, args):
        # only use the first value;
        if len(args) > 0:
            input = args[0];
            return (input in cls.validValues(release_type, version), input);
        else:
            return (False, None);
    
    @classmethod
    def action(cls, args):
        print 'package action';