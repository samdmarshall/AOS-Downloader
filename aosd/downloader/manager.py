from ..logging_helper import *

import os
try:
    import urllib.request as comp_urlreq # For Python 3.0 and later
    import urllib.error as compat_urlerr
    import http.client as compat_http
except ImportError:
    import urllib2 as comp_urlreq # Fall back to Python 2's urllib2
    import urllib2 as comp_urlerr
    import httplib as compat_http
    
import gzip
import tarfile

from .config import *

class manager(object):
    
    @classmethod
    def CreateTarballURL(cls, release_type, package_name, build_number):
        default_url = 'https://opensource.apple.com/tarballs/'+package_name+'/'+package_name+'-'+build_number+'.tar.gz';
        parsed_url = urlparse.urlparse(default_url);
        if config.getUseHTTPS() == False:
            parsed_url.scheme = 'http';
        return parsed_url.geturl();
    
    @classmethod
    def CreatePlistURL(cls, plist_name):
        default_url = 'https://opensource.apple.com/plist/'+plist_name;
        parsed_url = urlparse.urlparse(default_url);
        if config.getUseHTTPS() == False:
            parsed_url.scheme = 'http';
        return parsed_url.geturl();
    
    @classmethod
    def DownloadFileFromURLToPath(cls, url_address, file_path):
        request = comp_urlreq.Request(url_address);
        if config.getVerboseLogging() == True:
            logging_helper.getLogger().info(': Starting download from  "'+url_address+'" -> "'+file_path+'"...');
        response = None;
        try: 
            response = comp_urlreq.urlopen(request);
        except comp_urlerr.HTTPError as e:
            logging_helper.getLogger().error(': HTTPError = '+str(e.code)+' on '+url_address);
            response = None;
        except comp_urlerr.URLError as e:
            logging_helper.getLogger().error(': URLError = '+ str(e.reason)+' on '+url_address);
            response = None;
        except compat_http.HTTPException as e:
            logging_helper.getLogger().error(': HTTPException on '+url_address);
            response = None;
        except Exception:
            logging_helper.getLogger().error(':Exception :( on '+url_address);
            response = None;
        if response != None:
            output = open(file_path, 'wb');
            output.write(response.read());
            output.close();
            if config.getVerboseLogging() == True:
                logging_helper.getLogger().info(': Download Complete!');
        
    @classmethod
    def DownloadPackageTarball(cls, release_type, package_name, build_number):
        tarball_address = manager.CreateTarballURL(release_type, package_name, build_number);
        package_file_name = os.path.basename(tarball_address);
        output_directory = os.path.expanduser(config.getDownloadDir());
        output_file = os.path.join(output_directory, package_file_name)
        try:
            cls.DownloadFileFromURLToPath(tarball_address, output_file);
            if config.getVerboseLogging() == True:
                logging_helper.getLogger().info(': Decompressing "'+output_file+'" -> "'+package_file_name+'"...');
            gz_archive = gzip.open(output_file, 'rb');
            file_content = gz_archive.read();
            tar_name = os.path.splitext(package_file_name)[0];
            tar_path = os.path.join(output_directory, tar_name);
            open(tar_path, 'w').write(file_content);
            gz_archive.close();
            os.remove(output_file);
            tar_archive = tarfile.open(tar_path);
            tar_archive.extractall(output_directory);
            tar_archive.close();
            if config.getVerboseLogging() == True:
                logging_helper.getLogger().info(': Decompression Complete!');
            os.remove(tar_path);
            file_name = os.path.splitext(tar_name)[0];
            logging_helper.getLogger().info(': The package "'+file_name+'" has been downloaded to "'+output_directory+'".');
        except:
            logging_helper.getLogger().error(': Could not find tarball!');
    
    @classmethod
    def DownloadPackageManifest(cls, cached_plist_file_path):
        plist_name = os.path.basename(cached_plist_file_path);
        plist_url = manager.CreatePlistURL(plist_name);
        if os.path.exists(cached_plist_file_path) == False:
            cls.DownloadFileFromURLToPath(plist_url, cached_plist_file_path);
            
    @classmethod
    def RemovePackageManifest(cls, cached_plist_file_path):
        file_name = os.path.basename(cached_plist_file_path);
        if file_name != 'paackage_cache.plist' and file_name != 'cache.config' and file_name != 'aosd.config':
            if os.path.exists(cached_plist_file_path) == True:
                os.remove(cached_plist_file_path);