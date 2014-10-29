import os
import subprocess
import sys
import argparse
import plistlib
import urllib2
import gzip
import tarfile
import subprocess
from subprocess import CalledProcessError
# Version Map
OSX_MAP = {
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
OSX_MAP_OLD_PREFIX = 'mac-os-x'; # before 10.9
OSX_MAP_NEW_PREFIX_KEYS = ['10.9.5', '10.9.4', '10.9.3', '10.9.2', '10.9.1', '10.9'];
OSX_MAP_NEW_PREFIX = 'os-x';

DEVELOPER_MAP = {
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

DEVELOPER_MAP_PREFIX = 'developer-tools';

IOS_MAP = {
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

IOS_MAP_OLD_PREFIX = 'iphone'; #before ios 4
IOS_MAP_NEW_PREFIX_KEYS = ['6.1.3', '6.1', '6.0.1', '6.0', '5.1.1', '5.1', '5.0', '4.3.3', '4.3.2', '4.3.1', '4.3', '4.2', '4.1', '4.0'];
IOS_MAP_NEW_PREFIX = 'ios'; 

SERVER_MAP = {
    '3.0.2': '302',
    '2.2.2': '222'
};
# Helper Functions
def PackageListFetch(release_type, version):
    release_name = '';
    if release_type == 'OS X':
        if version in OSX_MAP_NEW_PREFIX_KEYS:
            release_name = OSX_MAP_NEW_PREFIX+'-'+OSX_MAP[version];
        else:
            release_name = OSX_MAP_OLD_PREFIX+'-'+OSX_MAP[version];
    elif release_type == 'iOS':
        if version in IOS_MAP_NEW_PREFIX_KEYS:
            release_name = IOS_MAP_NEW_PREFIX+'-'+IOS_MAP[version];
        else:
            release_name = IOS_MAP_OLD_PREFIX+'-'+IOS_MAP[version];
    elif release_type == 'OS X Server':
        release_name = SERVER_MAP_PREFIX+'-'+SERVER_MAP[version];
    elif release_type == 'Developer Tool':
        release_name = DEVELOPER_MAP_PREFIX+'-'+DEVELOPER_MAP[version];
    else:
        print 'Invalid version number, use -l or --list to print a list of available versions.';
        sys.exit();
    return release_name;
def FetchPlistFromURL(url):
    request = urllib2.Request(url);
    response = urllib2.urlopen(request);
    return plistlib.readPlistFromString(response.read());
def DownloadTarball(tarball_address, package_name):
    tarball = urllib2.urlopen(tarball_address);
    output = open(package_name,'wb');
    output.write(tarball.read());
    output.close();
def DownloadPackage(package, build):
    projects_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'projects');
    package_name = package+'-'+build;
    tarball_name = package_name+'.tar.gz';
    print 'Downloading \"'+tarball_name+'\"...';
    tarball_address = 'http://opensource.apple.com/tarballs/'+package+'/'+tarball_name;
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
# Main
def main(argv):
    parser = argparse.ArgumentParser();
    parser.add_argument('-t', '--type', help='specify the release type \'mac\', \'ios\', \'server\', \'dev\'', required=True, action='store');
    parser.add_argument('-v', '--version', help='specify the version number from a release type', action='store');
    args = parser.parse_args();
    
    release_type = '';
    release_map = {};
    plist_package_address = '';
    
    if args.type == 'mac':
        release_type = 'OS X';
        release_map = OSX_MAP;
    elif args.type == 'ios':
        release_type = 'iOS';
        release_map = IOS_MAP;
    elif args.type == 'server':
        release_type = 'OS X Server';
        release_map = SERVER_MAP;
    elif args.type == 'dev':
        release_type = 'Developer Tool';
        release_map = DEVELOPER_MAP;
    else:
        print 'Invalid release type. Please specify \'mac\', \'ios\', \'server\', or \'dev\' as the type.';
        sys.exit();
    
    if args.version in release_map.keys():
        print 'Found version!';
        plist_package_address = 'http://opensource.apple.com/plist/'+PackageListFetch(release_type,args.version)+'.plist';
    else:
        print 'Invalid version number, use -v or --version to specify a version number.';
        sys.exit();
    
    package_address = 'http://opensource.apple.com/plist/'+PackageListFetch(release_type,args.version)+'.plist';
    search_packages = FetchPlistFromURL(package_address);
    package_names = search_packages['projects'].keys();
    os.mkdir(os.path.join(os.getcwd(),'projects'));
    for package in search_packages['projects']:
        DownloadPackage(package,search_packages['projects'][package]['version']);

if __name__ == "__main__":
    main(sys.argv[1:]);