from __future__ import absolute_import

from ..logging_helper import *

from .releases import *
from .cacher import * 

class packages(object):
    
    @classmethod
    def GetPackages(cls, release_type, version):
        packages = [];
        release_info = releases.GetReleaseInfo(release_type, version);
        cache_result = cacher.access_cache(release_type, release_info);
        if cache_result[0] == True:
            packages = cache_result[1];
        else:
            logging_helper.getLogger().error(': Could not find any packages. If you think this is an error, please run the "cache rebuild" command.');
        return packages;
    
    @classmethod
    def package_list(cls, release_type):
        packages = [];
        if release_type != None:
            package_cache_file_path = cacher.GetCacheFile('package_cache.plist');
            if os.path.exists(package_cache_file_path) == False:
                cacher.fetch_cache(release_type, None);