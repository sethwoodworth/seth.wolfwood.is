#!/usr/bin/env python
from __future__ import unicode_literals

AUTHOR = "seth wolfwood"
SITENAME = "seth wolfwood is"
# SITEURL = "https://seth.wolfwood.is"
SITEURL = ""

PATH = "content"

TIMEZONE = "America/New_York"

DEFAULT_LANG = "en"

THEME = "./theme/"
DIRECT_TEMPLATES = ["writing"]
TEMPLATE_PAGES = {
    "index.html": "index.html",
}
CSS_FILE = "awsm.css"
FEED_ALL_RSS = "./rss.xml"

# Page URLs
ARTICLE_SAVE_AS = "writing/0{date:%Y}-{date:%m}-{date:%d}-{slug}/index.html"
ARTICLE_URL = "writing/0{date:%Y}-{date:%m}-{date:%d}-{slug}/"
AUTHOR_SAVE_AS = ""
AUTHOR_URL = ""
CATEGORIES_SAVE_AS = ""
CATEGORY_SAVE_AS = ""
CATEGORY_URL = ""
DRAFT_SAVE_AS = "still-writing/{slug}/index.html"
DRAFT_URL = "still-writing/{slug}/"
TAG_SAVE_AS = "writing/by-tag/{slug}/index.html"
TAG_URL = "writing/by-tag/{slug}/"
WRITING_SAVE_AS = "writing/index.html"

# Blogroll
LINKS = (
    ("my old blog", "https://blogs.harvard.edu/seth/"),
    ("GITenberg", "https://python.org/"),
    ("Free Ebook Foundation", "https://ebookfoundation.org/"),
    (
        "Free Programming Ebooks",
        "https://github.com/EbookFoundation/free-programming-books/",
    ),
)

# Social widget
SOCIAL = (
    ("I don't twitter anymore", "#"),
    ("my Github", "https://github.com/sethwoodworth"),
)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
