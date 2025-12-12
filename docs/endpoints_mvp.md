# RBB Engine - MVP API Endpoints (India-First)

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
- **Response**: `{id, locale, curriculum_board, grade_level, code, description, created_at}`

### `GET /api/v1/standards`
- **Description**: List all available standards
- **Query Params**: `locale`, `curriculum_board`, `grade_level`
- **Response**: `[{id, locale, curriculum_board, grade_level, code, description, created_at}]`

### `GET /api/v1/standards/{id}`
- **Description**: Get specific standard details
- **Response**: `{id, locale, curriculum_board, grade_level, code, description, created_at}`

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
- **Response**: `{id, standard_id, locale, curriculum_board, grade_level, job_type, status, created_at}`

### `GET /api/v1/generation-jobs`
- **Description**: List all generation jobs
- **Query Params**: `status`, `job_type`, `locale`, `curriculum_board`, `grade_level`
- **Response**: `[{id, standard_id, locale, curriculum_board, grade_level, job_type, status, created_at}]`

### `GET /api/v1/generation-jobs/{id}`
- **Description**: Get specific job details and progress
- **Response**: `{id, standard_id, locale, curriculum_board, grade_level, job_type, status, created_at}`

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