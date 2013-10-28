import os
import sys

from setuptools import setup, find_packages
from distutils.command.build_py import build_py


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

version = '0.1'

requires = [
]

develop_extras = [
    # Trick CI to build HTML packages, so they're NOT built on the IdPs
    'Jinja2==2.7.1',
]

testing_extras = [
    'nose==1.2.1',
    'coverage==3.6',
]

if sys.version_info[0] < 3:
    # Babel does not work with Python 3
    develop_extras.append('Babel==1.3')


class my_build_py(build_py):
    """
    Custom build step to generate the translated HTML pages.
    """

    def run(self):
        build_html = False
        src_dir = self.get_package_dir('eduid_IdP_html')
        stat_path = os.path.join(src_dir, 'templates')
        try:
            os.stat(stat_path)
            build_html = True
        except OSError:
            sys.stderr.write("NOT building HTML files - could not stat {!r}\n".format(stat_path))
            pass
        if build_html:
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
        'testing': testing_extras,
        'develop': develop_extras,
    },
    cmdclass={'build_py': my_build_py},
)
