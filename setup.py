module_dependencies = []
module_version = '1.0.1'
try:
    import sys
    if not sys.version_info > (2, 7):
        print('This software requires that you be running at least Python 2.7')
        sys.exit()
    else:
        shared_dependencies = ['argparse', 'sys', 'platform', 'os', 'cmd', 'plistlib', 'string', 'subprocess', 'hashlib', 'logging', 'gzip', 'tarfile', 'readline']
        python_2_dependencies = shared_dependencies + ['urllib2', 'httplib', 'urlparse']
        python_3_dependencies = shared_dependencies + ['urllib', 'http']
        install_dependency_list = None
        if sys.version_info.major == 2:
            install_dependency_list = python_2_dependencies
        if sys.version_info.major == 3:
            install_dependency_list = python_3_dependencies
    
        if install_dependency_list == None:
            print('Error in checking python version!')
        else:
            found_modules = {}
            for dependency in install_dependency_list:
                try:
                    found_modules[dependency] = __import__(dependency)
                except ImportError:
                    module_dependencies.append(dependency)
except ImportError as e:
    raise e
 
install_requires_dict = {'install_requires': module_dependencies}

try:
    import os
    import subprocess
    def make_call(call_args):
        error = 0
        output = ''
        try:
            output = subprocess.check_output(call_args)
            error = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            error = e.returncode
        return output

    install_path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(install_path)
    commit_hash = str(make_call(('git', 'rev-parse', '--short', 'HEAD'))).strip('\n')
    remote_origin = str(make_call(('git', 'ls-remote', '--get-url'))).strip('\n')
    versions_path = os.path.join(install_path, 'aosd/version.py')
    fd = open(versions_path, 'w')
    fd.write('__version__ = "'+module_version+' ('+remote_origin+' @ '+commit_hash+')"')
    fd.close()
except ImportError as e:
    raise e
 
try:
    from setuptools import setup

    setup(
        name='aosd',
        version=module_version,
        description='Apple Open Source Package Downloader',
        url='https://github.com/samdmarshall/AOS-Downloader',
        author='Samantha Marshall',
        author_email='hello@pewpewthespells.com',
        license='BSD 3-Clause',
        package_data = { 
            'aosd/commandparse/readline_unsorted': [
                'readline.so', 
                'libedit-unsorted.3.dylib'
            ],
        
            'aosd/data': [
                '*.plist'
            ], 
        
            'aosd/data/cache': [
                'package_cache.plist'
            ] 
        },
        packages=[
            'aosd', 
        
            'aosd/commandparse', 
            'aosd/commandparse/readline_unsorted', 
        
            'aosd/downloader', 
        
            'aosd/data', 
            'aosd/data/cache'
        ],
        entry_points = {
            'console_scripts': ['aosd = aosd:main'],
        },
        zip_safe=False,
        **install_requires_dict
    )
except ImportError as e:
    raise e