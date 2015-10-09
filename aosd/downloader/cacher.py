from __future__ import absolute_import

from ..logging_helper import logging_helper

import os
import plistlib
from .utilities import utilities
from .manager import manager
from .versions import versions
from .releases import releases
from .config import config

class cacher(object):


    @classmethod
    def access(cls, release_type, release_info_dict):
        found_manifest = False
        packages = []
        if release_type != None and release_info_dict != None:
            cls.fetch(release_type, release_info_dict['name'])
            release_plist_name = utilities.createcachefilename(release_info_dict['prefix'], release_info_dict['version'])
            cached_file_path = utilities.getcachefile(release_plist_name)

            if os.path.exists(cached_file_path) == True:
                found_manifest = True
                version_manifest_dict = plistlib.readPlist(cached_file_path)
                for key in version_manifest_dict['projects']:
                    packages.append(key)
        else:
            logging_helper.getLogger().error('Must supply a release type, set this using the "type" command.')
        return (found_manifest, packages)

    @classmethod
    def get(cls, release_type, release_version):
        files = None
        if release_type != None:
            if release_version != None:
                release_info_dict = releases.getInfo(release_type, release_version)
                release_plist_name = utilities.createcachefilename(release_info_dict['prefix'], release_info_dict['version'])
                cached_file_path = utilities.getcachefile(release_plist_name)

                if os.path.exists(cached_file_path) == True:
                    return cached_file_path

            else:
                files = []
                type_versions = versions.get(release_type)
                for version in type_versions:
                    release_version_info = releases.getInfo(release_type, version)
                    path = cls.get(release_type, release_version_info['name'])
                    if path != None:
                        files.append(path)
        else:
            files = {}
            types = releases.get()
            for type_name in types:
                packages = cls.get(type_name, None)
                if len(packages) > 0:
                    files[type_name] = packages
        return files

    @classmethod
    def fetch(cls, release_type, release_version):
        if release_type != None:
            if release_version != None:
                release_info_dict = releases.getInfo(release_type, release_version)
                release_plist_name = utilities.createcachefilename(release_info_dict['prefix'], release_info_dict['version'])
                cached_file_path = utilities.getcachefile(release_plist_name)

                if os.path.exists(cached_file_path) == False:
                    logging_helper.getLogger().info('Downloading version manifest ('+release_plist_name+')...')
                    manager.DownloadPackageManifest(cached_file_path)
            else:
                type_versions = versions.get(release_type)
                for version in type_versions:
                    release_version_info = releases.getInfo(release_type, version)
                    cls.fetch(release_type, release_version_info['name'])
        else:
            types = releases.get()
            for type_name in types:
                cls.fetch(type_name, None)

    @classmethod
    def flush(cls, release_type, release_version):
        if release_type == None and release_version == None:
            settings = config.read()
            settings['first_run'] = True
            config.write(settings)
        if release_type != None:
            if release_version != None:
                release_info_dict = releases.getInfo(release_type, release_version)
                release_plist_name = utilities.createcachefilename(release_info_dict['prefix'], release_info_dict['version'])
                cached_file_path = utilities.getcachefile(release_plist_name)

                if os.path.exists(cached_file_path) == True:
                    logging_helper.getLogger().info('Removing version manifest ('+release_plist_name+')...')
                    manager.RemovePackageManifest(cached_file_path)
            else:
                type_versions = versions.get(release_type)
                for version in type_versions:
                    release_version_info = releases.getInfo(release_type, version)
                    cls.flush(release_type, release_version_info['name'])
        else:
            types = releases.get()
            for type_name in types:
                cls.flush(type_name, None)

    @classmethod
    def rebuild(cls):
        config.toggleFirstRun()
        package_cache = {}
        available_package_manifests = cls.get(None, None)
        for release_type in available_package_manifests:
            release_packages = {}
            for manifest_path in available_package_manifests[release_type]:
                manifest = plistlib.readPlist(manifest_path)
                for package_name in manifest['projects']:
                    package_name = str(package_name)
                    version_number = str(manifest['projects'][package_name]['version'])
                    if package_name in release_packages.keys():
                        if version_number not in release_packages[package_name]:
                            release_packages[package_name].append(version_number)
                    else:
                        release_packages[package_name] = [version_number]
            package_cache[str(release_type)] = release_packages
        package_cache_path = utilities.getcachefile('package_cache.plist')
        plistlib.writePlist(package_cache, package_cache_path)

    @classmethod
    def clean(cls):
        cls.flush(None, None)
        cls.fetch(None, None)
        cls.rebuild()
