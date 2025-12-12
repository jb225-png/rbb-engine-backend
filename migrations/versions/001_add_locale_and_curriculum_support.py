"""Add locale and curriculum support

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create enum types
    locale_enum = sa.Enum('IN', 'US', name='locale')
    curriculum_enum = sa.Enum('CBSE', 'COMMON_CORE', name='curriculumboard')
    job_status_enum = sa.Enum('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', name='jobstatus')
    product_type_enum = sa.Enum('WORKSHEET', 'PASSAGE', 'QUIZ', 'ASSESSMENT', name='producttype')
    product_status_enum = sa.Enum('DRAFT', 'GENERATED', 'REVIEWED', 'PUBLISHED', name='productstatus')
    job_type_enum = sa.Enum('SINGLE_PRODUCT', 'FULL_BUNDLE', name='jobtype')
    file_type_enum = sa.Enum('RAW_JSON', 'FINAL_JSON', 'METADATA_JSON', 'PDF', 'ZIP', 'THUMBNAIL', name='filetype')
    
    # Create standards table
    op.create_table('standards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('locale', locale_enum, nullable=False, server_default='IN'),
        sa.Column('curriculum_board', curriculum_enum, nullable=False, server_default='CBSE'),
        sa.Column('grade_level', sa.Integer(), nullable=False),
        sa.Column('grade_range', sa.String(), nullable=True),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_standards_id', 'standards', ['id'])
    op.create_index('ix_standards_locale', 'standards', ['locale'])
    op.create_index('ix_standards_curriculum_board', 'standards', ['curriculum_board'])
    op.create_index('ix_standards_grade_level', 'standards', ['grade_level'])
    op.create_index('ix_standards_code', 'standards', ['code'])
    op.create_index('ix_standards_locale_curriculum', 'standards', ['locale', 'curriculum_board'])
    op.create_index('ix_standards_code_unique', 'standards', ['locale', 'curriculum_board', 'code'], unique=True)

    # Create products table
    op.create_table('products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('standard_id', sa.Integer(), nullable=False),
        sa.Column('locale', locale_enum, nullable=False, server_default='IN'),
        sa.Column('curriculum_board', curriculum_enum, nullable=False, server_default='CBSE'),
        sa.Column('grade_level', sa.Integer(), nullable=False),
        sa.Column('product_type', product_type_enum, nullable=False),
        sa.Column('status', product_status_enum, nullable=True, server_default='DRAFT'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_products_id', 'products', ['id'])
    op.create_index('ix_products_standard_id', 'products', ['standard_id'])
    op.create_index('ix_products_locale', 'products', ['locale'])
    op.create_index('ix_products_curriculum_board', 'products', ['curriculum_board'])
    op.create_index('ix_products_grade_level', 'products', ['grade_level'])
    op.create_index('ix_products_product_type', 'products', ['product_type'])
    op.create_index('ix_products_status', 'products', ['status'])
    op.create_index('ix_products_locale_curriculum', 'products', ['locale', 'curriculum_board'])
    op.create_index('ix_products_standard_status', 'products', ['standard_id', 'status'])
    op.create_index('ix_products_type_status', 'products', ['product_type', 'status'])

    # Create generation_jobs table
    op.create_table('generation_jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('standard_id', sa.Integer(), nullable=False),
        sa.Column('locale', locale_enum, nullable=False, server_default='IN'),
        sa.Column('curriculum_board', curriculum_enum, nullable=False, server_default='CBSE'),
        sa.Column('grade_level', sa.Integer(), nullable=False),
        sa.Column('job_type', job_type_enum, nullable=False),
        sa.Column('status', job_status_enum, nullable=True, server_default='PENDING'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_generation_jobs_id', 'generation_jobs', ['id'])
    op.create_index('ix_generation_jobs_standard_id', 'generation_jobs', ['standard_id'])
    op.create_index('ix_generation_jobs_locale', 'generation_jobs', ['locale'])
    op.create_index('ix_generation_jobs_curriculum_board', 'generation_jobs', ['curriculum_board'])
    op.create_index('ix_generation_jobs_grade_level', 'generation_jobs', ['grade_level'])
    op.create_index('ix_generation_jobs_job_type', 'generation_jobs', ['job_type'])
    op.create_index('ix_generation_jobs_status', 'generation_jobs', ['status'])
    op.create_index('ix_generation_jobs_locale_curriculum', 'generation_jobs', ['locale', 'curriculum_board'])
    op.create_index('ix_generation_jobs_status_created', 'generation_jobs', ['status', 'created_at'])
    op.create_index('ix_generation_jobs_standard_type', 'generation_jobs', ['standard_id', 'job_type'])

    # Create file_artifacts table
    op.create_table('file_artifacts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('locale', locale_enum, nullable=False, server_default='IN'),
        sa.Column('file_type', file_type_enum, nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_file_artifacts_id', 'file_artifacts', ['id'])
    op.create_index('ix_file_artifacts_product_id', 'file_artifacts', ['product_id'])
    op.create_index('ix_file_artifacts_locale', 'file_artifacts', ['locale'])
    op.create_index('ix_file_artifacts_file_type', 'file_artifacts', ['file_type'])
    op.create_index('ix_file_artifacts_product_type', 'file_artifacts', ['product_id', 'file_type'])

def downgrade() -> None:
    op.drop_table('file_artifacts')
    op.drop_table('generation_jobs')
    op.drop_table('products')
    op.drop_table('standards')
    
    # Drop enum types
    sa.Enum(name='filetype').drop(op.get_bind())
    sa.Enum(name='jobtype').drop(op.get_bind())
    sa.Enum(name='productstatus').drop(op.get_bind())
    sa.Enum(name='producttype').drop(op.get_bind())
    sa.Enum(name='jobstatus').drop(op.get_bind())
    sa.Enum(name='curriculumboard').drop(op.get_bind())
    sa.Enum(name='locale').drop(op.get_bind())