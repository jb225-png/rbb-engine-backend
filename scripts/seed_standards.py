#!/usr/bin/env python3
"""
Seed script for CBSE standards (India-first defaults)
Run with: python scripts/seed_standards.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.standard import Standard
from app.core.enums import Locale, CurriculumBoard

def seed_cbse_standards():
    """Seed CBSE standards for grades 6-10"""
    db = SessionLocal()
    
    try:
        # Check if standards already exist
        existing = db.query(Standard).first()
        if existing:
            print("Standards already exist. Skipping seed.")
            return
        
        cbse_standards = [
            # Grade 6 Mathematics
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 6,
                "code": "CBSE.MATH.6.1",
                "description": "Knowing Our Numbers - Place value and comparison"
            },
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 6,
                "code": "CBSE.MATH.6.2",
                "description": "Whole Numbers - Operations and properties"
            },
            
            # Grade 7 Mathematics
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 7,
                "code": "CBSE.MATH.7.1",
                "description": "Integers - Operations with positive and negative numbers"
            },
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 7,
                "code": "CBSE.MATH.7.2",
                "description": "Fractions and Decimals - Operations and applications"
            },
            
            # Grade 8 Mathematics
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 8,
                "code": "CBSE.MATH.8.1",
                "description": "Rational Numbers - Properties and operations"
            },
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 8,
                "code": "CBSE.MATH.8.2",
                "description": "Linear Equations in One Variable"
            },
            
            # Grade 9 Mathematics
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 9,
                "code": "CBSE.MATH.9.1",
                "description": "Number Systems - Real numbers and their properties"
            },
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 9,
                "code": "CBSE.MATH.9.2",
                "description": "Polynomials - Operations and factorization"
            },
            
            # Grade 10 Mathematics
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 10,
                "code": "CBSE.MATH.10.1",
                "description": "Real Numbers - Euclid's division lemma and algorithm"
            },
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 10,
                "code": "CBSE.MATH.10.2",
                "description": "Polynomials - Relationship between zeros and coefficients"
            },
            
            # Grade 6 Science
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 6,
                "code": "CBSE.SCI.6.1",
                "description": "Food: Where Does It Come From? - Sources of food"
            },
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 6,
                "code": "CBSE.SCI.6.2",
                "description": "Components of Food - Nutrients and their functions"
            },
            
            # Grade 7 Science
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 7,
                "code": "CBSE.SCI.7.1",
                "description": "Nutrition in Plants - Photosynthesis and plant nutrition"
            },
            {
                "locale": Locale.IN,
                "curriculum_board": CurriculumBoard.CBSE,
                "grade_level": 7,
                "code": "CBSE.SCI.7.2",
                "description": "Nutrition in Animals - Digestive system and nutrition"
            }
        ]
        
        # Create standard objects
        for std_data in cbse_standards:
            standard = Standard(**std_data)
            db.add(standard)
        
        db.commit()
        print(f"Successfully seeded {len(cbse_standards)} CBSE standards")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding standards: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_cbse_standards()