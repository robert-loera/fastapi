"""add user table

Revision ID: 487dd7a6a23e
Revises: efd4686f1e75
Create Date: 2022-03-28 21:40:17.520314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '487dd7a6a23e'
down_revision = 'efd4686f1e75'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    # assure we cannot have duplicate emails
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
