# RBB Engine - MVP API Endpoints

## Standards Management

### `GET /api/v1/standards`
- **Description**: List all available standards
- **Response**: `[{id, code, description, created_at}]`

### `GET /api/v1/standards/{id}`
- **Description**: Get specific standard details
- **Response**: `{id, code, description, created_at}`

## Product Management

### `GET /api/v1/products`
- **Description**: List all products with filtering
- **Query Params**: `status`, `type`, `standard_id`
- **Response**: `[{id, standard_id, type, status, created_at}]`

### `GET /api/v1/products/{id}`
- **Description**: Get specific product details
- **Response**: `{id, standard_id, type, status, created_at}`

## Generation Jobs

### `POST /api/v1/generation-jobs`
- **Description**: Create new generation job
- **Request**: `{standard_id, job_type}`
- **Response**: `{id, standard_id, job_type, status, created_at}`

### `GET /api/v1/generation-jobs`
- **Description**: List all generation jobs
- **Query Params**: `status`, `job_type`
- **Response**: `[{id, standard_id, job_type, status, created_at}]`

### `GET /api/v1/generation-jobs/{id}`
- **Description**: Get specific job details and progress
- **Response**: `{id, standard_id, job_type, status, created_at}`

## Dashboard Endpoints

### `GET /api/v1/dashboard/stats`
- **Description**: Get dashboard statistics
- **Response**: `{total_products, active_jobs, pending_tasks}`

### `POST /api/v1/dashboard/quick-generate`
- **Description**: Quick generation trigger from dashboard
- **Request**: `{standard_id, job_type}`
- **Response**: `{job_id, status, message}`

## Upload Tasks

### `GET /api/v1/upload-tasks`
- **Description**: List upload tasks for VA team
- **Query Params**: `status`
- **Response**: `[{id, product_id, status, created_at}]`

### `PUT /api/v1/upload-tasks/{id}`
- **Description**: Update upload task status
- **Request**: `{status}`
- **Response**: `{id, product_id, status, created_at}`