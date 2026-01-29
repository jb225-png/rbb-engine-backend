"""Add progress tracking fields to generation_jobs

Revision ID: 004
Revises: 003
Create Date: 2024-01-16 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add progress tracking fields to generation_jobs table
    op.add_column('generation_jobs', sa.Column('total_products', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('generation_jobs', sa.Column('completed_products', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('generation_jobs', sa.Column('failed_products', sa.Integer(), nullable=False, server_default='0'))

def downgrade() -> None:
    # Remove progress tracking fields
    op.drop_column('generation_jobs', 'failed_products')
    op.drop_column('generation_jobs', 'completed_products')
    op.drop_column('generation_jobs', 'total_products')