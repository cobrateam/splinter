import sys
from setuptools import setup as _setup

py3_args = ['use_2to3', 'convert_2to3_doctests', 'use_2to3_fixers', 'test_dirs', 'test_build_dir', 'doctest_exts', 'pyversion_patching']

if sys.version_info < (3,):
    # Remove any Python-3.x-only arguments (so they don't generate complaints
    # from 2.x setuptools) and then just pass through to the regular setup
    # routine.
    def setup(*args, **kwargs):
        for a in py3_args:
            if a in kwargs:
                del kwargs[a]
        return _setup(*args, **kwargs)
else:
    import os
    import re
    import logging
    from setuptools import Distribution as _Distribution
    from distutils.core import Command
    from setuptools.command.build_py import Mixin2to3
    from distutils import dir_util, file_util, log
    import setuptools.command.test
    from pkg_resources import normalize_path
    try:
        import patch
        patch.logger.setLevel(logging.WARN)
    except ImportError:
        patch = None

    patchfile_re = re.compile(r'(.*)\.py([0-9.]+)\.patch$')

    def pyversion_patch(filename):
        '''Find the best pyversion-fixup patch for a given filename and apply
           it.
        '''
        dir, file = os.path.split(filename)
        best_ver = (0,)
        patchfile = None
        for dirfile in os.listdir(dir):
            m = patchfile_re.match(dirfile)
            if not m:
                continue
            base, ver = m.groups()
            if base != file:
                continue
            ver = tuple([int(v) for v in ver.split('.')])
            if sys.version_info >= ver and ver > best_ver:
                best_ver = ver
                patchfile = dirfile
        if not patchfile:
            return False
        log.info("Applying %s to %s..." % (patchfile, filename))
        cwd = os.getcwd()
        os.chdir(dir)
        try:
            p = patch.fromfile(patchfile)
            p.apply()
        finally:
            os.chdir(cwd)
        return True

    class Distribution (_Distribution):
        def __init__(self, attrs=None):
            self.test_dirs = []
            self.test_build_dir = None
            self.doctest_exts = ['.py', '.rst']
            self.pyversion_patching = False
            _Distribution.__init__(self, attrs)

    class BuildTestsCommand (Command, Mixin2to3):
        # Create mirror copy of tests, convert all .py files using 2to3
        user_options = []

        def initialize_options(self):
            self.test_base = None

        def finalize_options(self):
            test_base = self.distribution.test_build_dir
            if not test_base:
                bcmd = self.get_finalized_command('build')
                test_base = bcmd.build_base
            self.test_base = test_base

        def run(self):
            use_2to3 = getattr(self.distribution, 'use_2to3', False)
            test_dirs = getattr(self.distribution, 'test_dirs', [])
            test_base = self.test_base
            bpy_cmd = self.get_finalized_command("build_py")
            lib_base = normalize_path(bpy_cmd.build_lib)
            modified = []
            py_modified = []
            doc_modified = []
            dir_util.mkpath(test_base)
            for testdir in test_dirs:
              for srcdir, dirnames, filenames in os.walk(testdir):
                destdir = os.path.join(test_base, srcdir)
                dir_util.mkpath(destdir)
                for fn in filenames:
                    if fn.startswith("."):
                        # Skip .svn folders and such
                        continue
                    dstfile, copied = file_util.copy_file(
                                          os.path.join(srcdir, fn),
                                          os.path.join(destdir, fn),
                                          update=True)
                    if copied:
                        modified.append(dstfile)
                        if fn.endswith('.py'):
                            py_modified.append(dstfile)
                        for ext in self.distribution.doctest_exts:
                            if fn.endswith(ext):
                                doc_modified.append(dstfile)
                                break
            if use_2to3:
                self.run_2to3(py_modified)
                self.run_2to3(doc_modified, True)
            if self.distribution.pyversion_patching:
                if patch is not None:
                    for file in modified:
                        pyversion_patch(file)
                else:
                    log.warn("Warning: pyversion_patching specified in setup config but patch module not found.  Patching will not be performed.")

            dir_util.mkpath(lib_base)
            self.reinitialize_command('egg_info', egg_base=lib_base)
            self.run_command('egg_info')

    class TestCommand (setuptools.command.test.test):
        # Override 'test' command to make sure 'build_tests' gets run first.
        def run(self):
            self.run_command('build_tests')
            setuptools.command.test.test.run(self)

    def setup(*args, **kwargs):
        kwargs.setdefault('distclass', Distribution)
        cmdclass = kwargs.setdefault('cmdclass', {})
        cmdclass.setdefault('build_tests', BuildTestsCommand)
        cmdclass.setdefault('test', TestCommand)
        return _setup(*args, **kwargs)
