"""Added new table books

Revision ID: b8a484e6683d
Revises: 
Create Date: 2023-05-01 20:43:38.914386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8a484e6683d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create table books
    op.create_table(
        "books",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("author", sa.String(255), nullable=False),
        sa.Column("pages_count", sa.Integer, nullable=True),
    )


def downgrade() -> None:
    # Drop table books
    op.drop_table("books")
