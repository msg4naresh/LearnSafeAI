"""
SQLAlchemy mapping of QuestionAnalysis table
"""

import datetime
from uuid import UUID as UUID4
from uuid import uuid4

from sqlalchemy import DateTime, Enum, Integer, String, Text, ARRAY, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, validates
from dateutil.parser import parse, ParserError


Base = declarative_base()

class QuestionAnalysis(Base):
    """QuestionAnalysis table represents the analysis of a question."""

    __tablename__ = 'question_analysis'
    caption = "Question Analysis"
    description = "Holds the analysis information of questions"

    id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid4,
        comment="The unique identifier assigned to a question analysis.",
        info={"verbose_name": "ID"},
    )
    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="The text of the analyzed question.",
        info={"verbose_name": "Question Text"},
    )
    category: Mapped[str] = mapped_column(
        String(255),
        comment="The category of the question.",
        info={"verbose_name": "Category"},
    )
    expertise_rating: Mapped[int] = mapped_column(
        Integer,
        comment="The expertise rating of the question.",
        info={"verbose_name": "Expertise Rating"},
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="The creation date of the question analysis.",
        info={"verbose_name": "Created At"},
    )
    knowledge_gaps: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        comment="The identified knowledge gaps in the question.",
        info={"verbose_name": "Knowledge Gaps"},
    )
    recommendations: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        comment="The recommendations based on the question analysis.",
        info={"verbose_name": "Recommendations"},
    )

    @validates("id")
    def validate_uuid(self, key, value):
        if value is None:
            raise ValueError(f"{key}: value cannot be None")
        if not isinstance(value, (UUID4, UUID)):
            try:
                val_as_uuid = UUID4(value)
            except (AttributeError, ValueError) as err:
                raise ValueError(f"{key}: {value} is not a valid UUID") from err
            return val_as_uuid
        return value

    @validates("question_text")
    def validate_text(self, key, value):
        if value is None:
            raise ValueError(f"{key}: value cannot be None")
        if not isinstance(value, str):
            raise ValueError(f"{key}: {value} is not a valid string")
        return value

    @validates("category")
    def validate_string_255(self, key, value):
        if value is None:
            return value
        if not isinstance(value, str) or len(value) > 255:
            raise ValueError(f"{key}: {value} is not a valid string under 255 characters")
        return value

    @validates("expertise_rating")
    def validate_integer(self, key, value):
        if value is None:
            return value
        if not isinstance(value, int):
            raise ValueError(f"{key}: {value} is not a valid integer")
        return value

    @validates("created_at")
    def validate_dates(self, key, value):
        if value is None:
            raise ValueError(f"{key}: value cannot be None")
        if not isinstance(value, (datetime.datetime, datetime.date)):
            if isinstance(value, str):
                try:
                    return parse(value)
                except ParserError as err:
                    raise ValueError(f"{key}: {value} is not a valid datetime coercible string or datetime") from err
            else:
                raise ValueError(f"{key}: {value} is not a valid datetime coercible string or datetime")
        return value

    @validates("knowledge_gaps", "recommendations")
    def validate_array(self, key, value):
        if value is None:
            return value
        if not isinstance(value, list):
            raise ValueError(f"{key}: {value} is not a valid list")
        return value
