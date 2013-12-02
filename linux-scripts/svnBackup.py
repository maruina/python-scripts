#! /usr/bin/env python
#
# Backup SVN folders given parent folder
#

# Import libraries
import os
import sys
import subprocess
import datetime
import argparse


def getTimestamp():
    now = datetime.datetime.now()
    timestamp = (
        str(now.year) + str(now.month) + str(now.day) + str(now.hour) +
        str(now.minute) + str(now.second)
    )
    return timestamp


def dirVerify(directory):
    if os.path.exists(directory):
        return True
    else:
        return False


def svnVerify(repository):
    """Check if repo is a valid SVN repository """
    try:
        p = (
            subprocess.Popen(
                ['svnadmin', 'verify', repository],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        )
        if p.returncode == 1:
            print (
                "ERROR: %s is not a valid SVN repository."
                "Removing from list" % repository
            )
            return False
        elif p.returncode == 0:
            print "OK: %s is a valid SVN repository" % repository
            return True
    except subprocess.OSError as e:
        print "Error: %s" % e
        return False


def parseArguments():
    parser = (
        argparse.ArgumentParser(description='Backup SVN repository to a destination folder')
    )

    # Read the arguments
    parser.add_argument(
        '-r', '--repository', help='Source repository', required=True
    )
    parser.add_argument(
        '-d', '--destination', help='Destination folder', required=True
    )

    args = parser.parse_args()

    return args


def svnBackup(repository, dstdir):
    """Backup a SVN repository to a destination folder."""
    if svnVerify(repository) is False:
        print "Error: %s is not a valid SVN repository" % repository
        sys.exit(1)

    if dirVerify(dstdir) is False:
        print "Error: %s does not exists" % dstdir
        sys.exit(2)

    # Find the paths
    abs_repository = os.path.abspath(repository)
    abs_dstdir = os.path.abspath(dstdir)
    timestamp = getTimestamp()

    # Create destination folder based on repository name and timestamp
    repository_name = os.path.basename(os.path.normpath(abs_repository))
    bkpdir = abs_dstdir + "/" + repository_name + "-" + timestamp
    try:
        os.makedirs(bkpdir)
    except os.error as e:
        print "Error: can not create %s directory" % bkpdir
        print e
        sys.exit(3)

    # Backup the repository
    p = (
        subprocess.Popen(
            ['svnadmin', 'hotcopy', abs_repository, bkpdir],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    )
    if p.returncode == 0:
        print "Backup of %s repository in progress" % repository_name
    else:
        print "Error: backup failed"

    if svnVerify(bkpdir) is True:
        print "Backup complete"
    else:
        print "Error: can not verify the repository backup"

    return True


if __name__ == '__main__':

    # Parse the script's arguments
    args = parseArguments()

    svnBackup(args.repository, args.destination)
