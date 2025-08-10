"""add is_e2e_test to auth_user

Revision ID: 4f1e3b2c1d2e
Revises: 909454950d14
Create Date: 2025-08-10 18:45:00.000000

"""

# for `sqlmodel.sql` access
# pyright: reportAttributeAccessIssue=false
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4f1e3b2c1d2e"
down_revision: Union[str, Sequence[str], None] = "909454950d14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: add is_e2e_test column to auth_user."""
    op.add_column(
        "auth_user",
        sa.Column("is_e2e_test", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )


def downgrade() -> None:
    """Downgrade schema: drop is_e2e_test column from auth_user."""
    op.drop_column("auth_user", "is_e2e_test")
