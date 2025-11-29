import os
from datetime import date

import django
from django.db.models import Q, Count, F, Case, When
from django.db.models.fields import DecimalField

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Publisher, Author, Book


# Create queries within functions
def populate_db():
    epic_reads = Publisher.objects.create(
        name="Epic Reads",
        country="USA",
        established_date=date(1923, 5, 15),
        rating=4.94
    )

    global_prints = Publisher.objects.create(
        name="Global Prints",
        country="Australia",
    )

    abrams_books = Publisher.objects.create(
        name="Abrams Books",
        rating=1.05
    )

    jack_london = Author.objects.create(
        name="Jack London",
        country="USA",
        birth_date=date(1876, 1, 12),
        is_active=False
    )

    craig_richardson = Author.objects.create(
        name="Craig Richardson",
    )

    ramsey_hamilton = Author.objects.create(
        name="Ramsey Hamilton",
    )

    luciano_ramalho = Author.objects.create(
        name="Luciano Ramalho",
    )

    book1 = Book.objects.create(
        title="Adventures in Python",
        publication_date=date(2015, 6, 1),
        summary="An engaging and detailed guide to mastering a popular programming language.",
        genre="NONFICTION",
        price=49.99,
        rating=4.8,
        publisher=epic_reads,
        main_author=craig_richardson,
    )
    book1.co_authors.add(ramsey_hamilton)

    book2 = Book.objects.create(
        title="The Call of the Wild",
        publication_date=date(1903, 11, 23),
        summary="A classic fiction adventure story set during the Klondike Gold Rush.",
        genre="FICTION",
        price=29.99,
        rating=4.9,
        is_bestseller=True,
        publisher=global_prints,
        main_author=jack_london,
    )

    book3 = Book.objects.create(
        title="Django World",
        publication_date=date(2025, 1, 1),
        summary="A comprehensive resource for advanced users of the Django web framework.",
        genre="NONFICTION",
        price=90.00,
        rating=5.0,
        publisher=epic_reads,
        main_author=craig_richardson,
    )
    book3.co_authors.add(luciano_ramalho, ramsey_hamilton)

    book4 = Book.objects.create(
        title="Integration Testing",
        publication_date=date(2024, 12, 31),
        summary="A thorough exploration of expert-level testing strategies.",
        genre="NONFICTION",
        price=89.99,
        rating=4.89,
        is_bestseller=True,
        publisher=epic_reads,
        main_author=ramsey_hamilton,
    )

    book5 = Book.objects.create(
        title="Unit Testing",
        publication_date=date(2025, 2, 1),
        summary="A detailed guide to foundational testing principles.",
        genre="NONFICTION",
        price=50.00,
        rating=3.99,
        publisher=epic_reads,
        main_author=craig_richardson,
    )
    book5.co_authors.add(ramsey_hamilton)

    return "Database populated successfully!"


def get_publishers(search_string=None):
    if search_string is None:
        return 'No search criteria.'

    publishers = Publisher.objects.filter(
        Q(name__icontains=search_string)
            |
        Q(country__icontains=search_string)
    ).order_by('-rating', 'name')

    if not publishers.exists():
        return 'No publishers found.'

    return '\n'.join(f"Publisher: {p.name}, country: {'Unknown' if p.country == 'TBC' else p.country}, rating: {p.rating:.1f}" for p in publishers)


def get_top_publisher():
    if Publisher.objects.all().count() == 0:
        return 'No publishers found.'

    p = Publisher.objects.get_publishers_by_books_count().first()

    return f"Top Publisher: {p.name} with {p.books_count} books."


def get_top_main_author():
    if Author.objects.all().count() == 0 or Book.objects.count() == 0:
        return 'No results.'
    a = Author.objects.annotate(num_books=Count('books')).order_by('-num_books', 'name').first()
    return f"Top Author: {a.name}, own book titles: {', '.join(b.title for b in a.books.all())}, books average rating: {sum(b.rating for b in a.books.all()) / a.books.all().count():.1f}"


def get_authors_by_books_count():
    if Author.objects.all().count() == 0 or Book.objects.count() == 0:
        return 'No results.'

    authors = Author.objects.annotate(all_books=Count('books') + Count('co_authored_books', distinct=True)).order_by('-all_books', 'name')[:3]

    return '\n'.join(f"{a.name} authored {a.all_books} books." for a in authors)


def get_bestseller():
    b = (Book.objects.filter(is_bestseller=True)
         .prefetch_related('co_authors')
         .annotate(num_of_authors=Count('co_authors', distinct=True) + 1)
         .annotate(composite_index=F('rating') + F('num_of_authors'))
         .first())

    return f"Top bestseller: {b.title}, index: {b.composite_index:.1f}. Main author: {b.main_author.name}. Co-authors: {'/'.join(a.name for a in b.co_authors.distinct()) if b.co_authors.exists() else 'N/A'}."


def increase_price():
    books = (Book.objects.filter(publication_date__year=2025)
             .annotate(total_rating=F('rating') + F('publisher__rating'))
             .filter(total_rating__gte=8.0)
             .update(price=Case(When(
        price__gt=50.0, then=F('price') * 1.1),
        default=F('price') * 1.2,
        output_field=DecimalField(
            max_digits=6, decimal_places=2
    )))
             )

    if not books:
        return 'No changes in price.'

    return f"Prices increased for {books} book/s."

