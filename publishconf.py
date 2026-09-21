# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://mchromiak.github.io'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True
DRAFT_SAVE_AS = ''
DRAFT_PAGE_SAVE_AS = ''

DISQUS_SITENAME = 'mchromiak'
GOOGLE_ANALYTICS_GA4 = 'G-58PH9XEMKB'
