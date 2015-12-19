from __future__ import absolute_import

from .utilities import utilities

from ..helpers.logging_helper import logging_helper

import plistlib
import os

class Builds(object):

    @classmethod
    def get(cls, release_type, package_name):
        builds_list = []
        package_cache_path = utilities.getcachefile('package_cache.plist')
        if os.path.exists(package_cache_path) == True:
            package_cache = plistlib.readPlist(package_cache_path)
            release_packages = package_cache.get(str(release_type), None)
            if release_packages != None:
                package_versions = release_packages.get(str(package_name), None)
                if package_versions != None:
                    builds_list = package_versions
        return builds_list
