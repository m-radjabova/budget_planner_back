"""add user firebase uid

Revision ID: 0004_user_firebase_uid
Revises: 0003_drop_user_prefs
Create Date: 2026-07-13
"""

from alembic import op
import sqlalchemy as sa


revision = "0004_user_firebase_uid"
down_revision = "0003_drop_user_prefs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("firebase_uid", sa.String(length=128), nullable=True))
    op.create_index(op.f("ix_users_firebase_uid"), "users", ["firebase_uid"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_firebase_uid"), table_name="users")
    op.drop_column("users", "firebase_uid")
