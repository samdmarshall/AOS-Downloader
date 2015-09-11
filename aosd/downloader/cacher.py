from __future__ import absolute_import

from ..logging_helper import *

import os
import plistlib
from .manager import *
from .versions import *
from .releases import *

class cacher(object):
    
    @classmethod
    def GetCacheFile(cls, file_name):
        return os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data/cache/'+file_name);

    @classmethod
    def CreateCacheFileName(cls, prefix, version):
        return prefix+'-'+version+'.plist';
    
    @classmethod
    def access_cache(cls, release_type, release_info_dict):
        found_manifest = False;
        packages = [];
        if release_type != None and release_info_dict != None:
            cacher.fetch_cache(release_type, release_info_dict['name']);
            release_plist_name = cacher.CreateCacheFileName(release_info_dict['prefix'], release_info_dict['version']);
            cached_file_path = cacher.GetCacheFile(release_plist_name);
            
            if os.path.exists(cached_file_path) == True:
                found_manifest = True;
                version_manifest_dict = plistlib.readPlist(cached_file_path);
                for key in version_manifest_dict['projects']:
                    packages.append(key);
        else:
            print '\n';
            logging_helper.getLogger().error(': Must supply a release type, set this using the "type" command.');
        return (found_manifest, packages);
    
    @classmethod
    def fetch_cache(cls, release_type, release_version):
        if release_type != None:
            if release_version != None:
                release_info_dict = releases.GetReleaseInfo(release_type, release_version);
                release_plist_name = cacher.CreateCacheFileName(release_info_dict['prefix'], release_info_dict['version']);
                cached_file_path = cacher.GetCacheFile(release_plist_name);

                if os.path.exists(cached_file_path) == False:
                    logging_helper.getLogger().info(': Downloading version manifest ('+release_plist_name+')...');
                    manager.DownloadPackageManifest(cached_file_path);
            else:
                type_versions = versions.GetVersions(release_type);
                for version in type_versions:
                    release_version_info = releases.GetReleaseInfo(release_type, version);
                    cacher.fetch_cache(release_type, release_version_info['name']);
        else:
            types = releases.GetReleases();
            for type_name in types:
                cacher.fetch_cache(type_name, None);
    
    @classmethod
    def flush_cache(cls, release_type, release_version):
        if release_type != None:
            if release_version != None:
                release_info_dict = releases.GetReleaseInfo(release_type, release_version);
                release_plist_name = cacher.CreateCacheFileName(release_info_dict['prefix'], release_info_dict['version']);
                cached_file_path = cacher.GetCacheFile(release_plist_name);

                if os.path.exists(cached_file_path) == True:
                    print '\n';
                    logging_helper.getLogger().info(': Removing version manifest ('+release_plist_name+')...');
                    manager.RemovePackageManifest(cached_file_path);
            else:
                type_versions = versions.GetVersions(release_type);
                for version in type_versions:
                    release_version_info = releases.GetReleaseInfo(release_type, version);
                    cacher.fetch_cache(release_type, release_version_info['name']);
        else:
            types = releases.GetReleases();
            for type_name in types:
                cacher.fetch_cache(type_name, None);
    
    @classmethod
    def rebuild(cls):
        return;