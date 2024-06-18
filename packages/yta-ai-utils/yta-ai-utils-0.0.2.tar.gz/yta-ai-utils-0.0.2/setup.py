from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Youtube Autónomo AI utils are here.'
LONG_DESCRIPTION = 'These are the AI utils we need in the Youtube Autónomo project to work in a better way.'

setup(
        name = "yta-ai-utils", 
        version = VERSION,
        author = "Daniel Alcalá",
        author_email = "<danielalcalavalera@gmail.com>",
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        packages = find_packages(),
        install_requires = [
            'yta-general-utils',
            'google-generativeai',
            'faster_whisper',
            'whisper_timestamped',
        ],
        
        keywords = [
            'youtube autonomo ai utils'
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