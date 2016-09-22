vboxupdater
===========
This script downloads a vagrantbox and a checksumfile.

After download it calculates the checksum of the downloaded vagrantbox and checks if it matches the one given from
in the sha256sum text file.

If it matches, the vagrantbox is assumed ok and renamed, otherwise its deleted from the filesystem.

Tested on Mac OSX 10.11 and Redhat Enterprise Linux 7.

todo
====
* Rewrite it with a configuration file to avoid hardcoded URLs
* Add some try/except to catch error conditions. If something
goes woo the script will probably just crash. Not cool.

copyright
=========
2016, Kristian Botnen