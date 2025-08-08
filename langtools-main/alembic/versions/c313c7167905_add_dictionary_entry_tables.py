"""add dictionary entry tables

Revision ID: c313c7167905
Revises: f30656839bba
Create Date: 2025-08-08 22:44:24.886286

"""

# for `sqlmodel.sql` access
# pyright: reportAttributeAccessIssue=false
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "c313c7167905"
down_revision: Union[str, Sequence[str], None] = "f30656839bba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create dictionary_entry table
    op.create_table(
        "dictionary_entry",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("json_data", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dictionary_entry_id"), "dictionary_entry", ["id"], unique=False)

    # Create indexes on json_data fields
    op.execute(
        "CREATE INDEX idx_dictionary_entry_meanings_local_id ON dictionary_entry "
        "USING gin ((json_data->'meanings') jsonb_path_ops)"
    )

    # Create dictionary_entry_translation table
    op.create_table(
        "dictionary_entry_translation",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("dictionary_entry_id", sa.String(), nullable=False),
        sa.Column("translation_language", sa.String(), nullable=False),
        sa.Column("json_data", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.ForeignKeyConstraint(
            ["dictionary_entry_id"],
            ["dictionary_entry.id"],
        ),
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

    # Create composite and json indexes
    op.execute(
        "CREATE INDEX idx_dictionary_entry_translation_entry_lang ON dictionary_entry_translation "
        "(dictionary_entry_id, translation_language)"
    )
    op.execute(
        "CREATE INDEX idx_dictionary_entry_translation_meaning_local_id "
        "ON dictionary_entry_translation USING gin ((json_data) jsonb_path_ops)"
    )

    # Create r_user_dictionary_entry table
    op.create_table(
        "r_user_dictionary_entry",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("auth_user_id", sa.String(), nullable=False),
        sa.Column("dictionary_entry_id", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.ForeignKeyConstraint(
            ["auth_user_id"],
            ["auth_user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["dictionary_entry_id"],
            ["dictionary_entry.id"],
        ),
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


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order
    op.drop_index(
        op.f("ix_r_user_dictionary_entry_dictionary_entry_id"), table_name="r_user_dictionary_entry"
    )
    op.drop_index(
        op.f("ix_r_user_dictionary_entry_auth_user_id"), table_name="r_user_dictionary_entry"
    )
    op.drop_index(op.f("ix_r_user_dictionary_entry_id"), table_name="r_user_dictionary_entry")
    op.drop_table("r_user_dictionary_entry")

    # Drop custom indexes
    op.execute("DROP INDEX IF EXISTS idx_dictionary_entry_translation_meaning_local_id")
    op.execute("DROP INDEX IF EXISTS idx_dictionary_entry_translation_entry_lang")

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

    # Drop custom indexes
    op.execute("DROP INDEX IF EXISTS idx_dictionary_entry_meanings_local_id")

    op.drop_index(op.f("ix_dictionary_entry_id"), table_name="dictionary_entry")
    op.drop_table("dictionary_entry")
