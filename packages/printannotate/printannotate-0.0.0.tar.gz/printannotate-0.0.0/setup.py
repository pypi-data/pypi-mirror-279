import subprocess
from setuptools import setup, find_packages
import re

def get_version():
    try:
        # Extract the version from the git tag
        version = subprocess.check_output(
            ["git", "describe", "--tags", "abbrev=0"]).strip().decode("utf-8")

        # Strip the 'v' prefix from the git tag
        if version.startswith('v'):
            version = version[1:]

        if re.match(r'^\d+\.\d+\.\d+$', version):
            return version
        else:
            print(f"Tag version '{version}' does not match the format 'x.y.z'.")
        return version
    except Exception as e:
        print(f"Error getting version from git tag: {e}")


setup(
    name='printannotate',
    version=get_version(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'printannotate = printannotate.__main__:main',
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
