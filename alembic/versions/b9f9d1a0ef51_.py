"""empty message

Revision ID: b9f9d1a0ef51
Revises: 
Create Date: 2023-05-11 14:00:21.269404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9f9d1a0ef51'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("books",
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String(255), nullable=False),
    sa.Column("author", sa.String(255), nullable=False),
    sa.Column("pages_count", sa.Integer, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("books")
