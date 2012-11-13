#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    fc_env = os.environ.get("FC_ENV")
    if fc_env == None:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
    else:
        if fc_env.lower() == "dev":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
        elif fc_env.lower() == "heroku-alpha":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.heroku-alpha")
        elif fc_env.lower() == "heroku-beta":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.heroku-beta")
        elif fc_env.lower() == "heroku-production":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.heroku-production")
        else:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
