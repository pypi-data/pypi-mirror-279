from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Youtube Autónomo stock utils are here.'
LONG_DESCRIPTION = 'These are the stock utils we need in the Youtube Autónomo project to work in a better way.'

setup(
        name = "yta-stock-downloader", 
        version = VERSION,
        author = "Daniel Alcalá",
        author_email = "<danielalcalavalera@gmail.com>",
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        packages = find_packages(),
        install_requires = [
            'yta-general-utils'
        ],
        
        keywords = [
            'youtube autonomo stock downloader'
        ],
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)