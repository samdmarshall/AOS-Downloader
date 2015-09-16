from __future__ import absolute_import

from .utilities import utilities

from ..logging_helper import logging_helper

import plistlib
import os

class Builds(object):

    @classmethod
    def get(cls, release_type, package_name):
        builds_list = []
        package_cache_path = utilities.getcachefile('package_cache.plist')
        if os.path.exists(package_cache_path) == True:
            package_cache = plistlib.readPlist(package_cache_path)
            release_packages = package_cache[str(release_type)]
            if release_packages != None:
                package_versions = release_packages[str(package_name)]
                if package_versions != None:
                    builds_list = package_versions
        return builds_list
