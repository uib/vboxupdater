#!/usr/bin/python#!/usr/bin/python
# coding=utf-8
#
# Author: Kristian Botnen <kristian.botnen@uib.no>
#
#
# This script downloads a vagrantbox and a checksumfile.
#
# After download it calculates the checksum of the downloaded vagrantbox and checks if it matches the one given from
# in the sha256sum text file.
#
# If it matches, the vagrantbox is assumed ok and renamed, otherwise its deleted from the filesystem.
#
# Tested on Mac OSX 10.11 and Redhat Enterprise Linux 7.
#

import os
import urllib
import hashlib

sha256sum_url = 'http://cloud.centos.org/centos/7/vagrant/x86_64/images/'
sha256sum_name = 'sha256sum.txt'
vagrantbox_url = 'http://cloud.centos.org/centos/7/vagrant/x86_64/images/'
vagrantbox_name = 'CentOS-7.box'
vagrantbox_tmpname = 'CentOS-7.box.notverified'

def retrieve_file(url, file):
    ''' Retrieve a file from a URL, save it to disk

    Paremeters
    ----------
    url : str
        The URL to the file that we want to download
    file : str
        The path + filename + extension where we want to save the downloaded file

    Returns
    -------
    None

    '''
    afile = urllib.URLopener()
    afile.retrieve(url, file)

def lookup_checksum(checksumfile, checksumitem):
    ''' Check if a given checksum exist in a textfile

    Paremeters
    ----------
    checksumfile : str
        A file that contains checksums in the format 'a83803df6b48fd311eb0a0af01cd4df220815ba574dc409249e7948ad5149277  centos-7-atomicapp-dev-1-1.x86_64.qcow2'.
    checksumitem : str
        The checksum that we want to search for inside checksumfile, i.e 'a83803df6b48fd311eb0a0af01cd4df220815ba574dc409249e7948ad5149277'.

    Returns
    -------
    return_value : bool
        True if we find the checksumitem inside the checksumfile, False otherwise.

    '''
    return_value = False
    checksum = {}

    with open(checksumfile) as f:
        for line in f:
            aobject = line.strip().split(' ')
            checksum[aobject[0]] = aobject[2]

    try:
        return_value = checksum[checksumitem]
        if return_value is not '':
            return_value = True
    except KeyError as ke:
        return_value = False

    return return_value


def calculate_sha256(filename):
    ''' Calculate the sha256hash of a given file.

    Paremeters
    ----------
    filename : str
        The URL to the file that we want to calculate the sha256hash on.

    Returns
    -------
    str
        A string representation of the sha256sum (double length, containing only hexadecimal digits).

    '''
    hash_sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        for blocks in iter(lambda: f.read(4096), b""):
            hash_sha256.update(blocks)
    return hash_sha256.hexdigest()


if __name__ == '__main__':
    # Get a file with checksums + the vagrantbox.
    retrieve_file(sha256sum_url + sha256sum_name, sha256sum_name)
    retrieve_file(vagrantbox_url + vagrantbox_name, vagrantbox_tmpname)

    # Calculate sha256 of the vagrantbox.
    calculated_checksum = calculate_sha256(vagrantbox_tmpname)
    # Check if the calculated checksum exist in the downloaded list of checksums.
    if (lookup_checksum(sha256sum_name, calculated_checksum)):
        os.rename(vagrantbox_tmpname, vagrantbox_name)
    else:
        os.remove(vagrantbox_tmpname)
