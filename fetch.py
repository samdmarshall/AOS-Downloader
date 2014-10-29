import os
import sys
import argparse
import urllib2
import gzip
import tarfile
import subprocess
from subprocess import CalledProcessError
import AOSD
# Helper Functions
def DownloadTarball(tarball_address, package_name):
    tarball = urllib2.urlopen(tarball_address);
    output = open(package_name,'wb');
    output.write(tarball.read());
    output.close();
def DownloadPackage(package, build):
    package_name = package+'-'+build;
    tarball_name = package_name+'.tar.gz';
    print 'Downloading \"'+tarball_name+'\"...';
    tarball_address = 'http://opensource.apple.com/tarballs/'+package+'/'+tarball_name;
    DownloadTarball(tarball_address, tarball_name);
    print 'Download Complete!';
    print 'Decompressing '+tarball_name+' -> '+package_name;
    gz_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), tarball_name);
    gz_archive = gzip.open(gz_path, 'rb');
    file_content = gz_archive.read();
    tar_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),package_name+'.tar');
    open(tar_path, 'w').write(file_content);
    gz_archive.close();
    os.remove(gz_path);
    tar_archive = tarfile.open(tar_path);
    tar_archive.extractall();
    tar_archive.close();
    os.remove(tar_path);
    print 'Decompression Complete!';
def RunDiff(call_args, diff_path):
    error = 0;
    output = '';
    try:
        output = subprocess.check_output(call_args);
        error = 0
    except CalledProcessError as e:
        output = e.output;
        error = e.returncode;
    diff_file = open(diff_path, 'w');
    diff_file.write(output);
    diff_file.close();
# Main
def main(argv):
    parser = argparse.ArgumentParser();
    parser.add_argument('-t', '--type', help='specify the release type \'mac\', \'ios\', \'server\', \'dev\'', required=True, action='store');
    parser.add_argument('-l', '--list', help='list versions of a package to check out, if no package is specified it lists available packages', action='store_true');
    parser.add_argument('-v', '--version', help='specify the version number from a release type', action='store');
    parser.add_argument('-p', '--package', help='specify the name of a package from a release', action='store');
    parser.add_argument('-b', '--build', help='specify the build number from a package', action='store');
    parser.add_argument('-d', '--diff', help='specify the build number of a package to create diff against', action='store');
    args = parser.parse_args();
    
    AOSD_instance = AOSD.AOSD();
    
    if AOSD_instance.ValidateMapping([args.type, '']) == False:
        print 'Invalid release type. Please specify \'mac\', \'ios\', \'server\', or \'dev\' as the type.';
    else:
        if args.package != None and args.list == True:
            args.diff = None;
            print 'No build number specified, searching all versions of '+AOSD_instance.TypeName()[args.type]+' for builds of \"'+args.package+'\". This may take a few minutes...';
            found_builds = AOSD_instance.CreateVersionListOfPackage([args.type, args.package]);
            for build in found_builds:
                print build['build']+' - '+build['release'];
        elif args.version != None and args.list == True:
            args.diff = None;
            packages = AOSD_instance.GetPackageListForVersion([args.type, args.version]);
            package_names = packages['projects'].keys();
            package_names = sorted(package_names);
            for package in package_names:
                print 'Package: '+package+' - '+packages['projects'][package]['version'];
        elif args.package != None and args.build != None:
            args.diff = None;
            DownloadPackage(args.package, args.build);
        elif args.version != None and args.package != None:
            packages = AOSD_instance.GetPackageListForVersion([args.type, args.version]);
            version_build = packages['projects'][args.package]['version'];
            DownloadPackage(args.package, version_build);
        else:
            args.diff = None;
            print 'Invalid arguments!';
            
        if args.diff != None:
            DownloadPackage(args.package, args.diff);
            first_package = os.path.join(os.path.abspath(os.path.dirname(__file__)), args.package+'-'+args.build);
            second_package = os.path.join(os.path.abspath(os.path.dirname(__file__)), args.package+'-'+args.diff);
            diff_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), args.package+'.diff');
            print 'Creating source diff...';
            diff_result = RunDiff(('diff', '-r', first_package, second_package), diff_path);
            print args.package+'.diff was created!';

if __name__ == "__main__":
    main(sys.argv[1:]);