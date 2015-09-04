This is the second part of a Template Design Series. If you haven't installed mezzanine yet, and/or don't have a working project, you might want to start with [Part 1.][1]

## Mezzanine: The Database

### But I postgres...

So right now all of your data is stored in a file, called `dev.db`, in your home directory. This is great for development, cause it's right there, you can destroy it and start over if you have to quite easily, and it doesn't involve much setup. 
          
But it's not a great solution for production. For that, I use postgres. If you're interested in setting it up, follow along, if not, you can skip ahead -- **do not do this section if this is your first time reading the article. This database is best used in production, *not development.* **  

First, install postgres: 

    $ sudo apt-get install postgresql postgresql-client

Next, install psycopg2:
  
    $ pip install psycopg2

And change some settings in `local_settings.py`:

    :::python
    # local_settings.py

    DATABASES = {
        "default": {
            # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            # DB name or path to database file if using sqlite3.
            "NAME": "project_db",
            # Not used with sqlite3.
            "USER": "project_user",
            # Not used with sqlite3.
            "PASSWORD": "project_pass",
            # Set to empty string for localhost. Not used with sqlite3.
            "HOST": "localhost",
            # Set to empty string for default. Not used with sqlite3.
            "PORT": "",
        }
    }

You can leave the settings in `settings.py` alone for now.

Now, we have to create the database. First:

    $ sudo -u postgres psql postgres

This starts a postgres prompt, as user postgres (i.e the "`-u`" switch). It's basically saying, "execute this command, as sudo of the user postgres, to run the command `psql` with argument `postgres`." You should get a prompt that looks like this:

    postgres=#

Now let's create a database that fits the credentials we used in `local_settings.py`. First (note when the semi-colon is used, and when it isn't):

    postgres=# create database project_db;
    postgres=# create user project_user;
    postgres=# \password project_user

We're all done with postgres for now, so we can do:

    postgres=# \q

to exit. Now since we're using a different database, we can get rid of the sqlite one:

    $ rm dev.db

And re-run the `createdb` command to regenerate the database. 

    $ python manage.py createdb --noinput --nodata

All done.

-------

  [1]: http://averylaird.com/blog/mezzanine-template-design/