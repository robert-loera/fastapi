"""add content colun to posts table

Revision ID: efd4686f1e75
Revises: 0baf6d846524
Create Date: 2022-03-28 21:21:27.640665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efd4686f1e75'
down_revision = '0baf6d846524'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
