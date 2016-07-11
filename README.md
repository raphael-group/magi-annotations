# MAGI Annotations #

[MAGI Annotations](http://annotations.cs.brown.edu) is a Django web server that allows users to view and edit annotations of mutation and protein-protein interactions. It is complementary to [MAGI](http://magi.brown.edu). MAGI Annotations was built and is maintained by the Raphael group at Brown University.

### Setup ###

1. **Set your environment variables (see below)**. We suggest making a file `ENVIRONMENT` and then loading the variables into your shell with `source ENVIRONMENT`.
2. **Install dependencies (see below)**.
3. **Setup your Postgres user and database.**   Then set up your Postgres user and database. For example (depending on your set up, these commands may differ slightly):

        createuser $POSTGRES_DJANGO_USER
        createdb $POSTGRES_DJANGO_DBNAME

3. **Run the migrations**. This will setup the tables in your Postgres database.

        python manage.py migrate

4. **Create a superuser**.

        python manage.py createsuperuser

5. **Initialize the database**. We provide a tarball of the data used to initialize [MAGI Annotations](annotations.cs.brown.edu) on our group website. We provide the `setup.sh` script for convenience which includes the contains the commands for initializing the database.

#### Dependencies ####

Latest tested version in parentheses.

1. **Python** (2.7.11). We suggest managing Python requirements using virtualenv and pip. Execute the
following commands on the command-line:

        virtualenv venv
        source venv/bin/activate
        pip install -r requirements.txt
2. **Postgres** (9.5.3).

3. **Bower**. Bower is required for managing Javascript dependencies. First, you will need to install [Node.js](https://nodejs.org/en/) and [NPM](https://www.npmjs.com/). Then, install [Bower](http://bower.io/), and use it to install the Javascript dependencies:

        npm install -g bower
        bower install

See our wiki page  [Getting set up with MAGI Annotations](https://github.com/raphael-group/magi-annotations/wiki/Getting-set-up-with-MAGI-Annotations) for additional instructions.

#### Environment variables ####

Many of the settings of MAGI Annotations are configurable with the following environment variables. Note that some of these environment variables overlap with MAGI (see [MAGI: Environment](https://github.com/raphael-group/magi#environment)), so be sure to set these appropriately.

| **Name**                      | **Default**               | **Description**                                               |
| ----------------------------- | ------------------------- | ------------------------------------------------------------- |
| `MAGIPY_PORT`                 | `'8080'`                  | Port from which you are serving MAGI                          |
| `MAGIPY_ENV`                  | `'development'`           | "production" for publicly available on the web, or "development" for local/testing |
| `MAGIPY_SITE_URL`             | `''`                      | URL for MAGI Annotations server (required in production only) |
| `MAGI_SECRET_KEY`             | `'MAGI_FOR_PRESIDENT'`    | Secret key (required in production only)                      |
| `POSTGRES_DJANGO_DBNAME`      | `'magipy'`                | Name of Postgres database                                     |
| `POSTGRES_DJANGO_HOST`        | None                      | Name of Postgres host                                         |
| `POSTGRES_DJANGO_PORT`        | `'5432'`                  | Name of Postgres port                                         |
| `POSTGRES_DJANGO_USER`        | `'postgres'`              | Name of Postgres user                                         |
| `POSTGRES_DJANGO_PASSWORD`    | None                      | Name of Postgres host                                         |
| `MAGI_STATIC_ROOT`            | `'/var/www/magipy/static/'` | Path for static files                                       |
| `MAGIPY_GOOGLE_CLIENT_ID`     | None                      | Google OAuth2 client ID                                       |
| `MAGIPY_GOOGLE_CLIENT_SECRET` | None                      | Google OAuth2 client secret                                   |
| `NODE_MAGI_URL`               | `'http://localhost:8000'` | URL for MAGI server                                           |

We suggest creating a file `ENVIRONMENT` and exporting each variable (e.g. `export MAGI_SITE_URL="http://localhost:8000"`), and then loading these into your shell with `source ENVIRONMENT`.

### Usage ###

Run the server:

    python manage.py runserver $MAGIPY_PORT
