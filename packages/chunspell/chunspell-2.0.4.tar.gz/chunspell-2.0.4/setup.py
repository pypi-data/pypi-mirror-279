import os
import sys
import glob
import shutil
import platform
from warnings import warn
from setuptools import setup, find_packages, Extension
from distutils.command.build import build
from build_hunspell import pkgconfig, repair_darwin_link_dep_path
from collections import defaultdict

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            self.root_is_pure = False
except ImportError:
    print("Could not register bdist_wheel. Make sure the wheel package is installed!")
    bdist_wheel = None


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BUILD_ARGS = defaultdict(lambda: ['-O3', '-g0'])
for compiler, args in [
        ('msvc', ['/EHsc', '/MD', '/DHUNSPELL_STATIC']),
        ('gcc', ['-O3', '-g0', '-DHUNSPELL_STATIC'])]:
    BUILD_ARGS[compiler] = args

def cleanup_pycs():
    file_tree = os.walk(os.path.join(BASE_DIR, 'hunspell'))
    to_delete = []
    for root, directory, file_list in file_tree:
        if len(file_list):
            for file_name in file_list:
                if file_name.endswith(".pyc"):
                    to_delete.append(os.path.join(root, file_name))
    for file_path in to_delete:
        try:
            os.remove(file_path)
        except:
            pass

def read(fname):
    with open(fname, 'r') as fhandle:
        return fhandle.read()

profiling = '--profile' in sys.argv or '-p' in sys.argv
linetrace = '--linetrace' in sys.argv or '-l' in sys.argv
building_ext = 'build_ext' in sys.argv
force_rebuild = '--force' in sys.argv or '-f' in sys.argv and building

datatypes = ['*.aff', '*.dic', '*.pxd', '*.pyx', '*.pyd', '*.pxd', '*.so', '*.so.*', '*.dylib', '*.dylib.*', '*.lib', '*.hpp', '*.cpp']
packages = find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests'])
packages.append('hunspell.dictionaries')
package_data = {'' : datatypes}

if building_ext:
    if (profiling or linetrace) and not force_rebuild:
        warn("WARNING: profiling or linetracing specified without forced rebuild")
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext

    ext_modules = cythonize([
        Extension(
            'hunspell.hunspell',
            [os.path.join('hunspell', 'hunspell.pyx')],
            **pkgconfig()
        )
    ], force=force_rebuild, compiler_directives={'language_level' : "3"})
else:
    from setuptools.command.build_ext import build_ext
    ext_modules = [
        Extension(
            'hunspell.hunspell',
            [os.path.join('hunspell', 'hunspell.cpp')],
            **pkgconfig()
        )
    ]

class build_ext_compiler_check(build_ext):
    def build_extensions(self):
        compiler = self.compiler.compiler_type
        args = BUILD_ARGS[compiler]
        for ext in self.extensions:
            ext.extra_compile_args = args
        build_ext.build_extensions(self)

    def run(self):
        cleanup_pycs()
        build_ext.run(self)

class build_darwin_fix(build):
    def run(self):
        build.run(self)
        # OSX build a shared dependency with an absolute path to the hunspell dylib. This fixes that
        if platform.system() == 'Darwin':
            repair_darwin_link_dep_path()

def version():
    with open(os.path.join(BASE_DIR, 'hunspell', '_version.py'), 'r') as ver:
        for line in ver.readlines():
            if line.startswith('__version__ ='):
                return line.split(' = ')[-1].strip()[1:-1]
    raise ValueError('No version found in hunspell/_version.py')

setup(
    name='chunspell',
    version=version(),
    author='cdhigh',
    author_email='akindleear@gmail.com',
    description='A wrapper on hunspell for use in Python',
    long_description=read(os.path.join(BASE_DIR, 'README.md')),
    long_description_content_type='text/markdown',
    ext_modules=ext_modules,
    cmdclass={ 'build_ext': build_ext_compiler_check, 'build': build_darwin_fix, 'bdist_wheel': bdist_wheel },
    license='MIT + MPL 1.1/GPL 2.0/LGPL 2.1',
    packages=packages,
    test_suite='tests',
    zip_safe=False,
    url='https://github.com/cdhigh/chunspell',
    download_url='https://github.com/cdhigh/chunspell/tarball/v' + version(),
    package_data=package_data,
    keywords=['hunspell', 'spelling', 'correction'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ]
)
