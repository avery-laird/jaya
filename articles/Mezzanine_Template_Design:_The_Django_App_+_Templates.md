## The Django App

<span class="dropcap">T</span>he main principle behind theme design in mezzanine involves a django app, placed in your project, that handles all of the custom styling and templates you want in the project. This way, one can share themes, install someone else's theme, or migrate/update their project quite easily. It keeps things modular, the benefits of which are explained (ad nauseam, believe me) [here][1]. By default, a django app consists of models and views. There are also files for tests, migrations (later explained with databases) and handling the admin side of things. Let's start by creating our `theme` app. This is pretty easy to do:

    $ python django-admin.py startapp theme

You'll see a new directory, called `theme`, show up in your project. The file tree should look something like this:

    theme/
        __init__.py
        admin.py
        migrations/
            __init__.py
        models.py
        tests.py
        views.py

I'll do a quick overview of each thing:

1. `__init__.py` should be in the directory every time it's something you want python to find -- that is largely what it does, in fact the file itself is often empty. It has other important uses as well, but that's all I'll say about it for now.
2. `admin.py` is used in the context of the admin site. This is where you register your app and tell django how to handle/display it.
3. `migrations/` directory: contains the migrations for that app. Migrations are used with the database and south -- we'll get more in depth about this later.
4. `models.py` is where the magic happens, or at least a large majority of it. This is where we represent models using classes (which subclass django's own special spice) and fields using class variables. We define how and when data should be stored. If you're new to this, it will probably make more sense once you see models in use.
5. `tests.py` is a file every good programmer *should* use with all their apps. I guess I'm not a good programmer...
6. `views.py` is not something we'll be using in the context of creating our theme. 

Okay, now that we've got all that explained, we can get started actually creating a theme! I'm going to start with a free theme called [clean blog][2] (actually what I used when first creating this site) and convert it to a new-and-improved mezzanine powered blog. 

### Install the app

We'll be making changes to our app and the data it deals with over the course of the series, but we can install it now. First, you have to add it to your `INSTALLED_APPS` setting in `settings.py`:

    :::python
    # settings.py

    INSTALLED_APPS = (
    	"theme",
        "django.contrib.admin",
    	"django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.redirects",
    	"django.contrib.sessions",
    	"django.contrib.sites",
    	"django.contrib.sitemaps",
    	"django.contrib.staticfiles",
    	"mezzanine.boot",
    	"mezzanine.conf",
    	"mezzanine.core",
    	"mezzanine.generic",
    	"mezzanine.blog",
    	"mezzanine.forms",
    	"mezzanine.pages",
    	"mezzanine.galleries",
    	"mezzanine.twitter",
    	#"mezzanine.accounts",
    	#"mezzanine.mobile",
    )

Make sure you add it first, so it's templates override mezzanine's, and remember the comma after the quotes. Our app doesn't have any models yet, so there's no need to migrate or sync the database (although it may be a good idea, just to check and see if you missed anything)

## Collect Templates

Right now, the website we see at localhost has it's templates being served from mezzanine, in `lib/python2.x/site-packages/mezzanine/core/templates/`. We don't want to get rid of them, or change them directly, but we don't have to -- they can be overridden. We will set up our app so that its templates are loaded before mezzanine's. This makes everything less messy, mostly because we can update mezzanine without causing a lot of issues, and we can move our `theme` app around and use it somewhere else.
    If we where to collect all of the templates, that would be too much; there are some that we don't want. With that in mind, let's collect each template as we need to, starting with `base.html`:

    $ python manage.py collecttemplates -t base.html

The template has been copied into a newly created directory, `templates/`, in your project directory. We want it in our app though, so let's copy the whole `templates/` directory over:

    $ mv templates theme

Now, our app's `base.html` will take precendence over the default. You can test this out by making changes to `theme/templates/base.html` and seeing them reflect in the site.

## Homepage Elements

> If you'd like to follow along with the tutorial using the clean blog template, you should download it into your project directory. Depending on 
> your preferences, you can either directly download it from the site or clone it using git. My preference is to just go:
> 
>     $ git clone git@github.com:IronSummitMedia/startbootstrap-clean-blog.git
> 
> in the project directory.


Our ``index.html`` is going to be the template that we draw the elements from our site from, so let's take a look at what we need to migrate over to our new shiny mezzanine app. Going from top to bottom, I see a:

* navbar
* splash image 
* header/subheader
* List of recent blog posts, with:
    * header
    * description/subheader
    * Metadata (author, day posted)
    * horizontal rule
    * pagination
* footer
    * social media buttons
        * twitter
        * facebook
        * github
    * info text (copyright, name)

Let's start by making some changes to `base.html`.

### Prepping base.html    
   
1.    Right now, `base.html` is the default mezzanine template, but we want our own fancy one, so let's get rid of what we don't want by deleting everything inside the `<body>` tag until the `{% include "includes/footer_scripts.html" %}` tag. 
2.    Transfer everything inside the header of the blog's `index.html` to the header of `base.html` -- all of the javascript and css. 
4.    Move everything inside the `<body>` tags of the clean blog's `index.html` to the `<body>` tags of `base.html`

You're almost done this step: the last thing you have to do is update the locations of the static content for the blog. When we moved the links in the header over, the respective paths changed, so we now have to move the content into the app and update the references in `base.html` to match.

1.    Create a `static` directory in `theme`:  

        $ mkdir theme/static

2.    Transfer over the static files:  

        $ mv startbootstrap-clean-blog/css/ theme/static/ 
        $ mv startbootstrap-clean-blog/js/ theme/static/
        $ mv startbootstrap-clean-blog/img/ theme/static/

3.    Update references. For example:    

        :::html
        <!-- index.html -->

        <link href="css/clean-blog.min.css" rel="stylesheet">

      Becomes:  
  
        :::html+django
        <!-- base.html -->
  
        <link href="{% static "css/clean-blog.min.css" %}" rel="stylesheet">

> The body of `index.html` also includes some images and other links: **don't forget to update those references too!** That would look like this:
>    :::html+django
>    <header class="intro-header" style="background-image: url("{% static "img/home-bg.jpg" %}")">
> 

Neat! Quick side-note: If you're using a halfway decent editor like vim or emacs and/or some sort of IDE, I would recommend using a search and replace tool to update your references.  

At this point, if you run the server, you'll see (should see) the new template rendered. Take this time to make sure everything's loading properly, and that all of the css and javascript is being found. If an element/style is not loading correctly, take a look at the server's output in the shell or your browser's dev tools (if it has any) to find the problem. I usually miss one or two files first time 'round, so this is a good spot to check your work.

### Navbar

If you take a look at the `index.html` you'll notice the navbar is layed out like a standard boostrap navbar:

    :::html
    <nav class="navbar navbar-default navbar-custom navbar-fixed-top">
      <div class="container-fluid">
        <!-- Brand and toggle get grouped for better mobile display -->
         <div class="navbar-header page-scroll">
           <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="index.html">Start Bootstrap</a>
            </div>

            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav navbar-right">
                    <li>
                        <a href="index.html">Home</a>
                    </li>
                    <li>
                        <a href="about.html">About</a>
                    </li>
                    <li>
                        <a href="post.html">Sample Post</a>
                    </li>
                    <li>
                        <a href="contact.html">Contact</a>
                    </li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->
    </nav>

The navbar is something we want on every page of our site (usually), as well has the header and footer -- that means we should probably put them in our `base.html`. You can go ahead delete everything in the `base.html` right now, from the `body` tag to `{% include "includes/footer_scripts.html" %}`. 

  [1]: https://docs.djangoproject.com/en/1.7/intro/reusable-apps/
  [2]: http://startbootstrap.com/template-overviews/clean-blog/