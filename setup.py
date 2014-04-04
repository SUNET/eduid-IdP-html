import os
import sys

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

version = '0.2.1'

requires = [
    'Jinja2==2.7.2',
]

testing_extras = [
    'nose==1.2.1',
    'coverage==3.6',
]

if sys.version_info[0] < 3:
    # Babel does not work with Python 3
    requires.append('Babel==1.3')


setup(
    name='eduid_IdP_html',
    version=version,
    description='eduID IdP HTML files',
    long_description=README + '\n\n' + CHANGES,
    # TODO: add classifiers
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='identity federation saml',
    author='SUNET',
    url='https://github.com/SUNET/eduid-IdP-html',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        'testing': testing_extras,
    },
)
