"""add fsrs tables

Revision ID: 4e2c1a7b9f10
Revises: 909454950d14
Create Date: 2025-08-11 00:00:00.000000

"""

# for `sqlmodel.sql` access
# pyright: reportAttributeAccessIssue=false
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4e2c1a7b9f10"
down_revision: Union[str, Sequence[str], None] = "909454950d14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create fsrs table
    op.create_table(
        "fsrs",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("due", sa.DateTime(), nullable=False),
        sa.Column("stability", sa.Float(), nullable=True),
        sa.Column("difficulty", sa.Float(), nullable=True),
        sa.Column("state", sa.Integer(), nullable=False),
        sa.Column("step", sa.Integer(), nullable=False),
        sa.Column("last_review", sa.DateTime(), nullable=True),
        sa.Column("reps", sa.Integer(), nullable=False),
        sa.Column("lapses", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_fsrs_id"), "fsrs", ["id"], unique=False)

    # Create r_meaning_translation_fsrs table
    op.create_table(
        "r_meaning_translation_fsrs",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("auth_user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("fsrs_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "dictionary_entry_translation_id",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column("meaning_local_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_r_meaning_translation_fsrs_id"),
        "r_meaning_translation_fsrs",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_r_meaning_translation_fsrs_auth_user_id"),
        "r_meaning_translation_fsrs",
        ["auth_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_r_meaning_translation_fsrs_fsrs_id"),
        "r_meaning_translation_fsrs",
        ["fsrs_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_r_meaning_translation_fsrs_dictionary_entry_translation_id"),
        "r_meaning_translation_fsrs",
        ["dictionary_entry_translation_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_r_meaning_translation_fsrs_meaning_local_id"),
        "r_meaning_translation_fsrs",
        ["meaning_local_id"],
        unique=False,
    )

    # FKs
    op.create_foreign_key(
        "fk_r_meaning_translation_fsrs_auth_user_id",
        "r_meaning_translation_fsrs",
        "auth_user",
        ["auth_user_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_r_meaning_translation_fsrs_fsrs_id",
        "r_meaning_translation_fsrs",
        "fsrs",
        ["fsrs_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_r_meaning_translation_fsrs_dictionary_entry_translation_id",
        "r_meaning_translation_fsrs",
        "dictionary_entry_translation",
        ["dictionary_entry_translation_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop FKs
    op.drop_constraint(
        "fk_r_meaning_translation_fsrs_dictionary_entry_translation_id",
        "r_meaning_translation_fsrs",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_r_meaning_translation_fsrs_fsrs_id",
        "r_meaning_translation_fsrs",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_r_meaning_translation_fsrs_auth_user_id",
        "r_meaning_translation_fsrs",
        type_="foreignkey",
    )

    # Drop indexes and tables
    op.drop_index(
        op.f("ix_r_meaning_translation_fsrs_meaning_local_id"),
        table_name="r_meaning_translation_fsrs",
    )
    op.drop_index(
        op.f("ix_r_meaning_translation_fsrs_dictionary_entry_translation_id"),
        table_name="r_meaning_translation_fsrs",
    )
    op.drop_index(
        op.f("ix_r_meaning_translation_fsrs_fsrs_id"),
        table_name="r_meaning_translation_fsrs",
    )
    op.drop_index(
        op.f("ix_r_meaning_translation_fsrs_auth_user_id"),
        table_name="r_meaning_translation_fsrs",
    )
    op.drop_index(
        op.f("ix_r_meaning_translation_fsrs_id"),
        table_name="r_meaning_translation_fsrs",
    )
    op.drop_table("r_meaning_translation_fsrs")

    op.drop_index(op.f("ix_fsrs_id"), table_name="fsrs")
    op.drop_table("fsrs")
