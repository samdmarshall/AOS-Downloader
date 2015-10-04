# Apple Open Source Downloader (aosd)

This utility makes it easy to find and download various versions of the open source code that Apple provides on https://opensource.apple.com.

---

## Requirements

####Python 2.7
* Modules used:
	* argparse
	* sys
	* os
	* plistlib
	* urllib2
	* httplib
	* urlparse
	* readline (this uses a custom readline implementation on OS X)
	* gzip
	* tarfile
	* logging
	* hashlib
	* subprocess
	* string


####Python 3.4
* Modules used:
	* argparse
	* sys
	* os
	* plistlib
	* urllib
	* http
	* readline (this uses a custom readline implementation on OS X)
	* gzip
	* tarfile
	* logging
	* hashlib
	* subprocess
	* string

---

## Installation

### From Source

Checkout this repo then run `python setup.py install` and optionally pass the `--user` flag if desired.

*Note: you may have to configure your `$PATH` variable to find the executable once installed.*

### Homebrew

	$ brew update
	$ brew tap samdmarshall/formulae
	$ brew install samdmarshall/formulae/aosd # you can optionally supply --HEAD here, though be aware that it can be unstable

---

## Usage

Once installed, the executable will be called `aosd`.

### Command Console

The application's command console will give you full access to all of the features of `aosd`. To enter the console run the binary with no flags passed. To get usage information use the `help` command.

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


---


## Submitting Updates

### Release Updates

Unlike the previous version, the code of `aosd` does not need to be updated to support new open source releases. Releases are now cateloged in plist files that ship with each distribution. To update these files to the latest version, you can run the `update` command in the command console. You can also point `aosd` at your own versions of the plists by modifying the `core_url` setting in the config.

* Releases: https://github.com/samdmarshall/AOS-Downloader/tree/master/aosd/data/releases.plist
* OS X: https://github.com/samdmarshall/AOS-Downloader/tree/master/aosd/data/mac.plist
* iOS: https://github.com/samdmarshall/AOS-Downloader/tree/master/aosd/data/ios.plist
* Developer Tools: https://github.com/samdmarshall/AOS-Downloader/tree/master/aosd/data/dev.plist
* OS X Server: https://github.com/samdmarshall/AOS-Downloader/tree/master/aosd/data/server.plist

The `releases.plist` dictates what release types there are. 

* Key: `package_name` 
* Value: This must be the same as the release index plist name. 

* Key: `display_name`
* Value: This is the name shown on the command console when selecting a release type.

Each of the release type plists (`mac`, `ios`, `dev`, `server`) consists of an array that is ordered from newest (first index) to oldest (last index). Each element in the array is a dictionary that contains 3 key-value pairs:

* Key: `name`
* Value: Display name of the release, this should correspond with the human readable number on main page of opensource.apple.com

* Key: `version`
* Value: The version number used for the release. To find this, please check the URL of the package list link for the specific release.

* Key: `prefix`
* Value: This is the prefix to the specific release version based on the release type. To find this, please check the URL of the package list link for the specific release.


Example:

	https://opensource.apple.com/release/developer-tools-63/


	https://opensource.apple.com/release/<prefix>-<version>/


In this case:

* `prefix`=`developer-tools` 
* `version`=`63`
* `name`=`6.3`


When you are submitting a release update, please also update the [hashes.plist](asod/data/hashes.plist) file to include the sha256 (`shasum -a 256 <file>`) of the `.tar.gz` file.
### Code Updates

Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines of how to make pull requests and submit changes to the code. 