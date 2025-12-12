# RBB Engine - Enhanced API Endpoints (Day 4)

## Response Format

All endpoints return standardized responses:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data here
  }
}
```

## Standards Management

### `POST /api/v1/standards`
- **Description**: Create new educational standard
- **Request**: 
```json
{
  "locale": "IN",
  "curriculum_board": "CBSE",
  "grade_level": 6,
  "grade_range": null,
  "code": "CBSE.MATH.6.1",
  "description": "Knowing Our Numbers - Place value and comparison"
}
```
- **Response**: 
```json
{
  "success": true,
  "message": "Standard created successfully",
  "data": {
    "id": 1,
    "locale": "IN",
    "curriculum_board": "CBSE",
    "grade_level": 6,
    "code": "CBSE.MATH.6.1",
    "description": "Knowing Our Numbers - Place value and comparison",
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

### `GET /api/v1/standards`
- **Description**: List all available standards with filtering and pagination
- **Query Params**: 
  - `curriculum_board` (CBSE, COMMON_CORE)
  - `grade_level` (1-12)
  - `locale` (IN, US)
  - `limit` (1-100, default: 50)
  - `offset` (default: 0)
- **Response**: 
```json
{
  "success": true,
  "message": "Standards retrieved successfully",
  "data": {
    "standards": [...],
    "pagination": {
      "total": 150,
      "limit": 50,
      "offset": 0,
      "has_next": true
    }
  }
}
```

### `GET /api/v1/standards/{id}`
- **Description**: Get specific standard details
- **Response**: 
```json
{
  "success": true,
  "message": "Standard retrieved successfully",
  "data": {
    "id": 1,
    "locale": "IN",
    "curriculum_board": "CBSE",
    "grade_level": 6,
    "code": "CBSE.MATH.6.1",
    "description": "Knowing Our Numbers - Place value and comparison",
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

## Generation Jobs

### `POST /api/v1/generation-jobs`
- **Description**: Create new generation job
- **Request**: 
```json
{
  "standard_id": 1,
  "locale": "IN",
  "curriculum_board": "CBSE",
  "grade_level": 6,
  "job_type": "SINGLE_PRODUCT"
}
```
- **Response**: 
```json
{
  "success": true,
  "message": "Generation job created successfully",
  "data": {
    "id": 1,
    "standard_id": 1,
    "locale": "IN",
    "curriculum_board": "CBSE",
    "grade_level": 6,
    "job_type": "SINGLE_PRODUCT",
    "status": "PENDING",
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

### `GET /api/v1/generation-jobs`
- **Description**: List all generation jobs with filtering and pagination
- **Query Params**: 
  - `status` (PENDING, RUNNING, COMPLETED, FAILED)
  - `job_type` (SINGLE_PRODUCT, FULL_BUNDLE)
  - `curriculum_board` (CBSE, COMMON_CORE)
  - `grade_level` (1-12)
  - `locale` (IN, US)
  - `limit` (1-100, default: 50)
  - `offset` (default: 0)
- **Response**: 
```json
{
  "success": true,
  "message": "Generation jobs retrieved successfully",
  "data": {
    "jobs": [...],
    "pagination": {
      "total": 25,
      "limit": 50,
      "offset": 0,
      "has_next": false
    }
  }
}
```

### `GET /api/v1/generation-jobs/{id}`
- **Description**: Get specific job details and progress
- **Response**: 
```json
{
  "success": true,
  "message": "Generation job retrieved successfully",
  "data": {
    "id": 1,
    "standard_id": 1,
    "locale": "IN",
    "curriculum_board": "CBSE",
    "grade_level": 6,
    "job_type": "SINGLE_PRODUCT",
    "status": "PENDING",
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

## Locale-Specific Examples

### India (CBSE) Example Requests
```json
// Create CBSE Standard
{
  "locale": "IN",
  "curriculum_board": "CBSE",
  "grade_level": 8,
  "code": "CBSE.MATH.8.1",
  "description": "Rational Numbers - Properties and operations"
}

// Create Generation Job for CBSE
{
  "standard_id": 1,
  "locale": "IN",
  "curriculum_board": "CBSE",
  "grade_level": 8,
  "job_type": "SINGLE_PRODUCT"
}
```

### US (Common Core) Example Requests
```json
// Create Common Core Standard
{
  "locale": "US",
  "curriculum_board": "COMMON_CORE",
  "grade_level": 3,
  "code": "CCSS.MATH.3.OA.1",
  "description": "Interpret products of whole numbers"
}
```

## Validation Rules
- **Locale-Curriculum Consistency**: India (IN) must use CBSE, US must use Common Core
- **Grade Level Range**: 1-12 for all locales
- **Required Fields**: All locale, curriculum_board, and grade_level fields are required
- **Default Values**: If not specified, defaults to IN locale and CBSE curriculum