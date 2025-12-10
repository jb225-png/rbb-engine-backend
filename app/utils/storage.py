import os
from pathlib import Path
from app.core.config import settings

class StorageManager:
    """
    Manages file storage for products and generated assets.
    Ensures directory structure exists and provides path utilities.
    """
    
    def __init__(self):
        self.base_path = Path(settings.storage_path)
    
    def ensure_directories(self) -> None:
        """Create base storage directories if they don't exist"""
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def get_product_path(self, product_id: int) -> Path:
        """Get storage path for a specific product"""
        product_path = self.base_path / f"product_{product_id}"
        product_path.mkdir(parents=True, exist_ok=True)
        return product_path

storage_manager = StorageManager()
