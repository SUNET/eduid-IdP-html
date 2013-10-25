This is the HTML files used for eduid-IdP in the eduid.se installation.

In order to keep the security sensitive code base as small as possible,
eduid-IdP does not use a templating engine. This brings extra challenges
to the internationalization (i18n) work.

This package _does_ use a templating engine (Jinja2) with i18n support.
The HTML files that will be served by eduid-IdP are generated in the
setup.py build stage from the Jinja2 templates ineduid_IdP_html/templates/.

While this is not a super-elegant solution, it allows us to translate
the eduid-IdP HTML pages in the same way we translate everything else,
without requiring a full templating engine in eduid-IdP.

Fredrik Thulin, 2013-10-25
