import os
import sys

from setuptools import setup, find_packages
from distutils.command.build_py import build_py


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

version = '0.1'

requires = [
    'Jinja2==2.7.1',
]

if sys.version_info[0] < 3:
    # Babel does not work with Python 3
    requires.append('Babel==1.3')

class my_build_py(build_py):

    def run(self):
        import eduid_IdP_html
        html_build_dir = os.path.join(self.build_lib, 'eduid_IdP_html', 'html')
        self.mkpath(html_build_dir, mode=0755)
        # Run eduid_IdP_html.main() to generate all translated HTMLs in the build process
        assert(eduid_IdP_html.main(
            verbose=True, output_dir=html_build_dir)
        )
        build_py.run(self)


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
    },
    cmdclass={'build_py': my_build_py},
)
