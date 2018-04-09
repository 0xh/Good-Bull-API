# Good-Bull-API
An API that serves information about professors (and their distributions), courses, sections, and buildings pulled from around the tamu.edu website.

## Installing Dependencies
To install all dependencies, first, it's highly recommended that you create a virtual environment using `virtualenv`.
`cd /into/your/cloned/version/`
`virtualenv env`

This will create a virtual environment so that all of the dependencies aren't immediately installed to your global Python installation.

To actually _install_ the dependencies, simply execute the following command.
`pip install -r requirements.txt`

## Outlining/Creating Tables
To outline all of the required tables, first do the following (taken from the Django Rest Framework documentation):
`python manage.py makemigrations`

To create all of the required tables, do the following:
`python manage.py migrate --run-syncdb`

## Deleting Tables
To delete tables, simply go to each individual app's directory, and recursively-remove its `migrations` directory. Afterwards, find the database file (at the time of writing, it is `db.sqlite3` found in the `server` directory) and delete it.

Then, re-run the above commands to outline and create the required tables.

## Troubleshooting
If you encounter the following `no such table <appname>_<appname>`, you need to create the required tables. See the above instructions to do so.
