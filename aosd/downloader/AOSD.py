import os
import sys
import plistlib
import urllib2
import gzip
import tarfile
from distutils.version import LooseVersion

OSX_MAP_NEW_PREFIX_KEYS = ['10.10.1', '10.10', '10.9.5', '10.9.4', '10.9.3', '10.9.2', '10.9.1', '10.9'];
IOS_MAP_NEW_PREFIX_KEYS = ['7.0', '6.1.3', '6.1', '6.0.1', '6.0', '5.1.1', '5.1', '5.0', '4.3.3', '4.3.2', '4.3.1', '4.3', '4.2', '4.1', '4.0'];

# Helper Functions
def GetCacheDir():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)),'cache');
def GetProjectsDir():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)),'projects');
def CheckMakeDir(path):
    if os.path.exists(path) == False:
        os.mkdir(path);
def MakeProjectsDir():
    CheckMakeDir(GetProjectsDir());
def MakeCacheDir():
    CheckMakeDir(GetCacheDir());
def ListVersionCompare(obj1, obj2):
    # This code is for sorting by release version
    #version1 = obj1['release'];
    #version2 = obj2['release'];
    #return VersionCompare(version1, version2);
    # This code is for sorting by build version
    version1 = obj1['build'];
    version2 = obj2['build'];
    versions = [ version1, version2 ];
    versions.sort(key=LooseVersion);
    if versions[0] == version1:
        return -1;
    elif versions[0] == version2:
        return 1;
    else:
        return 0;
def VersionCompareParseTypeResolve(elements, index):
    if index <= 2:
        return int(elements[index]);
    else:
        return str(elements[index]);
def VersionCompareParse(version1_elements, version1, version2_elements, version2, index):
    if version1 == version2:
        index += 1;
        changev1 = False;
        changev2 = False;
        if len(version1_elements) > index:
            version1 = VersionCompareParseTypeResolve(version1_elements, index);
            changev1 = True;
        if len(version2_elements) > index:
            version2 = VersionCompareParseTypeResolve(version2_elements, index);
            changev2 = True;
        if changev1 == True and changev2 == True:
            return VersionCompareParse(version1_elements, version1, version2_elements, version2, index);
        else:
            if changev1 == True:
                return 1;
            elif changev2 == True:
                return -1;
            else:
                return 0;
    else:
        if index <= 2:
            return version1 - version2;
        else:
            version_strings = [ version1, version2 ];
            version_strings.sort();
            if version1 == version_strings[0]:
                return 1;
            if version2 == version_strings[0]:
                return -1;
def VersionCompare(obj1, obj2):
    version1_elements = obj1.split('.');
    version2_elements = obj2.split('.');
    index = 0;
    
    if len(version1_elements) == 1 or len(version2_elements) == 1:
        if len(version1_elements) == 1:
            return 1;
        if len(version2_elements) == 1:
            return -1;
    else:
        version1 = VersionCompareParseTypeResolve(version1_elements, index);
        version2 = VersionCompareParseTypeResolve(version2_elements, index);
        return VersionCompareParse(version1_elements, version1, version2_elements, version2, index);

def GetPlistFromURL(url):
    head, tail = os.path.split(url);
    cached_path = os.path.join(GetCacheDir(),tail);
    MakeCacheDir();
    if os.path.exists(cached_path) == False:
        request = urllib2.Request(url);
        response = None;
        try: 
            response = urllib2.urlopen(request);
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code) + ' on ' + url;
            response = None;
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason) + ' on ' + url;
            response = None;
        except httplib.HTTPException, e:
            print 'HTTPException' + ' on ' + url;
            response = None;
        except Exception:
            print 'Exception :( on ' + url;
            response = None;
        if response != None:
            output = open(cached_path, 'wb');
            output.write(response.read());
            output.close();
    
    if os.path.exists(cached_path) == True:
        return plistlib.readPlist(cached_path);
    else:
        return {};
def CheckAndAppendBuildInfo(elements, build_number):
    should_append = True;
    for item in elements:
        if item['build'] == build_number:
            should_append = False;
        if should_append == False:
            break;
    return should_append;
def DownloadTarball(tarball_address, package_name):
    tarball = urllib2.urlopen(tarball_address);
    output = open(package_name,'wb');
    output.write(tarball.read());
    output.close();
def DownloadPackage(package, build):
    MakeProjectsDir();
    projects_path = GetProjectsDir();
    package_name = package+'-'+build;
    tarball_name = package_name+'.tar.gz';
    print 'Downloading \"'+tarball_name+'\"...';
    tarball_address = 'https://opensource.apple.com/tarballs/'+package+'/'+tarball_name;
    try:
        DownloadTarball(tarball_address, os.path.join(projects_path, tarball_name));
        print 'Download Complete!';
        print 'Decompressing '+tarball_name+' -> '+package_name;
        gz_path = os.path.join(projects_path, tarball_name);
        gz_archive = gzip.open(gz_path, 'rb');
        file_content = gz_archive.read();
        tar_path = os.path.join(projects_path,package_name+'.tar');
        open(tar_path, 'w').write(file_content);
        gz_archive.close();
        os.remove(gz_path);
        tar_archive = tarfile.open(tar_path);
        tar_archive.extractall(projects_path);
        tar_archive.close();
        os.remove(tar_path);
        print 'Decompression Complete!';
    except:
        print 'Could not find tarball!';
# AOSD Class
class AOSD():
    def MapType(self):
        return {
            'mac': self.OSX_MAP,
            'ios': self.IOS_MAP,
            'dev': self.DEVELOPER_MAP,
            'server': self.SERVER_MAP
        };
    def TypeName(self):
        return {
            'mac': 'OS X',
            'ios': 'iOS',
            'dev': 'Developer Tools',
            'server': 'OS X Server'
        };
    def OSX_MAP(self):
        return {
            '10.10.1': '10101',
            '10.10': '1010',
            '10.9.5': '1095',
            '10.9.4': '1094',
            '10.9.3': '1093',
            '10.9.2': '1092',
            '10.9.1': '1091',
            '10.9': '109',
        
            '10.8.5': '1085',
            '10.8.4': '1084',
            '10.8.3': '1083',
            '10.8.2': '1082',
            '10.8.1': '1081',
            '10.8': '108',
        
            '10.7.5': '1075',
            '10.7.4': '1074',
            '10.7.3': '1073',
            '10.7.2': '1072',
            '10.7.1': '1071',
            '10.7': '107',
        
            '10.6.8': '1068',
            '10.6.7': '1067',
            '10.6.6': '1066',
            '10.6.5': '1065',
            '10.6.4': '1064',
            '10.6.3': '1063',
            '10.6.2': '1062',
            '10.6.1': '1061',
            '10.6': '106',
        
            '10.5.8': '1058',
            '10.5.7': '1057',
            '10.5.6': '1056',
            '10.5.5': '1055',
            '10.5.4': '1054',
            '10.5.3': '1053',
            '10.5.2': '1052',
            '10.5.1': '1051',
            '10.5': '105',
        
            '10.4.11.x86': '10411x86',
            '10.4.11.ppc': '10411ppc',
            '10.4.10.x86': '10410x86',
            '10.4.10.ppc': '10410ppc',
            '10.4.9.x86': '1049x86',
            '10.4.9.ppc': '1049ppc',
            '10.4.8.x86': '1048x86',
            '10.4.8.ppc': '1048ppc',
            '10.4.7.x86': '1047x86',
            '10.4.7.ppc': '1047ppc',
            '10.4.6.x86': '1046x86',
            '10.4.6.ppc': '1046ppc',
            '10.4.5.x86': '1045x86',
            '10.4.5.ppc': '1045ppc',
            '10.4.4.x86': '1044x86',
            '10.4.4.ppc': '1044ppc',
            '10.4.3': '1043',
            '10.4.2': '1042',
            '10.4.1': '1041',
            '10.4': '104',
        
            '10.3.9': '1039',
            '10.3.8': '1038',
            '10.3.7': '1037',
            '10.3.6': '1036',
            '10.3.5': '1035',
            '10.3.4': '1034',
            '10.3.3': '1033',
            '10.3.2': '1032',
            '10.3.1': '1031',
            '10.3': '103',
        
            '10.2.8.G5': '1028g5',
            '10.2.8': '1028',
            '10.2.7': '1027',
            '10.2.6': '1026',
            '10.2.5': '1025',
            '10.2.4': '1024',
            '10.2.3': '1023',
            '10.2.2': '1022',
            '10.2.1': '1021',
            '10.2': '102',
        
            '10.1.5': '1015',
            '10.1.4': '1014',
            '10.1.3': '1013',
            '10.1.2': '1012',
            '10.1.1': '1011',
            '10.1': '101',
        
            '10.0.4': '1004',
            '10.0.3': '1003',
            '10.0.2': '1002',
            '10.0.1': '1001',
            '10.0': '100'
        };

    def DEVELOPER_MAP(self):
        return {
            '6.1': '61',
            '6.0': '60',
            
            '5.1': '51',
            '5.0': '50',
        
            '4.6': '46',
            '4.5': '45',
            '4.4': '44',
            '4.3': '43',
            '4.2': '42',
            '4.1': '41',
            '4.0': '40',
        
            '3.2.6': '326',
            '3.2.5': '325',
            '3.2.4': '324',
            '3.2.3': '323',
            '3.2.2': '322',
            '3.2.1': '321',
            '3.2': '32',
        
            '3.1.4': '314',
            '3.1.3': '313',
            '3.1.2': '312',
            '3.1.1': '311',
            '3.1.0': '31',
            '3.1.0.b': '31b',
            '3.0': '30',
        
            '2.5': '25',
            '2.4.1': '241',
            '2.4': '24',
            '2.3': '23',
            '2.2': '22',
            '2.1': '21',
        
            'WWDC2004DP': 'wwdc2004dp',
        
            'WWDC2003DP': 'wwdc2003dp',
        
            'Nov2004': 'nov2004',
            '1.5': '15',
            '1.2': '12',
            'Jun2003': 'jun2003',
            'Dec2002': 'dec2002',
            'May2002': 'may2002',
            'Dec2001': 'dec2001'
        };

    def IOS_MAP(self):
        return {
            '7.0': '70',
            
            '6.1.3': '613',
            '6.1': '61',
        
            '6.0.1': '601',
            '6.0': '60',
        
            '5.1.1': '511',
            '5.1': '51',
            '5.0': '50',
        
            '4.3.3': '433',
            '4.3.2': '432',
            '4.3.1': '431',
            '4.3': '43',
            '4.2': '42',
            '4.1': '41',
            '4.0': '40',
        
            '3.2': '32',
            '3.1.3': '313',
            '3.1.2': '312',
            '3.1.1': '311',
            '3.1': '31',
            '3.0': '30',
        
            '2.2.1': '221',
            '2.2': '22',
            '2.1': '21',
            '2.0': '20',
        
            'SDKb8': 'sdkb8',
            'SDKb7': 'sdkb7',
            'SDKb6': 'sdkb6',
            'SDKb5': 'sdkb5',
            'SDKb4': 'sdkb4',
            'SDKb3': 'sdkb3',
            'SDKb2': 'sdkb2',
        
            '1.1.4': '114',
            '1.1.3': '113',
            '1.1.2': '112',
            '1.1.1': '111',
            '1.0.1': '101',
            '1.0': '10'
        };

    def SERVER_MAP(self):
        return {
            '3.0.2': '302',
            '2.2.2': '222'
        };
    
    def ValidateMapping(self, args):
        arg_count = len(args);
        arg_items = args;
        if arg_items[0] in self.MapType().keys():
            return True;
        else:
            return False;
    def ResolveTypeIdentifier(self, args):
        arg_count = len(args);
        arg_items = args;
        type_name = arg_items[0];
        if type_name == 'mac':
            if arg_items[1] in OSX_MAP_NEW_PREFIX_KEYS:
                type_name = 'os-x';
            else:
                type_name = 'mac-os-x';
        elif type_name == 'ios':
            if arg_items[1] in IOS_MAP_NEW_PREFIX_KEYS:
                type_name = 'ios';
            else:
                type_name = 'iphone';
        elif type_name == 'dev':
            type_name = 'developer-tools';
        elif type_name == 'server':
            type_name = 'os-x-server';
        else:
            type_name = 'invalid';
        return type_name;
    def LookupMapping(self, args):
        arg_count = len(args);
        arg_items = args;
        type_identifier = self.ResolveTypeIdentifier(args);
        version_identifier = self.MapType()[arg_items[0]]()[arg_items[1]];
        return type_identifier+'-'+version_identifier;
    def ResolveMapping(self, args):
        if self.ValidateMapping(args) == True:
            return self.LookupMapping(args);
        else:
            return 'invalid';
    def CreatePackagePlistAddress(self, args):
        mapping_string = self.ResolveMapping(args);
        return 'https://opensource.apple.com/plist/'+mapping_string+'.plist';
    def GetPackageListForVersion(self, args):
        package_address = self.CreatePackagePlistAddress(args);
        search_packages = GetPlistFromURL(package_address);
        return search_packages;
    def CreateVersionListOfPackage(self, args):
        arg_count = len(args);
        arg_items = args;
        found_builds = [];
        for version in self.MapType()[arg_items[0]]().keys():
            search_packages = self.GetPackageListForVersion([arg_items[0], version])
            if 'projects' in search_packages.keys():
                if arg_items[1] in search_packages['projects']: 
                    build_number = search_packages['projects'][arg_items[1]]['version'];
                    if CheckAndAppendBuildInfo(found_builds, build_number) == True:
                        build_info = {
                            'release': version,
                            'build': build_number
                        };
                        found_builds.append(build_info);
        found_builds = sorted(found_builds, cmp=ListVersionCompare)
        return found_builds;