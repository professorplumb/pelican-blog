#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Eric Plumb'
SITENAME = u'This Is The Title Of This Page'
THEME = 'theme/built-texts'

TIMEZONE = 'US/Pacific'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = []

# Social widget
SOCIAL = (('Twitter', 'http://twitter.com/xanthelasmoidea'),
          ('GitHub', 'https://github.com/professorplumb'), )

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PLUGIN_PATH = "../pelican-plugins"
PLUGINS = ['html_entity', ]