# fuzzer/django_setup.py
import django
from django.conf import settings

def configure_django():
    if settings.configured:
        return

    settings.configure(
        DEBUG=False,
        SECRET_KEY="fuzz_secret",
        INSTALLED_APPS=[
            "app",
            "fuzzer_project",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",   # use RAM DB
            }
        }
    )

    django.setup()

    from django.core.management import call_command
    call_command("makemigrations", "app", verbosity=0)
    call_command("migrate", verbosity=0)
