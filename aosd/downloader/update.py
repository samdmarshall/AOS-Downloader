from ..logging_helper import *

import os
import urllib2

from .releases import *
from .config import *

class update(object):
    
    @classmethod
    def fetch(cls):
        logging_helper.getLogger().info(': Updating package data...');
        