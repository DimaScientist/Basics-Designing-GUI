from __future__ import annotations

from .book import *

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

SELECT_COLUMNS = ["all", "id", "name", "year", "author"]

AGGREGATION_COLUMNS = ["id", "year"]
AGGREGATION_FUNCTIONS = ["count", "min", "max"]

FILTER_COLUMNS = ["id", "name", "year", "author"]


def fill_db(session: Session) -> None:
    """Заполнение БД."""
    if session.query(Author).count() == 0:
        session.add_all([
            Author(id=1, first_name="Александр", second_name="Пушкин", third_name="Сергеевич"),
            Author(id=2, first_name="Николай", second_name="Гоголь", third_name="Васильевич"),
            Author(id=3, first_name="Джордж", second_name="Мартин"),
            Author(id=4, first_name="Джон", second_name="Толкин"),
            Author(id=5, first_name="Лев", second_name="Толстой", third_name="Николаевич"),
        ])
        session.commit()

    if session.query(Book).count() == 0:
        session.add_all([
            Book(id=1, name="Капитанская дочка", year=1836, author_id=1),
            Book(id=2, name="Война и мир", year=1873, author_id=5),
            Book(id=3, name="Властелин Колец: Братство кольца", year=1954, author_id=4),
            Book(id=4, name="Властелин Колец: Две башни", year=1954, author_id=4),
            Book(id=5, name="Властелин колец: Возвращение короля", year=1955, author_id=4),
            Book(id=6, name="Тарас Бульба", year=1835, author_id=2),
            Book(id=6, name="Песнь льда и огня", year=1996, author_id=3),
        ])
        session.commit()
