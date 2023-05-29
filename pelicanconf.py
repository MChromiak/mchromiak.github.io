#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Micha\u0142 Chromiak'        
SITENAME = u'Micha\u0142 Chromiak\'s blog'
SITESUBTITLE = 'Be a fool to become a Polymath.'

# WHEN empty the disqus not work; When set to mchromiak.gihub.io all rendered links refer thus
#   disable to test locally. To push use the publishconf.py that import pelicanconf.py and
#   adds the SITEURL as remote address:
#       pelican content -s publishconf.py
SITEURL = ''
SITELOGO = 'static_files/img/sitelogo40.png'
FAVICON = 'static_files/img/favicon.jpg'

DISQUS_SITENAME = 'mchromiak'
GOOGLE_ANALYTICS_UNIVERSAL = 'UA-108394162-1'
GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = 'auto'
#======================== DEV SETTINGS=======================
LOAD_CONTENT_CACHE = False
# !!!!!!!!!!!!!!!!! Del all every time change
DELETE_OUTPUT_DIRECTORY = True

# if DELETE_OUTPUT_DIRECTORY=True do not delete this directories
OUTPUT_RETENTION = [".git","LICENSE", "README.md", "robots.txt"]

#========================== FILES ==================================
PATH = 'content'

#articles are here so that the img files will be moved to output;
#the imgages not present in md file will be moved to "output/articles.../img/"
STATIC_PATHS = ['static_files', 'articles']
ARTICLE_PATHS = ['articles']
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

IGNORE_FILES = ['.#*', '*draft*']
#=============================== URL =====================================
# Define paths in 'output' dir where will be HTML files generated.

ARTICLE_URL = 'articles/{date:%Y}/{date:%b}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'articles/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.html'

DRAFT_URL = 'drafts/{slug}.html'
DRAFT_SAVE_AS = 'drafts/{slug}.html'

YEAR_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/{date:%b}/index.html'
DAY_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/{date:%b}/{date:%d}/index.html'
#============================================================

TIMEZONE = 'Europe/Warsaw'

DEFAULT_LANG = u'en'
DATE_FORMATS = { # to use US month names in article dates and archives
    'en': ('en_US.UTF-8','%a, %d %b %Y')
}

# Prefix the feeds with current URL (not localhost)
FEED_DOMAIN = SITEURL
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

AVATAR = 'static_files/img/me.png'
ABOUT_ME = ' PhD in Computer Science by Polish Academy of Sciences (PAS). Focus research on understanding chaos of data. Deeply understanding the phenomena makes it easy, but first you need to learn. Holds two MScs, in Mathematics and in Computer Science.'

# Blogroll
LINKS = (   ('ICLR Conf', 'http://www.iclr.cc'),
            ('ICML Conf', 'http://icml.cc'),
            ('NeurIPS Conf', 'https://nips.cc/'),
            ('AI Frontiers', 'http://aifrontiers.com/'),
            ('ML Glossary', 'https://developers.google.com/machine-learning/glossary/'),
            ('Deep Dream Generator', 'https://deepdreamgenerator.com/'),
            ('DeepArt Generator', 'https://deepart.io/'),
            ('Stanford ML Group Andrew Ng', 'https://stanfordmlgroup.github.io/'),
            ('AI•ON open ML collaboration', 'https://ai-on.org/'),
            ('My old blog on Java an SE', 'http://java-hive.blogspot.com/'),
            ('PhD', 'http://karpathy.github.io/2016/09/07/phd/'),
            ('SemEval2017', 'http://alt.qcri.org/semeval2017/'),
            ('Free CS courses', 'https://medium.freecodecamp.org/450-free-online-programming-computer-science-courses-you-can-start-in-september-59712e77635c'),
        )

# Social widget
SOCIAL = (('LinkedIn', 'https://www.linkedin.com/in/michal-chromiak'),
         ('GitHub', 'https://github.com/MichalChromiak'),
         ('Twitter', 'https://twitter.com/drChromiak'),
         ('ResearchGate', 'https://www.researchgate.net/profile/Michal_Chromiak'),
         ('Google Scholar', 'https://scholar.google.pl/citations?user=UeOad3YAAAAJ&hl=en'),
         ('RSS', 'localhost:8000/feeds/all.rss'),)

DEFAULT_PAGINATION = 10

DISPLAY_ARTICLE_INFO_ON_INDEX = True

RELATED_POSTS_MAX = 10 # plugin related_posts

DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True
TAG_CLOUD_BADGE = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = 3
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_ARCHIVE_ON_SIDEBAR = True

#SIDEBAR_ON_LEFT = True

CC_LICENSE = 'CC-BY-SA'

#=============================== THEME =====================================

THEME = 'custom/pelican-bootstrap3'
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
BOOTSTRAP_THEME='cerulean'

BANNER = 'static_files/img/prv/banner.jpg' # image from googlenet generate as Iterative_Places205-GoogLeNet_2
#BANNER_SUBTITLE = 'Be a fool to become a Polymath.'
BANNER_SUBTITLE = 'Cast Math spells on data.'

DISPLAY_CATEGORIES_ON_MENU = False

SHOW_ARTICLE_AUTHOR = True
SHOW_ARTICLE_CATEGORY = True
SHOW_DATE_MODIFIED = True

PYGMENTS_STYLE = 'colorful'
DISPLAY_BREADCRUMBS = True
DISPLAY_CATEGORY_IN_BREADCRUMBS = True

CUSTOM_CSS = 'static_files/css/custom.css'
CUSTOM_JS = 'static_files/js/custom.js'

# JS scripts run on article sides. see article.html template
ARTICLE_JS = 'static_files/js/article.js'

EXTRA_PATH_METADATA = {
    'css/custom.css': {'path': 'css/custom.css'},
    'js/custom.js': {'path': 'js/custom.js'},
    'js/article.js': {'path': 'js/article.js'}
}

DISQUS_DISPLAY_COUNTS = True
DISQUS_NO_ID = True

# ============== Open Graph =====================================================
USE_OPEN_GRAPH = True
OPEN_GRAPH_IMAGE = 'static_files/img/Avatar.png'
# twiitts of each post will have image and text included
TWITTER_CARDS = True
TWITTER_USERNAME = 'drChromiak'

ADDTHIS_PROFILE = 'ra-59ea3c17b283c631'

#=============================== PLUGINS =====================================

#Reqired by theme pelican-bootstrap3
PLUGIN_PATHS = ['../pelican/pelican-plugins']
PLUGINS = ['i18n_subsites','related_posts','tag_cloud','simple_footnotes','render_math','sitemap']

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {'permalink': '🔗'},
        'markdown.extensions.attr_list': {}, # to enable eg. alignment for images or image id for anchors
    },
    'output_format': 'html5',
}

SITEMAP = {
    'format': 'xml',
    'exclude': ['tag/', 'category/'],
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# TODO: Travis integration
