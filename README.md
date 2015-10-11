# Apple Open Source Downloader (aosd)

This utility makes it easy to find and download various versions of the open source code that Apple provides on https://opensource.apple.com.

---

## Requirements

Python 2.7 or greater (this does support Python 3), running the `setup.py` will determine if you need to install anything else.

---

## Installation

Via [homebrew](http://brew.sh):

	$ brew update
	$ brew tap samdmarshall/formulae
	$ brew install samdmarshall/formulae/aosd

For instructions on installing from source or from the development version via homebrew, please see the [Installing](https://github.com/samdmarshall/AOS-Downloader/wiki/Installing) instructions on the wiki.

---

## Usage

Once installed, the executable will be called `aosd`.

### Command Console

The application's command console will give you full access to all of the features of `aosd`. To enter the console run the binary with no flags passed. To get usage information use the `help` command. For more information, please check out the [guided tutorial](https://github.com/samdmarshall/AOS-Downloader/wiki/Tutorial) on the wiki.

### Flags

	-h, --help                         show help message and exit
	-t TYPE, --type TYPE               specify the release type
	-l, --list                         list versions of a package to check out, if no package is specified it lists available packages
	-p PACKAGE, --package PACKAGE      specify the name of a package from a release
	-b BUILD, --build BUILD            specify the build number from a package
	-d DIFF DIFF, --diff DIFF DIFF     specify the build number of a package to create diff against
	-r, --resetcache                   removes currently cached package plist files
	-c, --buildcache                   caches the package manifests and builds an index
	-f, --findhash					   this will display the sha256 for the specified build of a package
	-v, --version					   this will display the build version of AOSD


---


### More Information

Please see the [wiki](https://github.com/samdmarshall/AOS-Downloader/wiki) for more information!