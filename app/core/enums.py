from enum import Enum

class Locale(str, Enum):
    """Supported locales"""
    IN = "IN"  # India (default)
    US = "US"  # United States

class CurriculumBoard(str, Enum):
    """Educational curriculum boards"""
    CBSE = "CBSE"  # Central Board of Secondary Education (India)
    COMMON_CORE = "COMMON_CORE"  # Common Core State Standards (US)

class Currency(str, Enum):
    """Supported currencies"""
    INR = "INR"  # Indian Rupee (default)
    USD = "USD"  # US Dollar

class JobStatus(str, Enum):
    """Generation job statuses"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ProductType(str, Enum):
    """Product types"""
    WORKSHEET = "WORKSHEET"
    PASSAGE = "PASSAGE"
    QUIZ = "QUIZ"
    ASSESSMENT = "ASSESSMENT"

class ProductStatus(str, Enum):
    """Product statuses"""
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    REVIEWED = "REVIEWED"
    PUBLISHED = "PUBLISHED"

class JobType(str, Enum):
    """Generation job types"""
    SINGLE_PRODUCT = "SINGLE_PRODUCT"
    FULL_BUNDLE = "FULL_BUNDLE"

class FileType(str, Enum):
    """File artifact types"""
    RAW_JSON = "RAW_JSON"
    FINAL_JSON = "FINAL_JSON"
    METADATA_JSON = "METADATA_JSON"
    PDF = "PDF"
    ZIP = "ZIP"
    THUMBNAIL = "THUMBNAIL"