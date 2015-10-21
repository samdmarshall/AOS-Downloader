import sys
import platform
if sys.platform == 'darwin' and not 'ppc' in platform.machine():
     from .readline_unsorted.cmd import *
else:
    from cmd import Cmd

from .CmdBuild import CmdBuild
from .CmdCache import CmdCache
from .CmdConfig import CmdConfig
from .CmdDiff import CmdDiff
from .CmdDownload import CmdDownload
from .CmdHash import CmdHash
from .CmdList import CmdList
from .CmdPackage import CmdPackage
from .CmdQuit import CmdQuit
from .CmdType import CmdType
from .CmdUpdate import CmdUpdate
from .CmdVersion import CmdVersion

from ..downloader.releases import releases
from ..version import __version__ as AOSD_VERSION

class InteractiveInput(Cmd):
    prompt = ':> '
    display_info = {}
    quitOnError = True

    def GenerateInfo(self):
        info = []
        if 'type' in self.display_info.keys():
            info.append('Type: %s' % releases.get_display_name(self.display_info['type']))
        if 'version' in self.display_info.keys():
            info.append('Version: %s' % self.display_info['version'])
        if 'package' in self.display_info.keys():
            info.append('Package: %s' % self.display_info['package'])
        if 'build' in self.display_info.keys():
            info.append('Build: %s' % self.display_info['build'])
        return '\n'.join(info)

    def postcmd(self, stop, line):
        info_string = self.GenerateInfo()
        if len(info_string) > 0:
            print('\n'+info_string)
        return stop
        
    def emptyline(self):
        # do nothing as repeating the last command can be dangerous
        return None
    
    # Quit
    def help_quit(self):
        CmdQuit.DisplayUsage()

    def do_quit(self, line):
        ret_val = CmdQuit.process_do(line, self.display_info)
        return ret_val if self.quitOnError == True else None

    # Release type
    def help_type(self):
        CmdType.DisplayUsage()

    def do_type(self, line):
        ret_val = CmdType.process_do(line, self.display_info)
        return ret_val

    def complete_type(self, text, line, begidx, endidx):
        completions = []
        release_types = CmdType.valid_values()
        if not text:
            completions = release_types[:]
        else:
            completions = [item for item in release_types if item.startswith(text)]
        return completions

    # Package
    def help_package(self):
        CmdPackage.DisplayUsage()

    def do_package(self, line):
        ret_val = CmdPackage.process_do(line, self.display_info)
        return ret_val if self.quitOnError == True else None

    def complete_package(self, text, line, begidx, endidx):
        completions = []
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type']
            release_version = None
            if 'version' in self.display_info.keys():
                release_version = self.display_info['version']
            package_names = CmdPackage.valid_values(release_type, release_version)
            if not text:
                completions = package_names[:]
            else:
                completions = [item for item in package_names if item.startswith(text)]
        return completions

    # Release Version
    def help_version(self):
        CmdVersion.DisplayUsage()

    def do_version(self, line):
        ret_val = CmdVersion.process_do(line, self.display_info)
        return ret_val if self.quitOnError == True else None

    def complete_version(self, text, line, begidx, endidx):
        completions = []
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type']
            release_versions = CmdVersion.valid_values(release_type)
            if not text:
                completions = release_versions[:]
            else:
                completions = [item for item in release_versions if item.startswith(text)]
        return completions

    # Cache Control
    def help_cache(self):
        CmdCache.DisplayUsage()

    def do_cache(self, line):
        ret_val = CmdCache.process_do(line, self.display_info)
        return ret_val if self.quitOnError == True else None

    def complete_cache(self, text, line, begidx, endidx):
        completions = []
        cache_completions = CmdCache.valid_values()
        if not text:
            completions = cache_completions[:]
        else:
            completions = [item for item in cache_completions if item.startswith(text)]
        return completions

    # Update
    def help_update(self):
        CmdUpdate.DisplayUsage()

    def do_update(self, line):
        ret_val = CmdUpdate.process_do(line, self.display_info)
        return ret_val if self.quitOnError == True else None

    # Download
    def help_download(self):
        CmdDownload.DisplayUsage()

    def do_download(self, line):
        ret_val = CmdDownload.process_do(line, self.display_info)
        return ret_val if self.quitOnError == True else None

    # Build
    def help_build(self):
        CmdBuild.DisplayUsage()

    def complete_build(self, text, line, begidx, endidx):
        completions = []
        if 'type' in self.display_info.keys() and 'package' in self.display_info.keys():
            release_type = self.display_info['type']
            package_name = self.display_info['package']
            build_numbers = CmdBuild.valid_values(release_type, package_name)
            if not text:
                completions = build_numbers[:]
            else:
                completions = [item for item in build_numbers if item.startswith(text)]
        return completions

    def do_build(self, line):
        ret_val = CmdBuild.process_do(line, self.display_info)
        return ret_val if self.quitOnError == True else None

    # Config
    def help_config(self):
        CmdConfig.DisplayUsage()

    def complete_config(self, text, line, begidx, endidx):
        completions = []
        config_completions = CmdConfig.valid_values()
        if not text:
            completions = config_completions[:]
        else:
            completions = [item for item in config_completions if item.startswith(text)]
        return completions

    def do_config(self, line):
        ret_val = CmdConfig.process_do(line, self.display_info)
        return ret_val if self.quitOnError == True else None

    # diff
    def help_diff(self):
        CmdDiff.DisplayUsage()

    def do_diff(self, line):
        ret_val = CmdDiff.process_do(line, self.display_info)
        return ret_val if self.quitOnError == True else None
        
    # hashes
    def help_hash(self):
        CmdHash.DisplayUsage()
    
    def do_hash(self, line):
        ret_val = Cmdhash.process_do(line, self.display_info)
        return ret_val if self.quitOnError == True else None
    
    # list
    def help_list(self):
        CmdList.DisplayUsage()
    
    def do_list(self, line):
        ret_val = CmdList.process_do(line, self.display_info)
        return ret_val if self.quitOnError == True else None
    
    # info
    def do_info(self, line):
        print('AOSD Version: '+AOSD_VERSION)