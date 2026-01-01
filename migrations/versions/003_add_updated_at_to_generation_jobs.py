"""Add updated_at to generation_jobs

Revision ID: 003
Revises: 002
Create Date: 2024-01-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add updated_at column to generation_jobs table
    op.add_column('generation_jobs', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    
    # Set onupdate trigger for updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    op.execute("""
        CREATE TRIGGER update_generation_jobs_updated_at 
        BEFORE UPDATE ON generation_jobs 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)

def downgrade() -> None:
    # Drop trigger and function
    op.execute("DROP TRIGGER IF EXISTS update_generation_jobs_updated_at ON generation_jobs")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")
    
    # Remove updated_at column
    op.drop_column('generation_jobs', 'updated_at')