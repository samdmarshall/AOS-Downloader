import os
import sys
import argparse
import AOSD
# Main
def main(argv):
    parser = argparse.ArgumentParser();
    parser.add_argument('-t', '--type', help='specify the release type \'mac\', \'ios\', \'server\', \'dev\'', required=True, action='store');
    parser.add_argument('-v', '--version', help='specify the version number from a release type', action='store');
    args = parser.parse_args();
    
    AOSD_instance = AOSD.AOSD();
    
    if AOSD_instance.ValidateMapping([args.type, '']) == False:
        print 'Invalid release type. Please specify \'mac\', \'ios\', \'server\', or \'dev\' as the type.';
    else:
        packages = AOSD_instance.GetPackageListForVersion([args.type, args.version]);
        package_names = packages['projects'].keys();
        AOSD.MakeProjectsDir();
        for package in packages['projects']:
            AOSD.DownloadPackage(package,packages['projects'][package]['version']);

if __name__ == "__main__":
    main(sys.argv[1:]);