"""drop user language and theme color

Revision ID: 0003_drop_user_prefs
Revises: 0002_user_prefs_tags
Create Date: 2026-07-09
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_drop_user_prefs"
down_revision = "0002_user_prefs_tags"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("users", "theme_color")
    op.drop_column("users", "language")


def downgrade() -> None:
    op.add_column("users", sa.Column("language", sa.String(length=5), nullable=False, server_default="en"))
    op.add_column("users", sa.Column("theme_color", sa.String(length=20), nullable=False, server_default="#4f7cff"))
