from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from pathlib import Path
import json
from typing import Dict, Any
from app.utils.logger import logger
from app.utils.storage import storage_manager

class PDFGenerator:
    """Generate PDF files from AI-generated content"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        ))
        
        self.styles.add(ParagraphStyle(
            name='QuestionStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            leftIndent=20
        ))
    
    def generate_worksheet_pdf(self, product_id: int, content_data: Dict[str, Any]) -> Path:
        """Generate PDF for worksheet content"""
        try:
            # Get product storage path
            product_path = storage_manager.get_product_path(product_id)
            pdf_path = product_path / f"worksheet_{product_id}.pdf"
            
            # Create PDF document
            doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
            story = []
            
            # Title
            title = content_data.get('title', 'Educational Worksheet')
            story.append(Paragraph(title, self.styles['CustomTitle']))
            story.append(Spacer(1, 20))
            
            # Basic info
            grade_level = content_data.get('grade_level', 'N/A')
            subject = content_data.get('subject', 'N/A')
            estimated_time = content_data.get('estimated_time', 'N/A')
            
            info_text = f"<b>Grade:</b> {grade_level} | <b>Subject:</b> {subject} | <b>Time:</b> {estimated_time}"
            story.append(Paragraph(info_text, self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Learning objectives
            if 'learning_objectives' in content_data:
                story.append(Paragraph("<b>Learning Objectives:</b>", self.styles['Heading2']))
                for obj in content_data['learning_objectives']:
                    story.append(Paragraph(f"• {obj}", self.styles['Normal']))
                story.append(Spacer(1, 15))
            
            # Instructions
            if 'instructions' in content_data:
                story.append(Paragraph("<b>Instructions:</b>", self.styles['Heading2']))
                story.append(Paragraph(content_data['instructions'], self.styles['Normal']))
                story.append(Spacer(1, 20))
            
            # Questions
            if 'questions' in content_data:
                story.append(Paragraph("<b>Questions:</b>", self.styles['Heading2']))
                story.append(Spacer(1, 10))
                
                for i, question in enumerate(content_data['questions'], 1):
                    # Question number and text
                    q_text = question.get('question', f'Question {i}')
                    story.append(Paragraph(f"<b>{i}. {q_text}</b>", self.styles['QuestionStyle']))
                    
                    # Multiple choice options
                    if question.get('type') == 'multiple_choice' and 'options' in question:
                        for j, option in enumerate(question['options']):
                            letter = chr(65 + j)  # A, B, C, D
                            story.append(Paragraph(f"   {letter}) {option}", self.styles['Normal']))
                    
                    # Points
                    points = question.get('points', 1)
                    story.append(Paragraph(f"<i>Points: {points}</i>", self.styles['Normal']))
                    story.append(Spacer(1, 15))
            
            # Build PDF
            doc.build(story)
            logger.info(f"Generated PDF for product {product_id}: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"PDF generation failed for product {product_id}: {e}")
            raise
    
    def generate_quiz_pdf(self, product_id: int, content_data: Dict[str, Any]) -> Path:
        """Generate PDF for quiz content"""
        # Similar to worksheet but with quiz-specific formatting
        return self.generate_worksheet_pdf(product_id, content_data)
    
    def generate_pdf_from_content(self, product_id: int, product_type: str, content_data: Dict[str, Any]) -> Path:
        """Generate PDF based on product type"""
        if product_type.upper() == 'WORKSHEET':
            return self.generate_worksheet_pdf(product_id, content_data)
        elif product_type.upper() == 'QUIZ':
            return self.generate_quiz_pdf(product_id, content_data)
        else:
            # Default to worksheet format for other types
            return self.generate_worksheet_pdf(product_id, content_data)

pdf_generator = PDFGenerator()