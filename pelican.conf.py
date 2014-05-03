# -*- coding: utf-8 -*-
from __future__ import unicode_literals

AUTHOR = 'edk'
SITENAME = "edk's notes"
SITEURL = 'http://notes.glin.es'
TIMEZONE = "Europe/London"

GITHUB_URL = 'http://github.com/edk0/'
PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = True
LOCALE = map(str, ["en_GB.utf8", "en_GB", "en_US.utf8", "en_US", "C.UTF-8", "C"])
DEFAULT_PAGINATION = 25
DEFAULT_DATE_FORMAT = "%d %B %Y"

THEME = "theme/"

FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'

LINKS = [('contact', 'mailto:edk141@gmail.com')]

JINJA_EXTENSIONS = ['jinja2.ext.do']

MD_EXTENSIONS = ['codehilite(guess_lang=False)', 'extra']

ARTICLE_URL = "a/{slug}"
ARTICLE_SAVE_AS = "a/{slug}.html"
ARTICLE_LANG_URL = "a/{slug}-{lang}"
ARTICLE_LANG_SAVE_AS = "a/{slug}-{lang}.html"
PAGE_URL = "p/{slug}"
PAGE_SAVE_AS = "p/{slug}.html"
PAGE_LANG_URL = "p/{slug}-{lang}"
PAGE_LANG_SAVE_AS = "p/{slug}-{lang}.html"
AUTHOR_URL = "u/{slug}"
AUTHOR_SAVE_AS = "u/{slug}.html"
CATEGORY_URL = "c/{slug}"
CATEGORY_SAVE_AS = "c/{slug}.html"
TAG_URL = "t/{slug}"
TAG_SAVE_AS = "t/{slug}.html"
