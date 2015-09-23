# README #

### GETTING STARTED ###

1. Set your environment variables (see below).
2. Install the requirements below.
3. Run the migrations.

        python manage.py migrate

4. Create a superuser.

        python manage.py createsuperuser

5. Run the server.

        python manage.py runserver $MAGI_PORT

#### ENVIRONMENT VARIABLES ####

Many of the settings of MAGI are configurable with the following environment
variables:

| Name                        | Default value   |
| --------------------------- | --------------- |
| `MAGI_SITE_URL`             | `''`            |
| `MAGI_GOOGLE_CLIENT_ID`     | `''`            |
| `MAGI_GOOGLE_CLIENT_SECRET` | `''`            |
| `MAGI_PYTHON_ENV`           | `'development'` |
| `MAGI_PORT`                 | `'8080'`        |
| `MAGI_POSTGRES_USER`        | `'mdml'`        |
| `MAGI_POSTGRES_PASSWORD`    | `''`            |
| `MAGI_POSTGRES_PORT`        | `'5432'`        |
| `MAGI_POSTGRES_HOST`        | `''`            |
| `MAGI_POSTGRES_DB`          | `'magipy'`      |

### REQUIREMENTS ###

#### DEBIAN ####
1. **Postgres**. This can be installed on using the command:

        >>> sudo apt-get install postgresql postgresql-client

  Then set up your user and database:

        >>> sudo -u postgres createuser $MAGI_POSTGRES_USER
        >>> createdb $MAGI_POSTGRES_DB

  Note that if you don't set up a password for your $USER, you should exclude
the 'HOST' line in the `DATABASES` settings in `magipy/settings.py`.

2. **Python**. First, install dependencies:

        >>> sudo apt-get install libpq-dev python-dev

  We can manage Python requirements using virtualenv and pip. Execute the
following commands on the command-line:

        >>> virtualenv venv
        >>> source venv/bin/activate
        >>> pip install -r requirements.txt
