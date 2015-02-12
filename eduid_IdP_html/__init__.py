"""
Generate static HTML files for eduid-IdP in all supported languages.
"""

import os
import sys
import pkg_resources
import ConfigParser

from jinja2 import Environment, PackageLoader
from babel.support import Translations

__version__ = '0.1'
__copyright__ = 'SUNET'
__organization__ = 'SUNET'
__license__ = 'BSD'
__authors__ = ['Fredrik Thulin']

__all__ = [
]

_CONFIG_DEFAULTS = {'gettext_domain': 'eduid_IdP_html',
                    }


def translate_templates(env, loader, settings, verbose=False, debug=False):
    """
    Translate all templates available through `loader'.

    Returns a big dict with all the translated templates, in all languages :

    {'login.jinja2': {'en': string, 'sv': string, ...},
     'error.jinja2': ...
    }

    :param env: jinja2.Environment()
    :param loader: jinja2.BaseLoader()
    :param settings: dict with settings and variables available to the Jinja2 templates
    :param verbose: boolean, output to stdout or not
    :param debug: boolean, output debug information to stderr or not
    :return: dict with translated templates
    """
    languages = {}
    res = {}

    locale_dir = pkg_resources.resource_filename(__name__, 'locale')

    for lang in pkg_resources.resource_listdir(__name__, 'locale'):
        lang_dir = os.path.join(locale_dir, lang)
        if not os.path.isdir(lang_dir):
            if debug:
                sys.stderr.write("Not a directory: {!r}\n".format(lang_dir))
            continue
        if verbose:
            languages[lang] = 1

        translations = Translations.load(locale_dir, [lang], settings['gettext_domain'])
        env.install_gettext_translations(translations)

        for template_file in loader.list_templates():
            if template_file.endswith('.swp'):
                continue
            template = env.get_template(template_file)
            translated = template.render(settings=settings)

            if not template_file in res:
                res[template_file] = {}
            res[template_file][lang] = translated.encode('utf-8')

            if debug:
                sys.stderr.write("Lang={!s} :\n{!s}\n\n".format(lang, translated.encode('utf-8')))

    if verbose:
        print("\nLanguages : {!r}\nGenerated templates : {!r}\n".format(
            sorted(languages.keys()), sorted(res.keys())))

    return res


def load_settings(resource_name='settings.ini'):
    """
    Load settings from INI-file (package resource).

    All options from all sections are collapsed to one flat namespace.

    :param resource_name: string, name of package resource to load.
    :return: dict with settings
    """
    config = ConfigParser.ConfigParser(_CONFIG_DEFAULTS)
    config_fp = pkg_resources.resource_stream(__name__, resource_name)
    config.readfp(config_fp, resource_name)
    settings = {}
    for section in config.sections():
        for option in config.options(section):
            settings[option] = config.get(section, option)
    return settings


def save_to_files(translated, output_dir, verbose):
    """
    Save translated templates to files (with a .html extension).

    :param translated: dict (result of translate_templates() probably)
    :param output_dir: string, output path
    :param verbose: boolean, print status output to stdout or not
    """
    for template in translated.keys():
        template_html_fn = template
        if template_html_fn.endswith('.jinja2'):
            # remove '.jinja2' extension
            template_html_fn = template_html_fn[:len(template_html_fn) - len('.jinja2')]
        template_html_fn += '.html'
        for lang in translated[template].keys():
            lang_dir = os.path.join(output_dir, lang)
            try:
                os.stat(lang_dir)
            except OSError:
                os.mkdir(lang_dir)
            output_fn = os.path.join(lang_dir, template_html_fn)
            fp = open(output_fn, 'w')
            fp.write(translated[template][lang])
            fp.write("\n")  # eof newline disappears in Jinja2 rendering
            if verbose:
                print("Wrote {!r}".format(output_fn))
    if verbose:
        print("\n")


def main(verbose=False, output_dir=None):
    """
    Code executed when this module is started as a script.

    :param verbose: boolean, print status output to stdout/stderr or not
    :param output_dir: string, output path
    :return: boolean
    """
    settings = load_settings()
    if not settings:
        return False

    loader = PackageLoader(__name__)
    env = Environment(loader=loader,
                      extensions=['jinja2.ext.i18n',
                                  'jinja2.ext.autoescape',
                                  'jinja2.ext.with_',
                                  ],
                      )

    translated = translate_templates(env, loader, settings, verbose)

    if output_dir:
        save_to_files(translated, output_dir, verbose)

    return True

if __name__ == '__main__':
    if not main(verbose=True, output_dir="/tmp/foo"):
        sys.exit(1)
    sys.exit(0)
