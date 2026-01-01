# Generation Job Lifecycle Documentation

## Overview

Generation jobs are first-class entities that track the creation and progress of educational content products. This document outlines the job lifecycle, status meanings, and API usage patterns.

## Job Status Meanings

### PENDING
- **Definition**: Job has been created but no products have started processing
- **Transitions**: Can move to RUNNING when first product begins processing
- **Product State**: All products are in DRAFT status

### RUNNING  
- **Definition**: At least one product is being processed or has completed
- **Transitions**: Can move to COMPLETED when all products are done
- **Product State**: Mix of DRAFT, GENERATED, and/or FAILED products

### COMPLETED
- **Definition**: All products have finished processing (generated or failed)
- **Transitions**: Terminal state (no further transitions)
- **Product State**: All products are either GENERATED or FAILED

### FAILED
- **Definition**: Reserved for future use (job-level failures)
- **Transitions**: Terminal state (no further transitions)  
- **Product State**: Varies

## Job Progress Calculation

### Automatic Updates
Job progress is updated automatically when:
- Product status changes via `PATCH /api/products/{id}/status`
- Job details are retrieved via `GET /api/generation-jobs/{id}`
- Job summary is retrieved via `GET /api/generation-jobs/{id}/summary`

### Completion Logic
A job is marked as COMPLETED when:
- `completed_products + failed_products == total_products`
- At least one product exists (`total_products > 0`)

### Progress Tracking
- `total_products`: Total number of products in the job
- `completed_products`: Products with status GENERATED
- `failed_products`: Products with status FAILED
- Remaining products are in DRAFT status

## API Usage Patterns

### Creating Jobs and Products

**Endpoint**: `POST /api/generate-product`

Creates a generation job with associated product records:
- Job starts in PENDING status
- Products start in DRAFT status
- Returns job_id and product_ids for tracking

### Monitoring Job Progress

**Endpoint**: `GET /api/generation-jobs/{id}/summary`

Lightweight endpoint for frontend status panels:
- Returns job_id, status, product counts, created_at
- Automatically updates progress before returning
- Optimized for frequent polling

**Endpoint**: `GET /api/generation-jobs/{id}`

Complete job details including:
- All job fields (locale, curriculum_board, etc.)
- Current status and product counts
- Timestamps (created_at, updated_at)

**Endpoint**: `GET /api/generation-jobs`

Lists jobs with filtering by:
- status
- grade_level  
- curriculum_board
- locale
- job_type

### Product Management

**Endpoint**: `GET /api/products?generation_job_id={id}`

Lists products for a specific job:
- Supports additional filtering by status
- Includes pagination
- Indexed for efficient queries

**Endpoint**: `PATCH /api/products/{id}/status`

Updates product status and triggers job progress update:
- Validates status transitions
- Updates job progress counters
- Logs all changes

## Database Schema

### GenerationJob Model Fields

```python
id: int                    # Primary key
standard_id: int          # Reference to Standard
locale: Locale            # IN, US
curriculum_board: Board   # CBSE, COMMON_CORE  
grade_level: int          # 1-12
job_type: JobType         # SINGLE_PRODUCT, FULL_BUNDLE
status: JobStatus         # PENDING, RUNNING, COMPLETED, FAILED
total_products: int       # Total products to generate (default: 0)
completed_products: int   # Successfully completed count (default: 0)
failed_products: int      # Failed products count (default: 0)
created_at: datetime      # Job creation time
updated_at: datetime      # Last status change time
```

### Indexes

- Primary: `id`
- Status tracking: `(status, created_at)`
- Filtering: `locale`, `curriculum_board`, `grade_level`
- Relationships: `standard_id`, `(standard_id, job_type)`

## Service Functions

### Job Progress Updates

```python
# Automatic progress update (called on product status change)
update_job_progress(db, job_id, product_id, new_status)

# Manual status updates (for async workflows)
mark_job_running(db, job_id)    # Set to RUNNING
mark_job_completed(db, job_id)  # Set to COMPLETED  
mark_job_failed(db, job_id)     # Set to FAILED

# Full status recalculation
update_job_status(db, job_id)   # Calculate from product states
```

### Logging

All status changes are logged with:
- job_id and product_id
- old_status → new_status
- product counts and progress
- action name

## Error Handling

### Validation
- Invalid IDs (≤ 0) return 400 Bad Request
- Non-existent resources return 404 Not Found
- Invalid status transitions return 400 Bad Request

### Status Transitions
**Valid Product Status Transitions:**
- DRAFT → GENERATED, FAILED
- GENERATED → FAILED
- FAILED → DRAFT

## Frontend Integration

### Polling Pattern

Frontend should use the summary endpoint for efficient polling:

```javascript
// Poll job progress (lightweight)
const pollJobSummary = async (jobId) => {
  const response = await fetch(`/api/generation-jobs/${jobId}/summary`);
  const summary = await response.json();
  
  // Update UI with progress
  updateProgress(summary.completed_products, summary.total_products);
  
  // Continue polling if not completed
  if (summary.status === 'RUNNING' || summary.status === 'PENDING') {
    setTimeout(() => pollJobSummary(jobId), 2000);
  }
};
```

### Status Display

- **PENDING**: "Queued for processing..."
- **RUNNING**: "Processing {completed_products} of {total_products} products..."  
- **COMPLETED**: "All products processed ({completed_products} generated, {failed_products} failed)"
- **FAILED**: "Job failed"

### Product Listing

```javascript
// Get products for a specific job
const getJobProducts = async (jobId, status = null) => {
  const params = new URLSearchParams({ generation_job_id: jobId });
  if (status) params.append('status', status);
  
  const response = await fetch(`/api/products?${params}`);
  return response.json();
};
```

## Future Considerations

This foundation prepares for:
- Async AI model execution
- n8n workflow orchestration  
- Background job processing
- Queue management
- Retry mechanisms
- Partial failure handling

The job lifecycle is designed to be workflow-agnostic and can accommodate various execution patterns without API changes.