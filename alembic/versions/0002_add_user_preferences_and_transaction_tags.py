"""add user preferences and transaction tags

Revision ID: 0002_user_prefs_tags
Revises: 0001_budget_planner_init
Create Date: 2026-07-08
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_user_prefs_tags"
down_revision = "0001_budget_planner_init"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("language", sa.String(length=5), nullable=False, server_default="en"))
    op.add_column("users", sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"))
    op.add_column("users", sa.Column("theme_color", sa.String(length=20), nullable=False, server_default="#4f7cff"))
    op.add_column("transactions", sa.Column("tags", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")))


def downgrade() -> None:
    op.drop_column("transactions", "tags")
    op.drop_column("users", "theme_color")
    op.drop_column("users", "currency")
    op.drop_column("users", "language")
