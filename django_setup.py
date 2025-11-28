# fuzzer/django_setup.py
import django
from django.conf import settings

def configure_django():
    if settings.configured:
        return
    '''
    settings.configure(
        DEBUG=False,
        SECRET_KEY="fuzz_secret",
        INSTALLED_APPS=[
            "app",
            # "fuzzer_project",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",   # use RAM DB
            }
        }
    )  
    '''

    settings.configure(
        DEBUG=False,
        SECRET_KEY="fuzz_secret",
        INSTALLED_APPS=[
            # "django_sql_fuzzer.app.apps.FuzzerAppConfig",
            # "app.apps.FuzzerAppConfig",
            "app"
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": "fuzzdb",
                "USER": "root",
                "PASSWORD": "root",
                "HOST": "127.0.0.1",
                "PORT": "3306",
                "CONN_MAX_AGE": 0,    # important for fuzzing stability
                "OPTIONS": {
                    "sql_mode": "STRICT_ALL_TABLES",  # best for fuzzing
                }
            }
        }
    )


    django.setup()

    from django.core.management import call_command
    call_command("makemigrations", "app", verbosity=0)
    call_command("migrate", verbosity=0)
