    >>> import os
    >>> import tempfile
    >>> import shutil

    >>> from nose.util import ls_tree

    >>> dir_path = tempfile.mkdtemp()

    >>> def create_file(filename):
    ...     fd = os.open(filename, os.O_WRONLY|os.O_CREAT, 0666)
    ...     os.close(fd)

    >>> os.mkdir(os.path.join(dir_path, "top"))
    >>> os.mkdir(os.path.join(dir_path, "top/dir"))
    >>> os.mkdir(os.path.join(dir_path, "top/dir2"))
    >>> os.mkdir(os.path.join(dir_path, "top/dir3"))
    >>> os.mkdir(os.path.join(dir_path, "top/dir/dir"))
    >>> os.mkdir(os.path.join(dir_path, "top/dir/dir2"))
    >>> os.mkdir(os.path.join(dir_path, "top/.svn"))
    >>> os.mkdir(os.path.join(dir_path, "top/.notsvn"))
    >>> os.mkdir(os.path.join(dir_path, "top/dir/.svn"))
    >>> os.mkdir(os.path.join(dir_path, "top/dir/.notsvn"))
    >>> create_file(os.path.join(dir_path, "top/file"))
    >>> create_file(os.path.join(dir_path, "top/backup_file~"))
    >>> create_file(os.path.join(dir_path, "top/file2"))
    >>> create_file(os.path.join(dir_path, "top/dir/file"))
    >>> create_file(os.path.join(dir_path, "top/dir/dir/file"))
    >>> create_file(os.path.join(dir_path, "top/dir/dir/file2"))
    >>> create_file(os.path.join(dir_path, "top/dir/backup_file~"))
    >>> create_file(os.path.join(dir_path, "top/dir2/file"))

    Note that files matching skip_pattern (by default SVN files,
    backup files and compiled Python files) are ignored

    >>> print ls_tree(os.path.join(dir_path, "top"))
    |-- file
    |-- file2
    |-- .notsvn
    |-- dir
    |   |-- file
    |   |-- .notsvn
    |   |-- dir
    |   |   |-- file
    |   |   `-- file2
    |   `-- dir2
    |-- dir2
    |   `-- file
    `-- dir3

    >>> shutil.rmtree(dir_path)
