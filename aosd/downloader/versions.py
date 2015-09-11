from ..logging_helper import *

from .utilities import *

import plistlib

class versions(object):
    
    @classmethod
    def get(cls, release_type):
        versions = [];
        type_plist_path = utilities.GetLookupPlistPath(release_type);
        if os.path.exists(type_plist_path) == True:
            versions_dict = plistlib.readPlist(type_plist_path);
            version_results = map(lambda version: version['name'], versions_dict);
            if len(version_results) > 0:
                versions = version_results;
            else:
                logging_helper.getLogger().error(': Could not find any versions for release type "'+release_type+'".');
        else:
            logging_helper.getLogger().error(': Could not find a versions manifest for release type "'+release_type+'". If you think this is an error, run the "update" command.');
        return versions;
        