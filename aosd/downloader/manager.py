import os
import urllib2
import gzip
import tarfile

class manager(object):
    
    @classmethod
    def CreateTarballURL(cls, release_type, package_name, build_number):
        return 'https://opensource.apple.com/tarballs/'+package_name+'/'+package_name+'-'+build_number+'.tar.gz';
    
    @classmethod
    def CreatePlistURL(cls, plist_name):
        return 'https://opensource.apple.com/plist/'+plist_name;
    
    @classmethod
    def DownloadPackageTarball(cls, release_type, package_name, build_number):
        tarball_address = manager.CreateTarballURL(release_type, package_name, build_number);
        package_file_name = os.path.basename(tarball_address);
        output_directory = os.path.expanduser('~/Downloads');
        output_file = os.path.join(output_directory, package_file_name)
        try:
            tarball = None;
            try: 
                tarball = urllib2.urlopen(tarball_address);
            except urllib2.HTTPError, e:
                print 'HTTPError = ' + str(e.code) + ' on ' + tarball_address;
                tarball = None;
            except urllib2.URLError, e:
                print 'URLError = ' + str(e.reason) + ' on ' + tarball_address;
                tarball = None;
            except httplib.HTTPException, e:
                print 'HTTPException' + ' on ' + tarball_address;
                tarball = None;
            except Exception:
                print 'Exception :( on ' + tarball_address;
                tarball = None;
            if tarball != None:
                output = open(output_file, 'wb');
                output.write(tarball.read());
                output.close();
            
            print 'Download Complete!';
            print 'Decompressing '+output_file+' -> '+package_file_name;
            gz_archive = gzip.open(output_file, 'rb');
            file_content = gz_archive.read();
            tar_path = os.path.join(output_directory, os.path.splitext(package_file_name)[0]);
            open(tar_path, 'w').write(file_content);
            gz_archive.close();
            os.remove(output_file);
            tar_archive = tarfile.open(tar_path);
            tar_archive.extractall(output_directory);
            tar_archive.close();
            os.remove(tar_path);
            print 'Decompression Complete!';
        except:
            print 'Could not find tarball!';
    
    @classmethod
    def DownloadPackageManifest(cls, cached_plist_file_path):
        plist_name = os.path.basename(cached_plist_file_path);
        plist_url = manager.CreatePlistURL(plist_name);
        if os.path.exists(cached_plist_file_path) == False:
            request = urllib2.Request(plist_url);
            response = None;
            try: 
                response = urllib2.urlopen(request);
            except urllib2.HTTPError, e:
                print 'HTTPError = ' + str(e.code) + ' on ' + plist_url;
                response = None;
            except urllib2.URLError, e:
                print 'URLError = ' + str(e.reason) + ' on ' + plist_url;
                response = None;
            except httplib.HTTPException, e:
                print 'HTTPException' + ' on ' + plist_url;
                response = None;
            except Exception:
                print 'Exception :( on ' + plist_url;
                response = None;
            if response != None:
                output = open(cached_plist_file_path, 'wb');
                output.write(response.read());
                output.close();
            
    @classmethod
    def RemovePackageManifest(cls, cached_plist_file_path):
        file_name = os.path.basename(cached_plist_file_path);
        if file_name != 'paackage_cache.plist' and file_name != 'cache.config' and file_name != 'aosd.config':
            if os.path.exists(cached_plist_file_path) == True:
                os.remove(cached_plist_file_path);