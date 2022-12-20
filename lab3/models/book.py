"""Описание моделей."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, func, cast
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional
    from sqlalchemy.orm import Session

Base = declarative_base()


class Author(Base):
    """Модель автора."""
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    third_name = Column(String, nullable=True)

    @hybrid_property
    def name(self) -> str:
        """Имя автора."""
        return f"{self.second_name} {self.first_name} {self.third_name or ''}"

    @name.expression
    def name(self):
        return func.concat(self.second_name, " ", self.first_name, " ", self.third_name)


class Book(Base):
    """Модель книги."""
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)

    author: Author = relationship("Author")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "year": self.year,
            "author": self.author.name,
        }

    @classmethod
    def get_all(cls, session: Session, column: Optional[str]) -> List[Dict[str, Any]]:
        """Выдача всей таблицы."""
        result = None
        if column != "all":
            if column == "id":
                result = [{"id": item.id} for item in
                          session.query(Book.id.label("id")).select_from(Book).distinct().all()]
            if column == "name":
                result = [{"name": item.name} for item in
                          session.query(Book.name.label("name")).select_from(Book).distinct().all()]
            if column == "year":
                result = [{"year": item.year} for item in
                          session.query(Book.year.label("year")).select_from(Book).distinct().all()]
            if column == "author":
                result = [{"author": item.author} for item in
                          session.query(Author.name.label("author")).select_from(Author).join(Book).distinct().all()]
        else:
            result = [item.to_dict() for item in session.query(Book).all()]
        return result

    @classmethod
    def aggregation_result(cls, session: Session, column: str, func_agg: str) -> float:
        """Выдача результатов агрегации."""
        choosed_column = Book.id
        choosed_func = func.count
        if column == "year":
            choosed_column = Book.year

        if func_agg == "max":
            choosed_func = func.max
        if func_agg == "min":
            choosed_func = func.min

        if func == "count":
            result = session.query(choosed_column).select_from(Book).count()
        else:
            result = session.query(choosed_func(choosed_column)).scalar()

        return result

    @classmethod
    def filtered_query(cls, session: Session, field: str, value: str) -> List[Dict[str, Any]]:
        """Фильтрация."""
        query = session.query(Book).join(Author)

        if field == "id":
            query = query.filter(cast(Book.id, String).ilike(f"%{value}%"))
        if field == "name":
            query = query.filter(Book.name.ilike(f"%{value}%"))
        if field == "year":
            query = query.filter(cast(Book.year, String).ilike(f"%{value}%"))
        if field == "author":
            query = query.filter(Author.name.ilike(f"%{value}%"))

        return [item.to_dict() for item in query.all()]
