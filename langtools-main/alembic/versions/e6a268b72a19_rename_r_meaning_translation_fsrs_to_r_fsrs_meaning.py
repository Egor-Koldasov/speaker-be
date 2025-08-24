"""empty message

Revision ID: e6a268b72a19
Revises: d056f23efb11
Create Date: 2025-08-24 22:33:57.352490

"""

# for `sqlmodel.sql` access
# pyright: reportAttributeAccessIssue=false
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e6a268b72a19"
down_revision: Union[str, Sequence[str], None] = "d056f23efb11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("r_meaning_translation_fsrs", "r_fsrs_meaning")


def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table("r_fsrs_meaning", "r_meaning_translation_fsrs")
