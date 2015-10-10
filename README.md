# Apple Open Source Downloader (aosd)

This utility makes it easy to find and download various versions of the open source code that Apple provides on https://opensource.apple.com.

---

## Requirements

Python 2.7 or greater (this does support Python 3), running the `setup.py` will determine if you need to install anything else.

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


### Wiki

Please see the [wiki](https://github.com/samdmarshall/AOS-Downloader/wiki) for more information!