import os
import subprocess
from setuptools import setup, find_packages
import re

def get_version():
    # Check if version is passed as an environment variable
    version = os.getenv('PACKAGE_VERSION')

    if version.startswith('refs/tags/'):
        version = version[10:]

    if version.startswith('v'):
        version = version[1:]

    if version and re.match(r'^\d+\.\d+\.\d+$', version):
        return version

    # Fallback to default version if not provided or invalid
    return "0.0.0"


setup(
    name='printannotate',
    version=get_version(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'printannotate = printannotate.__main__:entrypoint',
        ],
    },
    install_requires=[
        # Add any dependencies here
    ],
    author='Andrzej Wasowski',
    author_email='me@wasowski.dev',
    description='A package to annotate print statements in provided script.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/saikotek/printannotate',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
