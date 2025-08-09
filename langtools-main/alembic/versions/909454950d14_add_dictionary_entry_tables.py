"""add_dictionary_entry_tables

Revision ID: 909454950d14
Revises: f30656839bba
Create Date: 2025-08-09 22:01:59.074850

"""

# for `sqlmodel.sql` access
# pyright: reportAttributeAccessIssue=false
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "909454950d14"
down_revision: Union[str, Sequence[str], None] = "f30656839bba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create dictionary_entry table
    op.create_table(
        "dictionary_entry",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("json_data", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dictionary_entry_id"), "dictionary_entry", ["id"], unique=False)

    # Create r_user_dictionary_entry table
    op.create_table(
        "r_user_dictionary_entry",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("auth_user_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("dictionary_entry_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_r_user_dictionary_entry_id"), "r_user_dictionary_entry", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_r_user_dictionary_entry_auth_user_id"),
        "r_user_dictionary_entry",
        ["auth_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_r_user_dictionary_entry_dictionary_entry_id"),
        "r_user_dictionary_entry",
        ["dictionary_entry_id"],
        unique=False,
    )

    # Create dictionary_entry_translation table
    op.create_table(
        "dictionary_entry_translation",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("dictionary_entry_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("translation_language", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("json_data", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_dictionary_entry_translation_id"),
        "dictionary_entry_translation",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_dictionary_entry_translation_dictionary_entry_id"),
        "dictionary_entry_translation",
        ["dictionary_entry_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_dictionary_entry_translation_translation_language"),
        "dictionary_entry_translation",
        ["translation_language"],
        unique=False,
    )

    # Add foreign key constraints
    op.create_foreign_key(
        "fk_r_user_dictionary_entry_auth_user_id",
        "r_user_dictionary_entry",
        "auth_user",
        ["auth_user_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_r_user_dictionary_entry_dictionary_entry_id",
        "r_user_dictionary_entry",
        "dictionary_entry",
        ["dictionary_entry_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_dictionary_entry_translation_dictionary_entry_id",
        "dictionary_entry_translation",
        "dictionary_entry",
        ["dictionary_entry_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign key constraints
    op.drop_constraint(
        "fk_dictionary_entry_translation_dictionary_entry_id",
        "dictionary_entry_translation",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_r_user_dictionary_entry_dictionary_entry_id",
        "r_user_dictionary_entry",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_r_user_dictionary_entry_auth_user_id", "r_user_dictionary_entry", type_="foreignkey"
    )

    # Drop indexes and tables in reverse order
    op.drop_index(
        op.f("ix_dictionary_entry_translation_translation_language"),
        table_name="dictionary_entry_translation",
    )
    op.drop_index(
        op.f("ix_dictionary_entry_translation_dictionary_entry_id"),
        table_name="dictionary_entry_translation",
    )
    op.drop_index(
        op.f("ix_dictionary_entry_translation_id"), table_name="dictionary_entry_translation"
    )
    op.drop_table("dictionary_entry_translation")

    op.drop_index(
        op.f("ix_r_user_dictionary_entry_dictionary_entry_id"), table_name="r_user_dictionary_entry"
    )
    op.drop_index(
        op.f("ix_r_user_dictionary_entry_auth_user_id"), table_name="r_user_dictionary_entry"
    )
    op.drop_index(op.f("ix_r_user_dictionary_entry_id"), table_name="r_user_dictionary_entry")
    op.drop_table("r_user_dictionary_entry")

    op.drop_index(op.f("ix_dictionary_entry_id"), table_name="dictionary_entry")
    op.drop_table("dictionary_entry")
