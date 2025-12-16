# RBB Engine - Database Entities

## Multi-Locale Design (India-First)

The RBB Engine is designed with **India as the default locale**, supporting CBSE curriculum primarily, with extensibility for other regions like the US (Common Core).

### Locale System
- **Default Locale**: `IN` (India)
- **Default Curriculum**: `CBSE` (Central Board of Secondary Education)
- **Default Currency**: `INR` (Indian Rupee)
- **Grade Levels**: 1-12 (aligned with Indian education system)

### Supported Locales
- **India (IN)**: CBSE curriculum, grades 1-12, INR currency
- **United States (US)**: Common Core curriculum, grades 1-12, USD currency

## Core Entities Overview

### Standards
Input units that define what content should be generated.
- **Purpose**: Educational standards or requirements that drive content generation
- **Key Fields**: 
  - `locale` (IN/US, default: IN)
  - `curriculum_board` (CBSE/COMMON_CORE, default: CBSE)
  - `grade_level` (1-12)
  - `grade_range` (optional, e.g., "6-8")
  - `code` (unique per locale+curriculum)
  - `description`
- **Usage**: Referenced by generation jobs to determine what type of content to create
- **India Examples**: "CBSE.MATH.6.1", "CBSE.SCI.7.2"

### Products
Individual pieces of generated educational content.
- **Purpose**: The actual output items (worksheets, passages, quizzes, etc.)
- **Key Fields**: 
  - `standard_id` (references Standards)
  - `generation_job_id` (references GenerationJob, optional)
  - `product_type` (WORKSHEET/PASSAGE/QUIZ/ASSESSMENT)
  - `status` (DRAFT/GENERATED/FAILED)
  - `locale` (IN/US, default: IN)
  - `curriculum_board` (CBSE/COMMON_CORE, default: CBSE)
  - `grade_level` (1-12)
- **Usage**: Core deliverable that gets bundled and sent to clients
- **Lifecycle**: DRAFT → GENERATED (success) or FAILED (error)
- **Relationships**: Linked to Standards (required) and GenerationJobs (optional)

### Generation Jobs
Automated or manual tasks that create products.
- **Purpose**: Tracks the process of generating content from standards
- **Key Fields**: 
  - `locale` (IN/US, default: IN)
  - `curriculum_board` (CBSE/COMMON_CORE, default: CBSE)
  - `grade_level` (1-12)
  - `job_type` (SINGLE_PRODUCT/FULL_BUNDLE)
  - `status` (PENDING/RUNNING/COMPLETED/FAILED)
  - `standard_id` (references Standards)
- **Usage**: Triggered by dashboard or n8n workflows to create products

### File Artifacts
Physical files associated with products (JSON, ZIP, etc.).
- **Purpose**: Store references to generated files and their metadata
- **Key Fields**: 
  - `locale` (IN/US, default: IN)
  - `file_type` (RAW_JSON/FINAL_JSON/METADATA_JSON/PDF/ZIP/THUMBNAIL)
  - `file_path` (relative path in storage)
  - `product_id` (references Products)
- **Usage**: Track all files created during generation process

### Upload Tasks
Tasks assigned to VA team for manual content processing.
- **Purpose**: Track manual work required for product finalization
- **Key Fields**: product_id, status
- **Usage**: Workflow management for human-in-the-loop processes

### Validation Rules
- **Locale-Curriculum Consistency**: 
  - India (IN) → must use CBSE
  - US → must use Common Core
- **Grade Level Range**: 1-12 for all locales
- **Unique Constraints**: Standards must be unique per locale+curriculum+code

### Future Entities
- **Bundles**: Collections of 12 related products grouped together
- **Users**: Basic user management for system access