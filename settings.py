JAYA_CONFIG = {
    "SSH_USER": "root",
    "REMOTE_DIR": "/home/root/mezzanine/project/jaya/articles",
    "REMOTE_FIXTURE_DIR": "/home/root/mezzanine/project/jaya/fixtures",
    "HOSTS": ["45.55.39.64"],
    "ARTICLE_ROOT": '/home/avery/Websites/averylaird.com/project/jaya/articles',
    "FIXTURE_FILE": 'fixtures.json', # path to fixture file. Must be in articles directory
    "FIXTURE_DIR": '/home/avery/Websites/averylaird.com/project/jaya/fixtures', # Directory in which to place articles
}

FIXTURE_PATH = JAYA_CONFIG['ARTICLE_ROOT'] + "/" + JAYA_CONFIG['FIXTURE_FILE']

# Utilize the codehilite extension in markdown. You can also add your own extensions here.
# Leave the list empty to disable all extensions.
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.codehilite',
]

# Prompt the user for extensions on sync
CHECK_EXTENSIONS = True

# Currently only supports one site at a time
SITE_ID = 1
