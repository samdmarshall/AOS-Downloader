from setuptools import setup

setup(
    name='aosd',
    version='1.0',
    description='Apple Open Source Package Downloader',
    url='https://github.com/samdmarshall/AOS-Downloader',
    author='Sam Marshall',
    author_email='sam@pewpewthespells.com',
    license='BSD 3-Clause',
    packages=['aosd', 'aosd/commandparse', 'aosd/downloader'],
    entry_points = {
        'console_scripts': ['aosd = aosd:main'],
    },
    zip_safe=False
)