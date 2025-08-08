"""RMeaningTranslationFsrs SQLModel definition."""

from datetime import datetime
from typing import cast

from sqlalchemy import func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class RMeaningTranslationFsrs(SQLModel, table=True):
    """Database model for r_meaning_translation_fsrs table.

    Links FSRS records to specific meaning translations by meaning_local_id.
    Creates a one-to-one relationship between fsrs and individual AiMeaningTranslation records.
    """

    __tablename__ = cast(declared_attr[str], "r_meaning_translation_fsrs")

    id: str = Field(primary_key=True, index=True)
    dictionary_entry_translation_id: str = Field(
        foreign_key="dictionary_entry_translation.id", index=True
    )
    meaning_local_id: str = Field(
        index=True, description="meaning_local_id from AiMeaningTranslation"
    )
    fsrs_id: str = Field(foreign_key="fsrs.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )
