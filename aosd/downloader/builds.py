from ..logging_helper import *

from .cacher import *
import plistlib
import os

class builds(object):
    
    @classmethod
    def get(cls, release_type, package_name):
        builds = [];
        package_cache_path = cacher.GetCacheFile('package_cache.plist');
        if os.path.exists(package_cache_path) == True:
            package_cache = plistlib.readPlist(package_cache_path);
            release_packages = package_cache[str(release_type)];
            if release_packages != None:
                package_versions = release_packages[str(package_name)];
                if package_versions != None:
                    builds = package_versions;
        return builds;
    
    @classmethod
    def resolveNumberFromVersion(cls, release_type, version, package_name):
        build_number = '';
        version_manifest_path = cacher.get(release_type, version);
        if version_manifest_path != None:
            version_manifest = plistlib.readPlist(version_manifest_path);
            build_number = version_manifest['projects'][package_name]['version'];
        return build_number;
            