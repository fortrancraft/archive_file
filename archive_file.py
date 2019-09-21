#!/usr/bin/env python3

__author__      = 'Jeffrey R. Bell'
__license__     = "GPL-3.0"
__version__     = "0.0.0"
__status__      = "beta"
__description__ = 'utility to archive a file by renaming it with a time ' + \
                  'time stamp suffix, and moving it to an archive directory.'
__email__       = 'fortrancraft@gmail.com',
__url__         = 'https://github.com/fortrancraft/archive_file',

# Create an archive version of a file by adding a time stamp suffix
# to the file name, and move it to an archive directory.
#
# JRB 2019/09/21

import argparse
import datetime
import os
import shutil


def make_arg_parser():
    """Make an argument parser."""
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file',
        help='Input the file to archive')

    parser.add_argument('--da', default='.',
        help='Input a directory to move the archive file to.')

    parser.add_argument('--verbose', '-v', action='count', default=0,
        help='Set the output printing verbosity level')

    parser.add_argument('--dry-run', action='store_true', default=False,
        help='Execute the script without moving the input file')

    args = parser.parse_args()

    if args.verbose > 1:
        print('args.input_file = {}'.format(args.input_file))
        print('args.da         = {}'.format(args.da))
        print('args.verbose    = {}'.format(args.verbose))
        print('args.dry_run    = {}'.format(args.dry_run))

    return args


def main():
    """Archive a file by appending a time stamp to the file's name, and
       moving it to an archive directory.
    """

    # Prepare for execution.
    args = make_arg_parser()
    if args.dry_run:
        drnote = ' (dry-run)'
    else:
        drnote = ''

    # Create the directory destination if it does not exist.
    if not os.path.isdir(args.da):
        if not args.dry_run:
            os.makedirs(args.da)
        print('created directory : {}{}'.format(args.da, drnote))

    # Split the file name into a path, name and extension.
    file_dir = os.path.dirname(args.input_file)
    basename = os.path.basename(args.input_file)
    file_name, file_ext = os.path.splitext(basename)

    # Get metadata information from the file.
    file_info = os.stat(args.input_file)
    tstr = datetime.datetime.fromtimestamp(file_info.st_mtime)\
        .strftime('%Y%m%dT%H%M')

    # Create the archive file name and path.
    archive_name = file_name + '__{}{}'.format(tstr, file_ext)
    archive_file = os.path.join(args.da, archive_name)

    if args.verbose > 0:
        print(' ')
        print('file_dir    = {}'.format(file_dir))
        print('basename    = {}'.format(basename))
        print('file_name   = {}'.format(file_name))
        print('file_ext    = {}'.format(file_ext))
        print(' ')
        if args.verbose > 1:
            print('file_info   = {}'.format(file_info))
            print('tstr        = {}'.format(tstr))
        print('archive_name = {}'.format(archive_name))
        print('archive_file = {}'.format(archive_file))

    # Move the file to the archive directory with the new name.
    if not args.dry_run:
        # Check if the file exists already to prevent over writing.
        if os.path.isfile(archive_file):
            msg = 'achive_file = {} alreadys exists!'.format(archive_file)
            raise FileExistsError(msg)
        else:
            shutil.move(args.input_file, archive_file)

    # Check if the file move was successful.
    if args.dry_run:
        pass
    else:
        if not os.path.isfile(archive_file):
            msg = 'Failed to archive the file! File move unsuccessful.'
            raise FileNotFoundError(msg)

    print('moved {} to {}{}'.format(args.input_file, archive_file, drnote))

if __name__ == "__main__":
    main()
