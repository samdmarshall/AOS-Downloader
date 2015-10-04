from setuptools import setup

setup(
    name='aosd',
    version='1.0',
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
    zip_safe=False
)