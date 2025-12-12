from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.standard import Standard
from app.schemas.standard import StandardRead, StandardCreate

router = APIRouter()

@router.get("/", response_model=List[StandardRead])
async def list_standards(db: Session = Depends(get_db)):
    """List all available standards"""
    standards = db.query(Standard).all()
    return standards

@router.get("/{standard_id}", response_model=StandardRead)
async def get_standard(standard_id: int, db: Session = Depends(get_db)):
    """Get specific standard details"""
    standard = db.query(Standard).filter(Standard.id == standard_id).first()
    if not standard:
        raise HTTPException(status_code=404, detail="Standard not found")
    return standard

@router.post("/", response_model=StandardRead)
async def create_standard(standard: StandardCreate, db: Session = Depends(get_db)):
    """Create new standard"""
    db_standard = Standard(**standard.model_dump())
    db.add(db_standard)
    db.commit()
    db.refresh(db_standard)
    return db_standard