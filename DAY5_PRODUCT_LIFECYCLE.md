# Day 5 - Product Lifecycle Foundations

## What's New in Day 5

✅ **Product Entity** - First-class API resource with complete CRUD operations  
✅ **Entity Relationships** - Standards → Generation Jobs → Products  
✅ **Product Status Handling** - DRAFT, GENERATED, FAILED lifecycle  
✅ **Enhanced Filtering** - Products can be filtered by job, standard, type, status  
✅ **Clean Data Model** - Proper foreign key relationships and indexes  

## Core Entity Relationships

```
Standards (Educational Requirements)
    ↓ (referenced by)
Generation Jobs (Content Creation Tasks)
    ↓ (can create multiple)
Products (Generated Content Items)
```

### Data Flow
1. **Standards** define what content should be generated
2. **Generation Jobs** track the process of creating content from standards
3. **Products** are the actual generated content items (worksheets, passages, etc.)

## New Product Model

### Core Fields
- `id` - Primary key
- `standard_id` - References the educational standard (required)
- `generation_job_id` - References the job that created this product (optional)
- `product_type` - Type of content (WORKSHEET, PASSAGE, QUIZ, ASSESSMENT)
- `status` - Current state (DRAFT, GENERATED, FAILED)
- `locale` - Geographic region (IN, US)
- `curriculum_board` - Educational system (CBSE, COMMON_CORE)
- `grade_level` - Target grade (1-12)
- `created_at` - Timestamp

### Product Status Lifecycle
- **DRAFT** - Initial state when product is created
- **GENERATED** - Product has been successfully generated
- **FAILED** - Product generation encountered an error

## New API Endpoints

### Product Management
- **POST /api/v1/products** - Create new product
- **GET /api/v1/products** - List products with comprehensive filtering
- **GET /api/v1/products/{id}** - Get specific product details

### Enhanced Filtering Options
Products can be filtered by:
- `status` (DRAFT, GENERATED, FAILED)
- `product_type` (WORKSHEET, PASSAGE, QUIZ, ASSESSMENT)
- `generation_job_id` - Find all products from a specific job
- `standard_id` - Find all products for a specific standard
- `curriculum_board` (CBSE, COMMON_CORE)
- `grade_level` (1-12)
- `locale` (IN, US)

## Repository Pattern Enhancement

### New Product Repository
- `app/repositories/products.py` - Clean database operations
- Methods: `create`, `get_by_id`, `get_all`, `list_by_job`
- Comprehensive filtering support
- Consistent with existing standards and jobs repositories

## Database Changes

### Migration 002
- Added `generation_job_id` column to products table
- Updated ProductStatus enum (removed REVIEWED, PUBLISHED; kept DRAFT, GENERATED, FAILED)
- Added new indexes for performance:
  - `ix_products_generation_job_id`
  - `ix_products_status_type`
- Maintained backward compatibility

## API Examples

### Create Product
```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{
    "standard_id": 1,
    "generation_job_id": 2,
    "product_type": "WORKSHEET",
    "locale": "IN",
    "curriculum_board": "CBSE",
    "grade_level": 6
  }'
```

### List Products by Generation Job
```bash
curl "http://localhost:8000/api/v1/products?generation_job_id=2"
```

### List Failed Products for Review
```bash
curl "http://localhost:8000/api/v1/products?status=FAILED&limit=20"
```

### List CBSE Grade 7 Worksheets
```bash
curl "http://localhost:8000/api/v1/products?curriculum_board=CBSE&grade_level=7&product_type=WORKSHEET"
```

## Benefits

1. **Clear Data Relationships** - Standards → Jobs → Products flow is explicit
2. **Flexible Product Creation** - Products can be created independently or via jobs
3. **Comprehensive Filtering** - Find products by any relevant criteria
4. **Status Tracking** - Monitor product generation success/failure
5. **Scalable Design** - Ready for batch operations and bulk generation

## File Structure Changes

```
app/
├── core/
│   └── enums.py              # UPDATED: ProductStatus enum simplified
├── models/
│   └── product.py            # UPDATED: Added generation_job_id, reordered fields
├── schemas/
│   └── product.py            # UPDATED: Full validation and enum support
├── repositories/
│   └── products.py           # NEW: Product database operations
├── api/v1/routes/
│   └── products.py           # UPDATED: Complete CRUD with filtering
└── ...

migrations/versions/
└── 002_update_products_add_generation_job_link.py  # NEW: Migration

docs/
└── product_endpoints.md      # NEW: Product API documentation
```

## Next Steps (Day 6+)

- Add file artifact management for products
- Implement product bundling logic
- Add QC and review workflows
- Connect to AI generation services
- Add bulk operations for efficiency
- Implement product versioning

## Testing the New Features

### 1. Create a Standard (if needed)
```bash
curl -X POST "http://localhost:8000/api/v1/standards" \
  -H "Content-Type: application/json" \
  -d '{"locale": "IN", "curriculum_board": "CBSE", "grade_level": 6, "code": "CBSE.MATH.6.TEST", "description": "Test standard"}'
```

### 2. Create a Generation Job (if needed)
```bash
curl -X POST "http://localhost:8000/api/v1/generation-jobs" \
  -H "Content-Type: application/json" \
  -d '{"standard_id": 1, "locale": "IN", "curriculum_board": "CBSE", "grade_level": 6, "job_type": "SINGLE_PRODUCT"}'
```

### 3. Create Products
```bash
# Product linked to job
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{"standard_id": 1, "generation_job_id": 1, "product_type": "WORKSHEET", "locale": "IN", "curriculum_board": "CBSE", "grade_level": 6}'

# Standalone product
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{"standard_id": 1, "product_type": "QUIZ", "locale": "IN", "curriculum_board": "CBSE", "grade_level": 6}'
```

### 4. List and Filter Products
```bash
# All products
curl "http://localhost:8000/api/v1/products"

# Products by job
curl "http://localhost:8000/api/v1/products?generation_job_id=1"

# Products by type and status
curl "http://localhost:8000/api/v1/products?product_type=WORKSHEET&status=DRAFT"
```

The backend now clearly represents the Standards → Generation Jobs → Products relationship with clean APIs and stable data flow, ready for frontend integration and future enhancements.