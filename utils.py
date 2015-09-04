import json
import markdown
import codecs
import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from os import path
from fabric.colors import green, yellow, red

from django.core.exceptions import ObjectDoesNotExist
from models import BlogPostCount

try:
    article_root = settings.JAYA_CONFIG['ARTICLE_ROOT']
except KeyError:
    raise KeyError("ARTICLE_ROOT must be set in jaya.settings.JAYA_CONFIG")

try:
    fixture_dir = settings.JAYA_CONFIG['FIXTURE_DIR']
except KeyError:
    raise KeyError("The path to your fixtures directory must be set in jaya.settings.JAYA_CONFIG")


# Create tree from blogpost JSON
# TODO: using titles to compare is fragile, should use pk instead
def fetch_articles(article_root=article_root, fixture_file=settings.FIXTURE_PATH):
    # Check remote database for articles
    with open(fixture_file, 'r') as f:
        data = json.load(f)
        print green("Fetched %s posts" % len(data)) + " from %s" % fixture_file
        i = 0
        s = 0
        for post in data:
            title = post['fields']['title']
            pk = post['pk']
            if post_exists(pk) and filesystem_safe(title) in article_titles():
                print "\"%s\" already exists" % title
                s += 1
            else:
                print yellow("Creating article \"%s\":" % title)
                content = post['fields']['content']
                if settings.CHECK_EXTENSIONS:
                    extension = raw_input("\nThe extension for this post is not specified,"
                                          " please enter it here (with no period): ")
                else:
                    extension = ""

                filesystem_title = filesystem_safe(title)
                with codecs.open(article_root + "/{}.{}".format(filesystem_title, extension), 'w+', encoding='utf8') as l:
                    l.write(content)

                # Construct article-specific fixture in fixtures directory
                with open(fixture_dir + "/{}.json".format(filesystem_title), 'w+') as fixture:
                    fixture.write(construct_fixture(pk=pk, title=title, content=content))
                print "Wrote fixture %s to %s" % (filesystem_title + "." + extension, fixture_dir)

                # Increment counter and assign pk
                p = BlogPostCount(counter=pk)
                p.save()
                print red("Created pk %i" % p.counter)

                i += 1
        print green("Successfully created %i posts and skipped %i" % (i, s))
        return True


def collect_articles():
    """
    Search articles directory for newly created articles, and generate a fixture
    for each one using a `null` primary key. When the fixtures are installed, a
    pk will be assigned by the remote database, and obtained locally on next sync
    :return:
    """
    # Create a json fixture for all articles which don't exist in the current
    # fixture file
    # TODO: Parse content before writing content to fixture
    for article in get_new_local_articles():
        with open(article_root + "/" + article, 'r') as f:
            #extension = article.split(".")[1]
            content = f.read()
            fixture = construct_fixture(pk=None, title=filesystem_to_pretty(article.split(".")[0]),
                                        content=content)
            with open(fixture_dir + "/{}.json".format(article.split(".")[0]), 'w+') as f:
                f.write(fixture)


def get_new_local_articles(fixture_file=settings.FIXTURE_PATH, article_root=article_root):
    """
    Compares a fixture file with titles in article root. Returns the titles of articles
    which are in the article root, but not the fixture file.
    :return:
    """
    articles = []
    with open(fixture_file, 'r') as f:
        posts = json.load(f, encoding='utf8')
        for title in article_titles(article_root):
            match = False
            for index, post in enumerate(posts):
                if names_are_equal(title, post['fields']['title']):
                    match = True
                if index == len(posts)-1 and not match:
                    articles.append(title)
    return articles


# Check if blogpost is already synced
def post_exists(pk):
    try:
        post = BlogPostCount.objects.get(counter=pk)
    except ObjectDoesNotExist:
        return False
    return True


def filesystem_safe(title):
    return title.replace(" ", "_")


def filesystem_to_pretty(title):
    return title.split("0.")[0]


def names_are_equal(filesystem_name, fixture_name):
    """
    takes a generated title, with underscores and extension, and tests
    equality with the name in the fixture
    :param filesystem_name:
    :param fixture_name:
    :return:
    """
    if filesystem_safe(filesystem_name) == fixture_name:
        return True
    return False


def article_titles(article_root=article_root):
    """
    return a list of titles currently in the articles directory
    :param article_root:
    :return:
    """
    return [f for f in os.listdir(article_root) if path.isfile(article_root + "/" + f)]


# Convert markdown to HTML
def markdown_to_html(obj, prefix=article_root):
    return markdown.markdownFromFile(prefix + "/" + obj, extensions=settings.MARKDOWN_EXTENSIONS)


# Convert LaTeX to HTML
def latex_to_html(obj, prefix=article_root):
    pass


def list_fields(fixture_file=settings.FIXTURE_PATH, list_to_shell=True):
    """
    Returns list of fields on BlogPost fixture. Call with `list_to_shell` set
    to false to silence output.
    :param fixture_file:
    :param list_to_shell:
    :return:
    """
    fields = []
    with open(fixture_file, 'r') as posts:
        posts = json.load(posts, encoding='utf8')
        i = 0
        for post in posts:
            for field in post['fields']:
                fields.append(field)
                i += 1
    if list_to_shell:
        print yellow("All available BlogPost fields:")
        print fields
        print yellow("%i fields total" % i)
    return fields


def construct_fixture(pk, title, content, extra_fields={}, model='blog.BlogPost', site_id=settings.SITE_ID):
    """
    takes a primary key and local article, and constructs a fixture to be
    loaded on the remote database. An arbitrary model fixture can be
    constructed using the `model` argument.
    :param pk:
    :param model:
    :param title:
    :param content:
    :param extra_fields:
    :return:
    """
    fixture = {'pk': pk, 'model': model, 'fields': {'site_id': site_id, 'title': title, 'content': content,}}
    for field, value in extra_fields.items():
        fixture['fields'][field] = value
    return json.dumps([fixture], indent=4)


def create_local_fixtures():
    """

    :return:
    """
    for article in get_new_local_articles():
        #construct_fixture(article)
        pass