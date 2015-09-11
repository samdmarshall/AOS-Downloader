from ..logging_helper import *

import os
import urllib2

from .utilities import *
from .releases import *
from .config import *
from .manager import *

class update(object):
    
    @classmethod
    def fetch(cls):
        logging_helper.getLogger().info(': Updating package data...');
        release_plist_url = os.path.join(config.getUpdateURL(), 'releases.plist');
        release_plist_path = utilities.GetReleasePlistPath();
        manager.DownloadFileFromURLToPath(release_plist_url, release_plist_path);
        if os.path.exists(release_plist_path) == True:
            for release_type in releases.get():
                release_type_plist_url = os.path.join(config.getUpdateURL(), release_type+'.plist');
                release_type_plist_path = utilities.GetLookupPlistPath(release_type);
                manager.DownloadFileFromURLToPath(release_type_plist_url, release_type_plist_path);