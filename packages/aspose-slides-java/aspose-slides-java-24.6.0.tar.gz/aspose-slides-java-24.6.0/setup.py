# coding: utf-8

import sys
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description_file = fh.read()

NAME = "aspose-slides-java"
VERSION = "24.6.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["JPype1 >= 1.5.0"]

setup(
    name=NAME,
    version=VERSION,
    description="A powerful library for manipulating and converting PowerPoint (PPT, PPTX, ODT, OTP, POT, POTX, PPS, PPSX) files.",
    author="Aspose",
    url="https://products.aspose.com/slides/python-java/",
    keywords=["ppt", "pptx", "potx", "pot", "pps", "ppsx", "odt", "otp", "import", "export", "convert", "edit", "pdf", "xps", "swf", "svg", "html", "html5", "powerpoint", "presentation"],
    install_requires=REQUIRES,
    packages=['asposeslides'],
    include_package_data=True,
    project_urls={
        'Homepage': 'https://products.aspose.com/slides/python-java/',
        'API Reference': 'https://reference.aspose.com/slides/python-java/',
        'Blog': 'https://blog.aspose.com/category/slides/',
        'Docs': 'https://docs.aspose.com/slides/python-java/',
        'Free Support': 'https://forum.aspose.com/c/slides',
        'Release Notes': 'https://releases.aspose.com/slides/python-java/release-notes/2024/aspose-slides-for-python-via-java-24-6-release-notes/',
        'Search': 'https://search.aspose.com/',
        'Temporary License': 'https://purchase.aspose.com/temporary-license',
    },
    license='https://company.aspose.com/legal/eula',
    classifiers=[
        'License :: Other/Proprietary License',
        'License :: Free To Use But Restricted',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Office Suites',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
    ],
    platforms=[
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
    python_requires='>=3.7,<=3.12',
    long_description=long_description_file,
    long_description_content_type='text/markdown',
)

