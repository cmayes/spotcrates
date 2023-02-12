"""Add a column

Revision ID: 5aac0c2505d9
Revises: 5b47a2873750
Create Date: 2023-01-15 17:12:18.182583

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5aac0c2505d9'
down_revision = '5b47a2873750'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))


def downgrade():
    op.drop_column('account', 'last_transaction_date')
