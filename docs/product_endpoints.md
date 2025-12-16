# Product Management API Endpoints

## Products

### `POST /api/v1/products`
- **Description**: Create new product
- **Request**: 
```json
{
  "standard_id": 1,
  "generation_job_id": 2,
  "product_type": "WORKSHEET",
  "status": "DRAFT",
  "locale": "IN",
  "curriculum_board": "CBSE",
  "grade_level": 6
}
```
- **Response**: 
```json
{
  "success": true,
  "message": "Product created successfully",
  "data": {
    "id": 1,
    "standard_id": 1,
    "generation_job_id": 2,
    "product_type": "WORKSHEET",
    "status": "DRAFT",
    "locale": "IN",
    "curriculum_board": "CBSE",
    "grade_level": 6,
    "created_at": "2024-01-16T10:00:00Z"
  }
}
```

### `GET /api/v1/products`
- **Description**: List all products with filtering and pagination
- **Query Params**: 
  - `status` (DRAFT, GENERATED, FAILED)
  - `product_type` (WORKSHEET, PASSAGE, QUIZ, ASSESSMENT)
  - `generation_job_id` (integer)
  - `standard_id` (integer)
  - `curriculum_board` (CBSE, COMMON_CORE)
  - `grade_level` (1-12)
  - `locale` (IN, US)
  - `limit` (1-100, default: 50)
  - `offset` (default: 0)
- **Response**: 
```json
{
  "success": true,
  "message": "Products retrieved successfully",
  "data": {
    "products": [...],
    "pagination": {
      "total": 25,
      "limit": 50,
      "offset": 0,
      "has_next": false
    }
  }
}
```

### `GET /api/v1/products/{id}`
- **Description**: Get specific product details
- **Response**: 
```json
{
  "success": true,
  "message": "Product retrieved successfully",
  "data": {
    "id": 1,
    "standard_id": 1,
    "generation_job_id": 2,
    "product_type": "WORKSHEET",
    "status": "DRAFT",
    "locale": "IN",
    "curriculum_board": "CBSE",
    "grade_level": 6,
    "created_at": "2024-01-16T10:00:00Z"
  }
}
```

## Product Lifecycle

### Status Flow
1. **DRAFT** - Initial state when product is created
2. **GENERATED** - Product has been successfully generated
3. **FAILED** - Product generation failed

### Relationships
- **Standard** (required) - The educational standard this product fulfills
- **Generation Job** (optional) - The job that created this product (if any)

## Example Usage

### Create Product for Specific Standard
```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{
    "standard_id": 1,
    "product_type": "WORKSHEET",
    "locale": "IN",
    "curriculum_board": "CBSE",
    "grade_level": 7
  }'
```

### List Products by Generation Job
```bash
curl "http://localhost:8000/api/v1/products?generation_job_id=2&status=GENERATED"
```

### List CBSE Grade 6 Worksheets
```bash
curl "http://localhost:8000/api/v1/products?curriculum_board=CBSE&grade_level=6&product_type=WORKSHEET"
```