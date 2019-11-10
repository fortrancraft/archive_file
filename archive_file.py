#!/usr/bin/env python3

__author__      = 'Jeffrey R. Bell'
__license__     = "GPL-3.0"
__version__     = "0.1.0"
__status__      = "beta"
__description__ = 'utility to archive a file by renaming it with a time ' + \
                  'time stamp suffix, and moving it to an archive directory.'
__email__       = 'fortrancraft@gmail.com',
__url__         = 'https://github.com/fortrancraft/archive_file',

# Create an archive version of a file by adding a time stamp suffix
# to the file name, and move it to an archive directory, compress it, etc...


import argparse
import datetime
import gzip
import os
import shutil


def make_arg_parser():
    """Make an argument parser."""
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file',
        help='input the file to archive')

    parser.add_argument('--da', default='.',
        help='input a directory to move the archive file to.')

    parser.add_argument('--verbose', '-v', action='count', default=0,
        help='set the output printing verbosity level')

    parser.add_argument('--dry-run', action='store_true', default=False,
        help='execute the script without moving the input file')

    parser.add_argument('-z', '--gzip',
        action='store_true', default=False,
        help='compress the archived file in place with gzip')

    args = parser.parse_args()

    if args.verbose > 1:
        print('args.input_file = {}'.format(args.input_file))
        print('args.da         = {}'.format(args.da))
        print('args.verbose    = {}'.format(args.verbose))
        print('args.dry_run    = {}'.format(args.dry_run))
        print('args.gzip       = {}'.format(args.gzip))

    return args


def main():
    """Archive a file.
    """

    # Prepare for execution.
    args = make_arg_parser()
    if args.dry_run:
        drnote = ' (dry-run)'
    else:
        drnote = ''

    if not os.path.isfile(args.input_file):
        msg = 'Input file, "{}" does not exist!'.format(args.input_file)
        raise FileNotFoundError(msg)

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
    archive_name = file_name + '__{}'.format(tstr) + file_ext
    archive_file = os.path.join(args.da, archive_name)
    archive_file_gz = archive_file + '.gz'

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
        if args.gzip:
            print('archive_file_gz = {}'.format(archive_file_gz))

    # Move the file to the archive directory with the new name.
    if not args.dry_run:
        # Check if the file exists already to prevent over writing.
        if os.path.isfile(archive_file):
            msg = 'achive_file = {} alreadys exists!'.format(archive_file)
            raise FileExistsError(msg)
        else:
            # Move the file to the archive directory.
            shutil.move(args.input_file, archive_file)

            # Compress the file if requested.
            if args.gzip:
                with open(archive_file, 'rb') as f_in:
                    with gzip.open(archive_file_gz, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(archive_file)

    # Check if the file move was successful.
    if args.dry_run:
        pass
    else:
        if args.gzip:

            # Check if the file move and compression worked.
            if not os.path.isfile(archive_file_gz):
                msg = 'Failed to archive and compress the file!'
                raise FileNotFoundError(msg)

        else:

            # Check if the file move worked.
            if not os.path.isfile(archive_file):
                msg = 'Failed to archive the file!'
                raise FileNotFoundError(msg)


    if args.gzip:
        out_fmt = 'moved and compressed {} to {}{}'
        print(out_fmt.format(args.input_file, archive_file_gz, drnote))
    else:
        out_fmt = 'moved {} to {}{}'
        print(out_fmt.format(args.input_file, archive_file, drnote))

if __name__ == "__main__":
    main()
