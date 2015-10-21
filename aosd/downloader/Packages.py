from __future__ import absolute_import

from ..helpers.logging_helper import logging_helper

from .releases import releases
from .utilities import utilities
from .cacher import cacher

import os
import plistlib

class Packages(object):

    @classmethod
    def get(cls, release_type, version):
        packages = []
        if version == None:
            packages = cls.list(release_type)
        else:
            release_info = releases.getInfo(release_type, version)
            cache_result = cacher.access(release_type, release_info)
            if cache_result[0] == True:
                packages = cache_result[1]
            else:
                logging_helper.getLogger().error('Could not find any packages. If you think this is an error, please run the "cache rebuild" command.')
        return sorted(packages)

    @classmethod
    def list(cls, release_type):
        packages = []
        package_cache_path = utilities.getcachefile('package_cache.plist')
        if os.path.exists(package_cache_path) == True:
            package_cache = plistlib.readPlist(package_cache_path)
            release_packages = package_cache.get(str(release_type), None)
            if release_packages != None:
                for package_name in release_packages:
                    packages.append(str(package_name))
        return sorted(packages)

    @classmethod
    def resolveNumberFromVersion(cls, release_type, version, package_name):
        build_number = ''
        version_manifest_path = cacher.get(release_type, version)
        if version_manifest_path != None:
            version_manifest = plistlib.readPlist(version_manifest_path)
            project_manifest = version_manifest.get('projects', None)
            if project_manifest != None:
                package_manifest = project_manifest.get(package_name, None)
                if package_manifest != None:
                    build_number = package_manifest.get('version', '')
        return build_number
