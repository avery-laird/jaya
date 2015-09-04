<span class="dropcap">A</span>s a newbie in the world of Mezzanine, I found many resources provided by the project to be tremendously useful. However, I remember a few obstacles I ran across while trying to get started that sometimes hindered my progress (often severely). I think this stems from the fact that I have no solid footing in any one aspect of web development. I am fairly confident in Python, but only with a solid eye on the documentation -- like many, I am completely self taught. This resulted in a largely non-linear education, causing numerous gaps in my learning that I had to fill as I went. This could be frustrating while also trying to simply get everything off the ground, and have at least *something* that **just worked.**  
    
    As a result, I decided to create a series in which I describe more of the finer details that often get missed -- for people like me, with certain gaps in their learning that often make what should be a simple process much more difficult than it needs to be. Here's what the order of the series will look like:  

1. Installing mezzanine and creating the proper development environment
2. Setting up the development and production databases (and the difference between the two)
3. Models and the layout of your average django app
4. Useful Mezzanine utilities
5. Creating your own theme: pages
6. More to come...  

Let's get started!

------

## Installing Mezzanine  


Python is great. Here's one problem, however: when packages are installed, they're installed **globally** (as always, there are exceptions) which means that one package is used throughout the system. This is great for a lot of things, but it can cause some issues with development. Let's say you start a project, and install a certain amount of dependencies -- you build your entire project around those dependencies, and most importantly, that *version* of dependencies. Now, you start another project, and decide you want the shiny new feature of some previously installed dependency. You update the package, and suddenly your other project is completely broken. Crap! What do I do? A virtual environment is the answer.
### virtualenv

A virtual environment is exactly what it sounds like -- a sandbox, safe haven from the perils the open sea of globally installed packages entails. Well... maybe I got a bit "overboard". No, I will not apologize!
But anyway, it comes in handy sometimes.

### Putting it all together

Okay, here we go. Let's get a mezzanine project going. I assume you are using a linux system (or some other unix variant) and have pip installed. 

First, install virtualenv:

    $ sudo apt-get install virtualenv

Next, create a virtual environment:

    $ virtualenv project_name

It will setup some things for you, like your own special pip instance for installing packages. Next:

    $ cd project_name  
    $ source bin/activate

The `source bin/activate` command is **super important.** This is what starts the insulated environment, and installs packages locally (not globally) so your project's libraries are safe. Every time you start working on your app, you should run this command -- believe me, it's the kind of mistake you only want to make once. You can check by looking at the left of the command line: if your virtualenv name is there in parentheses, you're good. Now we're ready to start the project.

Install mezzanine:

    $ pip install south mezzanine
    $ mezzanine-project project_name
    $ mv project_name/* .

That last command moves the mezzanine project into the main directory, since a mezzanine project needs a name and cannot be generated with a `.` (eg, in that directory) -- and you don't want to end up with a bunch of nested directories to get through. Now the previous directory is empty, so you can remove it.

    $ rm -r project_name

We can now create the server by:

    $ python manage.py createdb

If you just want the default settings and/or no demo data, you can run

    $ python manage.py createdb --noinput --nodata

instead.

Now that the database is created, you can start the server:

    $ python manage.py runserver

and go check it out at localhost, port 8000: `127.0.0.1:8000`

