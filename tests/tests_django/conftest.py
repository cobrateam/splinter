import os
import sys

import django


sys.path.append("tests/fake_django")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"


django.setup()
