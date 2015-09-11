from ..logging_helper import *

import os
import urllib2

from .releases import *

class update(object):
    
    @classmethod
    def PerformUpdate(cls):
        logging_helper.getLogger().info(': Updating package data...');