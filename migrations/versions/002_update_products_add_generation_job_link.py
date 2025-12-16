"""Update products add generation job link

Revision ID: 002
Revises: 001
Create Date: 2024-01-16 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Update product status enum to match Day 5 requirements
    op.execute("ALTER TYPE productstatus RENAME TO productstatus_old")
    
    # Create new enum with updated values
    new_product_status_enum = sa.Enum('DRAFT', 'GENERATED', 'FAILED', name='productstatus')
    new_product_status_enum.create(op.get_bind())
    
    # Add generation_job_id column to products table
    op.add_column('products', sa.Column('generation_job_id', sa.Integer(), nullable=True))
    
    # Update status column to use new enum
    op.execute("ALTER TABLE products ALTER COLUMN status TYPE productstatus USING status::text::productstatus")
    
    # Drop old enum
    op.execute("DROP TYPE productstatus_old")
    
    # Create indexes for new column
    op.create_index('ix_products_generation_job_id', 'products', ['generation_job_id'])
    op.create_index('ix_products_status_type', 'products', ['status', 'product_type'])
    
    # Drop old indexes that are being replaced
    op.drop_index('ix_products_locale_curriculum', 'products')
    op.drop_index('ix_products_type_status', 'products')

def downgrade() -> None:
    # Recreate old indexes
    op.create_index('ix_products_locale_curriculum', 'products', ['locale', 'curriculum_board'])
    op.create_index('ix_products_type_status', 'products', ['product_type', 'status'])
    
    # Drop new indexes
    op.drop_index('ix_products_status_type', 'products')
    op.drop_index('ix_products_generation_job_id', 'products')
    
    # Remove generation_job_id column
    op.drop_column('products', 'generation_job_id')
    
    # Revert enum changes
    op.execute("ALTER TYPE productstatus RENAME TO productstatus_new")
    
    # Recreate old enum
    old_product_status_enum = sa.Enum('DRAFT', 'GENERATED', 'REVIEWED', 'PUBLISHED', name='productstatus')
    old_product_status_enum.create(op.get_bind())
    
    # Update status column to use old enum
    op.execute("ALTER TABLE products ALTER COLUMN status TYPE productstatus USING 'DRAFT'::productstatus")
    
    # Drop new enum
    op.execute("DROP TYPE productstatus_new")