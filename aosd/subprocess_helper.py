from .logging_helper import logging_helper

import subprocess
from subprocess import CalledProcessError

class subprocess_helper(object):
    
    @classmethod
    def make_call(cls, call_args):
        error = 0
        output = ''
        try:
            output = subprocess.check_output(call_args)
            error = 0
        except CalledProcessError as e:
            output = e.output
            error = e.returncode
        if error != 0:
            logging_helper.getLogger().error(': There was an error in creating the diff, the error will be logged to the diff file...')
        return output