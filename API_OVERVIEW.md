# 🚀 RBB Engine Backend - API Overview

## 📋 Table of Contents
- [System Architecture](#system-architecture)
- [Data Flow Overview](#data-flow-overview)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [File Storage Structure](#file-storage-structure)

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │───▶│  FastAPI Backend │───▶│   PostgreSQL    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  File Storage   │
                       │   (/rbb-drive)  │
                       └─────────────────┘
```

## 🔄 Data Flow Overview

### 1. 📚 Standards Lookup & Selection Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  User searches  │───▶│ Standards API   │───▶│ Database Query  │
│  for standards  │    │ /v1/standards/  │    │ with filters    │
└─────────────────┘    │     lookup      │    └─────────────────┘
                       └─────────────────┘             │
                                │                      ▼
                                ▼              ┌─────────────────┐
                       ┌─────────────────┐    │ Return filtered │
                       │ Return matching │◀───│ standards list  │
                       │ standards (≤20) │    │ (code, grade,   │
                       └─────────────────┘    │ curriculum)     │
                                              └─────────────────┘
```

**Detailed Steps**:
1. **User Input**: User types in search box (e.g., "Math Grade 5")
2. **API Call**: Frontend calls `GET /api/v1/standards/lookup?code=Math&grade_level=5&curriculum_board=CBSE`
3. **Database Query**: Backend queries `standards` table with ILIKE pattern matching
4. **Filtering**: Applies curriculum_board, grade_level, locale filters
5. **Limit Results**: Returns max 20 results for performance
6. **Response**: JSON array of matching standards with id, code, description
7. **UI Update**: Frontend populates dropdown/autocomplete

**What It's Waiting For**: User selection from dropdown
**Next Step**: User selects standard → triggers product generation

---

### 2. 🎯 Product Generation Flow (Complete Lifecycle)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ User selects    │───▶│ Validate Input  │───▶│ Database        │
│ standard +      │    │ (standard_id,   │    │ Transaction     │
│ product type    │    │ grade, type)    │    │ BEGIN           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                      │
                                ▼                      ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ POST /api/      │    │ 1. Create       │
                       │ generate-       │    │ GenerationJob   │
                       │ product         │    │ (PENDING)       │
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ 2. Create       │
                                              │ Product (DRAFT) │
                                              │ linked to job   │
                                              └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ 3. Create       │
                                              │ Storage Dir     │
                                              │ /products/{id}/ │
                                              └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ 4. Generate     │
                                              │ Stub Files:     │
                                              │ - PDF           │
                                              │ - Thumbnail     │
                                              │ - JSON metadata │
                                              └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ 5. COMMIT       │
                                              │ Transaction     │
                                              │ Return IDs      │
                                              └─────────────────┘
```

**Detailed Steps**:
1. **Input Validation**: 
   - Checks standard_id exists in database
   - Validates grade_level (1-12)
   - Validates product_type enum
   - Validates locale and curriculum_board

2. **Database Transaction (Atomic)**:
   - **GenerationJob Creation**: 
     - Status: PENDING
     - Type: SINGLE_PRODUCT
     - Links to standard_id
     - Sets total_products = 1, completed_products = 0
   - **Product Creation**:
     - Status: DRAFT (waiting for AI generation)
     - Links to generation_job_id
     - Inherits locale, curriculum_board, grade_level

3. **File System Operations**:
   - Creates `/rbb-drive/products/{product_id}/` directory
   - Generates stub PDF with basic structure
   - Creates placeholder thumbnail (1x1 PNG)
   - Creates metadata.json with product info

4. **Response**: Returns job_id and product_id for tracking

**What It's Waiting For**: 
- **Currently**: Manual status updates (future: AI processing)
- **Future**: Background worker to process PENDING jobs

**Current State**: Product is in DRAFT, Job is PENDING
**Next Steps**: 
- Manual: Admin updates product status via PATCH API
- Future: AI worker picks up PENDING job, processes, updates status

---

### 3. 📊 Status Update Flow (Manual/Automated)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Status Update   │───▶│ Validate        │───▶│ Update Product  │
│ Request         │    │ Transition      │    │ Status          │
│ (DRAFT→GEN)     │    │ Rules           │    │ in Database     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                      │
                                ▼                      ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ PATCH /api/     │    │ Automatic Job   │
                       │ products/{id}/  │    │ Status Update   │
                       │ status          │    │ Calculation     │
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ Update Job      │
                                              │ Progress:       │
                                              │ completed_      │
                                              │ products++      │
                                              └─────────────────┘
```

**Detailed Steps**:
1. **Status Transition Validation**:
   - DRAFT → GENERATED (success) or FAILED (error)
   - GENERATED → FAILED (reprocessing needed)
   - FAILED → DRAFT (retry)

2. **Product Status Update**:
   - Updates product.status in database
   - Logs change with timestamp

3. **Automatic Job Status Calculation**:
   - Counts products by status for this job
   - Updates job.completed_products, job.failed_products
   - Updates job.status based on progress:
     - All products GENERATED → Job COMPLETED
     - Any product FAILED → Job FAILED
     - Still processing → Job RUNNING

**What It's Waiting For**: External trigger (manual admin or AI worker)
**Impact**: Affects dashboard statistics, job progress tracking

---

### 4. 📋 Upload Task Workflow (VA Team Process)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Product Ready   │───▶│ Create Upload   │───▶│ VA Assignment   │
│ (GENERATED)     │    │ Task (PENDING)  │    │ (Optional)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                      │
                                ▼                      ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ POST /api/v1/   │    │ Task appears    │
                       │ upload-tasks    │    │ in VA queue     │
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ VA picks up:    │
                                              │ PENDING →       │
                                              │ IN_PROGRESS     │
                                              └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ VA completes:   │
                                              │ IN_PROGRESS →   │
                                              │ COMPLETED       │
                                              └─────────────────┘
```

**Detailed Steps**:
1. **Task Creation Trigger**: 
   - Manual: Admin creates task for specific product
   - Future: Automatic when product status = GENERATED

2. **Task Assignment**:
   - Can be assigned to specific VA team member
   - Or left unassigned for queue pickup

3. **VA Workflow**:
   - VA sees task in their queue (GET /api/v1/upload-tasks?assigned_to=me)
   - VA starts work: PATCH status to IN_PROGRESS
   - VA completes work: PATCH status to COMPLETED

4. **Status Transitions**:
   - PENDING → IN_PROGRESS (VA starts)
   - IN_PROGRESS → COMPLETED (VA finishes)
   - IN_PROGRESS → PENDING (VA pauses/reassigns)

**What It's Waiting For**: VA team member action
**Tracking**: All status changes logged with timestamps

---

### 5. 📊 Dashboard Data Aggregation Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Dashboard       │───▶│ Database        │───▶│ Aggregate       │
│ Request         │    │ Queries         │    │ Calculations    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                      │
                                ▼                      ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ GET /api/       │    │ Count products  │
                       │ dashboard/stats │    │ by status       │
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ Count jobs by   │
                                              │ status          │
                                              └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ Count tasks by  │
                                              │ status          │
                                              └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ Return JSON     │
                                              │ with all stats │
                                              └─────────────────┘
```

**Detailed Steps**:
1. **Real-time Queries**: 
   - `SELECT status, COUNT(*) FROM products GROUP BY status`
   - `SELECT status, COUNT(*) FROM generation_jobs GROUP BY status`
   - `SELECT status, COUNT(*) FROM upload_tasks GROUP BY status`

2. **Calculations**:
   - Total counts for each entity type
   - Percentage breakdowns
   - Active vs completed ratios

3. **Response Format**: Structured JSON with nested status breakdowns

**What It's Waiting For**: Nothing - real-time data
**Performance**: Optimized with database indexes on status columns

---

### 6. 🔄 Complete System Integration Flow

```
Frontend UI ──────────────────────────────────────────────────────┐
    │                                                            │
    ▼                                                            ▼
┌─────────────────┐                                    ┌─────────────────┐
│ 1. Standards    │                                    │ 6. Dashboard    │
│    Lookup       │                                    │    Monitoring   │
└─────────────────┘                                    └─────────────────┘
    │                                                            ▲
    ▼                                                            │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 2. Product      │───▶│ 3. File System  │───▶│ 5. Status       │
│    Generation   │    │    Operations   │    │    Updates      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
    │                           │                       ▲
    ▼                           ▼                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Database        │    │ Storage         │    │ 4. VA Upload    │
│ (PostgreSQL)    │    │ (/rbb-drive)    │    │    Tasks        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Integration Points**:
1. **Standards → Generation**: Selected standard triggers product creation
2. **Generation → Files**: Product creation triggers file system setup
3. **Files → Tasks**: Generated files trigger VA workflow
4. **Tasks → Status**: VA completion updates product status
5. **Status → Dashboard**: All changes reflect in real-time dashboard
6. **Dashboard → Monitoring**: Provides visibility into entire system

**Current Limitations**:
- **No AI Processing**: Products stay in DRAFT until manual status update
- **No Background Workers**: All processing is synchronous
- **No Automated Workflows**: VA tasks created manually

**Future Enhancements**:
- Background job processing for AI generation
- Automated upload task creation
- Real-time notifications for status changes
- File processing pipelines

---

## 🛠️ API Endpoints

### 🏥 Health & System

#### `GET /api/health`
**Purpose**: System health check with database connectivity  
**Data Flow**: 
- Tests database connection with `SELECT 1`
- Returns service status, version, environment info
- Logs connection status for monitoring

**Response**:
```json
{
  "status": "ok|degraded",
  "service": "rbb-engine-backend", 
  "version": "1.0.0",
  "environment": "development",
  "database": "connected|disconnected"
}
```

---

### 🎯 Core Generation

#### `POST /api/generate-product`
**Purpose**: Main product generation endpoint - creates jobs and products atomically  
**Data Flow**:
1. Validates input (standard_id, grade_level, product_type)
2. Creates GenerationJob with PENDING status
3. Creates Product linked to job with DRAFT status
4. Creates storage directory structure
5. Generates stub PDF and thumbnail files
6. Returns job and product IDs

**Request**:
```json
{
  "standard_id": 1,
  "product_type": "WORKSHEET",
  "locale": "IN",
  "curriculum_board": "CBSE", 
  "grade_level": 5
}
```

**Response**:
```json
{
  "success": true,
  "message": "Product generation job created successfully",
  "data": {
    "job_id": 123,
    "product_ids": [456],
    "message": "Product generation job created successfully for WORKSHEET"
  }
}
```

---

### 📦 Products Management

#### `GET /api/products`
**Purpose**: List products with filtering and pagination  
**Data Flow**:
- Queries products table with optional filters
- Orders by created_at DESC (newest first)
- Applies pagination
- Returns products with metadata

**Query Parameters**:
- `status`: ProductStatus (DRAFT, GENERATED, FAILED)
- `product_type`: ProductType (WORKSHEET, PASSAGE, QUIZ, ASSESSMENT)
- `generation_job_id`: Filter by job
- `standard_id`: Filter by standard
- `curriculum_board`: CBSE, COMMON_CORE
- `grade_level`: 1-12
- `locale`: IN, US
- `limit`: 1-100 (default: 50)
- `offset`: 0+ (default: 0)

#### `GET /api/products/{product_id}`
**Purpose**: Get specific product details  
**Data Flow**:
- Fetches product by ID from database
- Returns full product information
- 404 if not found

#### `PATCH /api/products/{product_id}/status`
**Purpose**: Update product status with validation  
**Data Flow**:
1. Validates product exists
2. Checks status transition is valid:
   - DRAFT → GENERATED, FAILED
   - GENERATED → FAILED  
   - FAILED → DRAFT
3. Updates product status
4. Updates linked generation job status automatically
5. Logs status change

---

### 📊 Dashboard & Analytics

#### `GET /api/dashboard/stats`
**Purpose**: Detailed dashboard statistics with breakdowns  
**Data Flow**:
- Aggregates product counts by status
- Aggregates generation job counts by status  
- Aggregates upload task counts by status
- Returns comprehensive statistics

**Response**:
```json
{
  "success": true,
  "data": {
    "total_products": 150,
    "products_by_status": {
      "DRAFT": 45,
      "GENERATED": 90, 
      "FAILED": 15
    },
    "total_generation_jobs": 75,
    "jobs_by_status": {
      "PENDING": 10,
      "RUNNING": 5,
      "COMPLETED": 55,
      "FAILED": 5
    },
    "total_upload_tasks": 30,
    "tasks_by_status": {
      "PENDING": 10,
      "IN_PROGRESS": 5,
      "COMPLETED": 15
    }
  }
}
```

#### `GET /api/dashboard/summary`
**Purpose**: Lightweight dashboard summary for quick checks  
**Data Flow**:
- Counts total products
- Counts active jobs (PENDING + RUNNING)
- Counts pending upload tasks
- Returns minimal summary

---

### 📚 Standards Management

#### `GET /api/v1/standards`
**Purpose**: List educational standards with filtering  
**Data Flow**:
- Queries standards table
- Applies curriculum, grade, locale filters
- Returns paginated results

#### `GET /api/v1/standards/{standard_id}`
**Purpose**: Get specific standard details  
**Data Flow**:
- Fetches standard by ID
- Returns standard information
- 404 if not found

#### `GET /api/v1/standards/lookup`
**Purpose**: Quick standards search for UI dropdowns  
**Data Flow**:
- Searches standards by code (ILIKE pattern)
- Applies filters for curriculum and grade
- Returns limited results (max 20)
- Optimized for autocomplete/typeahead

**Query Parameters**:
- `code`: Search pattern for standard code
- `grade_level`: 1-12
- `curriculum_board`: CBSE, COMMON_CORE
- `limit`: 1-50 (default: 20)

---

### 🔄 Generation Jobs

#### `GET /api/v1/generation-jobs`
**Purpose**: List generation jobs with filtering  
**Data Flow**:
- Queries generation_jobs table
- Filters by status, job_type, dates
- Returns job information with progress

#### `GET /api/v1/generation-jobs/{job_id}`
**Purpose**: Get specific job details with linked products  
**Data Flow**:
- Fetches job by ID
- Includes linked products
- Shows progress statistics

---

### 📋 Upload Tasks (VA Workflow)

#### `POST /api/v1/upload-tasks`
**Purpose**: Create upload task for VA team processing  
**Data Flow**:
1. Validates product exists
2. Creates upload task with PENDING status
3. Optional assignment to VA team member
4. Links to product for context

**Request**:
```json
{
  "product_id": 456,
  "assigned_to": "va_member@company.com",
  "status": "PENDING"
}
```

#### `GET /api/v1/upload-tasks`
**Purpose**: List upload tasks with filtering  
**Data Flow**:
- Queries upload_tasks table
- Joins with products for context
- Filters by status, assignee, product
- Orders by created_at DESC

**Query Parameters**:
- `status`: PENDING, IN_PROGRESS, COMPLETED
- `assigned_to`: VA team member email
- `product_id`: Filter by specific product

#### `GET /api/v1/upload-tasks/{task_id}`
**Purpose**: Get specific upload task details  
**Data Flow**:
- Fetches task by ID
- Includes linked product information
- 404 if not found

#### `PATCH /api/v1/upload-tasks/{task_id}`
**Purpose**: Update upload task status with validation  
**Data Flow**:
1. Validates task exists
2. Checks status transition is valid:
   - PENDING → IN_PROGRESS
   - IN_PROGRESS → COMPLETED, PENDING
   - COMPLETED → (terminal state)
3. Updates task status and assignment
4. Logs status change

---

### 🔗 Webhooks

#### `POST /api/v1/webhooks/generation-request`
**Purpose**: External webhook for n8n workflow integration  
**Data Flow**:
- Receives generation requests from external systems
- Validates webhook payload
- Triggers product generation flow
- Returns acknowledgment

---

## 🗄️ Database Schema

### Core Tables

#### `standards`
- Educational standards (CBSE, Common Core)
- Fields: id, code, description, curriculum_board, grade_level, locale

#### `generation_jobs` 
- Product generation jobs
- Fields: id, standard_id, job_type, status, total_products, completed_products, failed_products
- Status: PENDING → RUNNING → COMPLETED/FAILED

#### `products`
- Generated educational content
- Fields: id, standard_id, generation_job_id, product_type, status, locale, curriculum_board, grade_level
- Status: DRAFT → GENERATED → FAILED

#### `upload_tasks`
- VA team workflow tasks
- Fields: id, product_id, status, assigned_to
- Status: PENDING → IN_PROGRESS → COMPLETED

#### `file_artifacts`
- Generated files metadata
- Fields: id, product_id, file_type, file_path, file_size

#### `bundles`
- Product bundles for grouped delivery
- Fields: id, name, description, locale, curriculum_board, grade_level

#### `error_logs`
- System error logging
- Fields: id, endpoint, method, error_type, error_message, stack_trace, created_at

---

## 📁 File Storage Structure

```
rbb-drive/
├── products/
│   └── {product_id}/
│       ├── raw.json          # Raw generation data
│       ├── final.json        # Processed content
│       ├── metadata.json     # Product metadata
│       ├── {type}_stub.pdf   # Generated PDF
│       ├── {type}_thumbnail.png # Thumbnail image
│       └── bundle.zip        # Packaged content
└── temp/                     # Temporary processing files
```

---

## 🔄 Status Workflows

### Product Lifecycle
```
DRAFT ──────────────▶ GENERATED ──────────────▶ FAILED
  ▲                                               │
  └───────────────────────────────────────────────┘
```

### Generation Job Lifecycle  
```
PENDING ──────────────▶ RUNNING ──────────────▶ COMPLETED
                                  │
                                  ▼
                                FAILED
```

### Upload Task Lifecycle
```
PENDING ──────────────▶ IN_PROGRESS ──────────────▶ COMPLETED
  ▲                         │
  └─────────────────────────┘
```

---

## 🛡️ Error Handling

- **Validation Errors**: 400 Bad Request with detailed field errors
- **Not Found**: 404 with specific entity not found message  
- **Status Transition Errors**: 400 with invalid transition details
- **Database Errors**: 500 Internal Server Error with logged details
- **Authentication**: 401 Unauthorized (future implementation)

---

## 📝 Logging

All endpoints log:
- Request details (method, endpoint, parameters)
- Processing results (success/failure)
- Performance metrics (response time)
- Error details (stack traces for debugging)

Log levels: INFO (operations), ERROR (failures), DEBUG (detailed tracing)