import os
import sys

import django


# This is a header that is required by every file that is going
# to write to the Django ORM. It's extracted to its own file
# for the simple purpose of cleaning up code. It appends all of the
# modules in the Django project to the Python path.
sys.path.append(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../server/')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()
