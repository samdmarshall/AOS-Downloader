#Apple Open Source Downloader

This script allows for query and fetching of various open source releases from opensource.apple.com.

###Usage:

	$ python fetch.py [-h] -t TYPE [-l] [-v VERSION] [-p PACKAGE] [-b BUILD]

* TYPE
  * mac - Query OS X releases
  * ios - Query iOS releases
  * dev - Query Developer Tool releases
  * server - Query OS X Server releases

* VERSION 
  * the release version to query a package list of

* PACKAGE
  * the name of the package to query

* BUILD
  * the build number of the package to download
