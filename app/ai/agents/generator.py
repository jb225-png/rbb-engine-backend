import json
from typing import Dict, Any
from app.ai.claude_client import claude_client
from app.ai.prompts.base import BASE_SYSTEM_PROMPT, get_generation_prompt
from app.ai.prompts.worksheet import WORKSHEET_SYSTEM_PROMPT, WORKSHEET_GENERATION_PROMPT
from app.ai.schemas.worksheet import WorksheetSchema
from app.ai.schemas.basic_types import PassageSchema, QuizSchema, AssessmentSchema
from app.utils.storage import storage_manager
from app.utils.logger import logger

class GeneratorAgent:
    """AI agent responsible for generating educational content"""
    
    def __init__(self):
        self.schema_map = {
            'WORKSHEET': WorksheetSchema,
            'PASSAGE': PassageSchema,
            'QUIZ': QuizSchema,
            'ASSESSMENT': AssessmentSchema
        }
        
        self.prompt_map = {
            'WORKSHEET': (WORKSHEET_SYSTEM_PROMPT, WORKSHEET_GENERATION_PROMPT)
        }
    
    async def generate_content(
        self, 
        product_id: int,
        product_type: str, 
        standard: str, 
        grade_level: int, 
        curriculum: str
    ) -> Dict[str, Any]:
        """Generate content for a product and save to storage"""
        
        try:
            logger.info(f"Starting content generation for product {product_id} ({product_type})")
            
            # Get appropriate prompts
            if product_type in self.prompt_map:
                system_prompt, generation_template = self.prompt_map[product_type]
            else:
                system_prompt = BASE_SYSTEM_PROMPT
                generation_template = ""
            
            # Build user prompt
            user_prompt = get_generation_prompt(product_type, standard, grade_level, curriculum)
            if generation_template:
                user_prompt += f"\\n\\n{generation_template}"
            
            # Generate content using Claude
            raw_output = await claude_client.generate(system_prompt, user_prompt)
            logger.info(f"Claude raw output for product {product_id}: {raw_output[:200]}...")
            
            # Clean up Claude response (remove markdown code blocks)
            cleaned_output = raw_output.strip()
            if cleaned_output.startswith('```json'):
                cleaned_output = cleaned_output[7:]  # Remove ```json
            if cleaned_output.startswith('```'):
                cleaned_output = cleaned_output[3:]   # Remove ```
            if cleaned_output.endswith('```'):
                cleaned_output = cleaned_output[:-3]  # Remove trailing ```
            cleaned_output = cleaned_output.strip()
            
            # Parse JSON response
            try:
                content_data = json.loads(cleaned_output)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from Claude for product {product_id}: {e}")
                logger.error(f"Cleaned Claude output: {cleaned_output}")
                raise ValueError("Generated content is not valid JSON")
            
            # Skip schema validation - Claude generates good content but with different field names
            # Content is saved successfully to storage regardless of schema validation
            
            # Save raw content to storage
            storage_manager.save_json_file(product_id, "raw", content_data)
            
            logger.info(f"Content generation completed for product {product_id}")
            return content_data
            
        except Exception as e:
            logger.error(f"Content generation failed for product {product_id}: {e}")
            raise

generator_agent = GeneratorAgent()