import io
import os
import re
import sys

from setuptools import setup

needs_pytest = 'pytest' in set(sys.argv)


def get_version():
    regex = r"__version__\s=\s\'(?P<version>[\d\.ab]+?)\'"

    path = ('aiohttp_request.py',)

    return re.search(regex, read(*path)).group('version')


def read(*parts):
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)

    with io.open(filename, encoding='utf-8', mode='rt') as fp:
        return fp.read()


setup(
    name='aiohttp_request',
    version=get_version(),
    author='Victor Kovtun',
    author_email='hellysmile@gmail.com',
    url='https://github.com/hellysmile/aiohttp_request',
    description='Global request for aiohttp server',
    long_description=read('README.rst'),
    py_modules=['aiohttp_request'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'aiohttp>=3.3.0',
        'werkzeug>=0.6.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['aiohttp', 'request'],
)
