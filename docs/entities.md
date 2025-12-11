# RBB Engine - Database Entities

## Core Entities Overview

### Standards
Input units that define what content should be generated.
- **Purpose**: Educational standards or requirements that drive content generation
- **Key Fields**: code (unique identifier), description
- **Usage**: Referenced by generation jobs to determine what type of content to create

### Products
Individual pieces of generated educational content.
- **Purpose**: The actual output items (worksheets, passages, quizzes, etc.)
- **Key Fields**: standard_id (what standard it fulfills), type, status
- **Usage**: Core deliverable that gets bundled and sent to clients

### Generation Jobs
Automated or manual tasks that create products.
- **Purpose**: Tracks the process of generating content from standards
- **Key Fields**: standard_id, job_type (single/bundle), status
- **Usage**: Triggered by dashboard or n8n workflows to create products

### Bundles
Collections of 12 related products grouped together.
- **Purpose**: Package products for delivery to clients
- **Key Fields**: Will be implemented in future iterations
- **Usage**: Organizational unit for product delivery

### Upload Tasks
Tasks assigned to VA team for manual content processing.
- **Purpose**: Track manual work required for product finalization
- **Key Fields**: product_id, status
- **Usage**: Workflow management for human-in-the-loop processes

### File Artifacts
Physical files associated with products (JSON, ZIP, etc.).
- **Purpose**: Store references to generated files and their metadata
- **Key Fields**: product_id, file_type, file_path
- **Usage**: Track all files created during generation process

### Users (Future)
Basic user management for system access.
- **Purpose**: Authentication and authorization (planned for later phases)
- **Key Fields**: TBD - basic user info
- **Usage**: System access control (not implemented in MVP)