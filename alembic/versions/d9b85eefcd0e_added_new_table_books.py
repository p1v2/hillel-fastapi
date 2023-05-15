"""Added new table books

Revision ID: d9b85eefcd0e
Revises: b8a484e6683d
Create Date: 2023-05-14 20:21:45.567433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9b85eefcd0e'
down_revision = 'b8a484e6683d'
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
