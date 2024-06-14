from setuptools import setup, find_packages

from setuptools.command.test import test as test_command
import sys


class PyTest(test_command):
    # This class will tell setuptools to run pytest
    def run_tests(self):
        # Import here, because outside the eggs aren't loaded
        import pytest
        errno = pytest.main(['test'])  # Pointing to your test directory or files
        sys.exit(errno)


setup(
    name='HandyPython',  # Replace with your project name
    version='0.1',  # Initial version
    author='puyanh',
    author_email='whatsbehind1@gmail.com',
    description='A Python tool kit',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # For Markdown README files
    url='https://github.com/whatsBehind/pyinheritance',  # Replace with your GitHub repo URL
    packages=find_packages(where='src'),  # Look for packages in the 'src' directory
    package_dir={'': 'src'},  # Tell setuptools that packages are under 'src'
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Choose an appropriate license
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.10',  # Specify the Python version compatibility
    install_requires=[
        'pytest',
        'graphviz'
    ],
    extras_require={
        'testing': ['pytest'],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
