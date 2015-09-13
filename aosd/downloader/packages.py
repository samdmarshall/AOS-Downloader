from __future__ import absolute_import

from ..logging_helper import *

from .releases import *
from .cacher import * 

class packages(object):
    
    @classmethod
    def get(cls, release_type, version):
        packages = [];
        if version == None:
            packages = cls.list(release_type);
        else:
            release_info = releases.getInfo(release_type, version);
            cache_result = cacher.access(release_type, release_info);
            if cache_result[0] == True:
                packages = cache_result[1];
            else:
                logging_helper.getLogger().error(': Could not find any packages. If you think this is an error, please run the "cache rebuild" command.');
        return packages;
    
    @classmethod
    def list(cls, release_type):
        packages = [];
        package_cache_path = cacher.GetCacheFile('package_cache.plist');
        if os.path.exists(package_cache_path) == True:
            package_cache = plistlib.readPlist(package_cache_path);
            release_packages = package_cache.get(str(release_type), None);
            if release_packages != None:
                for package_name in release_packages:
                    packages.append(str(package_name));
        return packages;