"""init

Revision ID: 968060135d36
Revises: 
Create Date: 2022-03-18 14:21:18.397877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '968060135d36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'api',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('path', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('date_created', sa.Date)
    )
def downgrade():
    op.drop_table('api')
