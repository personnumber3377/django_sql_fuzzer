# fuzzer/database_seed.py
from datetime import datetime, timedelta, date, time
from decimal import Decimal
from django.utils import timezone

from app.models import (
    Company, Employee, Author, Publisher, Book, Store,
    Experiment, DTModel, DurationFieldModel, JSONFieldModel,
)

def seed_all():
    seed_companies()
    seed_books_authors()
    seed_durations()
    seed_datetime_models()


def seed_companies():
    ceo1 = Employee.objects.create(firstname="Alice", lastname="CEO", salary=100)
    ceo2 = Employee.objects.create(firstname="Bob", lastname="Boss", salary=200)

    Company.objects.create(name="Example Inc", num_employees=50, num_chairs=20, ceo=ceo1)
    Company.objects.create(name="TestCorp", num_employees=10, num_chairs=5, ceo=ceo2)


def seed_books_authors():
    a1 = Author.objects.create(name="Author One", age=30)
    a2 = Author.objects.create(name="Author Two", age=40)
    p = Publisher.objects.create(name="Publisher House", num_awards=2)

    b1 = Book.objects.create(
        isbn="123456789",
        pages=200,
        rating=4.7,
        price=Decimal("10.99"),
        contact=a1,
        publisher=p,
        pubdate=date(2010, 1, 1),
        name="Book One",
    )
    b2 = Book.objects.create(
        isbn="987654321",
        pages=300,
        rating=4.0,
        price=Decimal("15.49"),
        contact=a2,
        publisher=p,
        pubdate=date(2012, 2, 2),
        name="Book Two",
    )
    b1.authors.add(a1)
    b2.authors.add(a2)


def seed_durations():
    DurationFieldModel.objects.create(dt=timedelta(hours=4))
    JSONFieldModel.objects.create(data={"description": "Hello"})


def seed_datetime_models():
    dt1 = datetime(2015, 6, 15, 14, 30, 50, 321)
    dt2 = datetime(2016, 6, 15, 14, 10, 50, 123)

    if timezone.is_aware(dt1) is False:
        dt1 = timezone.make_aware(dt1)
        dt2 = timezone.make_aware(dt2)

    DTModel.objects.create(
        name="dt1", start_datetime=dt1, end_datetime=dt2,
        start_date=dt1.date(), end_date=dt2.date(),
        start_time=dt1.time(), end_time=dt2.time(),
        duration=dt2 - dt1
    )
