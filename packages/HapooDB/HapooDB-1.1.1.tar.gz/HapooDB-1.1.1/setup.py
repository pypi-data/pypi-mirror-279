from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.1.1'
DESCRIPTION = 'Hapoo DB'


# Setting up
setup(
    name="HapooDB",
    version=VERSION,
    author="HapooIsLuv (Pro gamer!1!)",
    author_email="<Hapoo@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'DB', 'Noob'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)