Create an archive version of a file by adding a time stamp suffix
to the file name, and moving it to an archive directory, and
optionally compressing it as well.

Examples:

    >>> ./archive_file.py ex_file.txt --da=archives/ --dry-run
        created directory : archives/ (dry-run)
        moved ex_file.txt to archives/ex_file__20190921T1514.txt (dry-run)

    >>> ./archive_file.py ex_file.txt --da=archives/ --dry-run -v
        created directory : archives/ (dry-run)

        file_dir    =
        basename    = ex_file.txt
        file_name   = ex_file
        file_ext    = .txt

        archive_name = ex_file__20190921T1514.txt
        archive_file = archives/ex_file__20190921T1514.txt
        moved ex_file.txt to archives/ex_file__20190921T1514.txt (dry-run)

    >>> ./archive_file.py ex_file.txt --da=archives/
        created directory : archives/
        moved ex_file.txt to archives/ex_file__20190921T1514.txt

    >>> ./archive_file.py ex_file2.txt --da=archives/
        moved ex_file2.txt to archives/ex_file2__20190921T1520.txt

    >>> ./archive_file.py ex_file3.txt --da=archives/ -v --gzip
 
        file_dir    = 
        basename    = ex_file3.txt
        file_name   = ex_file3
        file_ext    = .txt
 
        archive_name = ex_file3__20191110T1535.txt
        archive_file = archives/ex_file3__20191110T1535.txt
        archive_file_gz = archives/ex_file3__20191110T1535.txt.gz
        moved and compressed ex_file3.txt to archives/ex_file3__20191110T1535.txt.gz

