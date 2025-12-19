"""
Cold Outreach Email Generator Service

Uses Mistral AI to generate personalized cold outreach emails.
"""
from mistralai import Mistral
from app.config import settings
from app.models.schemas import EmailInput, EmailTone, EmailLength
from typing import Dict, Any, List


class EmailGenerator:
    def __init__(self):
        self.client = Mistral(api_key=settings.MISTRAL_API_KEY)
        self.model = settings.MISTRAL_MODEL
    
    def _get_tone_instructions(self, tone: EmailTone) -> str:
        """Get writing style instructions based on tone."""
        instructions = {
            EmailTone.PROFESSIONAL: "Use a polished, business-appropriate tone. Be direct and respectful.",
            EmailTone.CASUAL: "Keep it conversational and relaxed while still being professional. Avoid stiff corporate language.",
            EmailTone.FRIENDLY: "Be warm and personable. Write as if reaching out to a potential friend in business.",
            EmailTone.FORMAL: "Use proper business etiquette. Be respectful and courteous throughout.",
            EmailTone.PERSUASIVE: "Focus on compelling benefits and creating urgency. Use persuasive language without being pushy.",
            EmailTone.CONSULTATIVE: "Position yourself as a helpful advisor. Focus on understanding their needs and offering solutions."
        }
        return instructions.get(tone, instructions[EmailTone.PROFESSIONAL])
    
    def _get_length_instructions(self, length: EmailLength) -> str:
        """Get length instructions."""
        instructions = {
            EmailLength.SHORT: "Keep the email very concise - around 50-75 words. Get straight to the point.",
            EmailLength.MEDIUM: "Write a moderate-length email - around 100-150 words. Balance detail with brevity.",
            EmailLength.LONG: "Write a more detailed email - around 200-250 words. Include more context and benefits."
        }
        return instructions.get(length, instructions[EmailLength.MEDIUM])
    
    def _build_personalization_context(self, input_data: EmailInput) -> str:
        """Build personalization context from input data."""
        context_parts = []
        
        if input_data.personalization_notes:
            context_parts.append(f"Personal details: {input_data.personalization_notes}")
        
        if input_data.previous_interaction:
            context_parts.append(f"Previous interaction: {input_data.previous_interaction}")
        
        if input_data.specific_pain_points:
            context_parts.append(f"Pain points to address: {', '.join(input_data.specific_pain_points)}")
        
        if input_data.competitor_mentions:
            context_parts.append(f"Competitor context: {input_data.competitor_mentions}")
        
        return "\n".join(context_parts) if context_parts else "No additional context provided."
    
    async def generate_email(self, input_data: EmailInput) -> Dict[str, Any]:
        """Generate personalized cold outreach email(s)."""
        
        personalization_context = self._build_personalization_context(input_data)
        
        prompt = f"""You are an expert B2B sales copywriter specializing in cold outreach emails that get responses. Generate a personalized cold outreach email based on the following information.

## SENDER INFORMATION
- Name: {input_data.sender_name}
- Company: {input_data.sender_company}
- Role: {input_data.sender_role}

## RECIPIENT INFORMATION
- Name: {input_data.recipient_name}
- Company: {input_data.recipient_company}
- Role: {input_data.recipient_role or 'Not specified'}
- Industry: {input_data.recipient_industry or 'Not specified'}

## OFFERING
- Product/Service: {input_data.product_or_service}
- Value Proposition: {input_data.value_proposition}

## PERSONALIZATION CONTEXT
{personalization_context}

## CALL TO ACTION
{input_data.call_to_action or 'Schedule a brief call to discuss further'}

## WRITING STYLE
{self._get_tone_instructions(input_data.tone)}

## LENGTH
{self._get_length_instructions(input_data.length)}

## REQUIREMENTS
1. {"Start with a compelling subject line (prefix with 'Subject: ')" if input_data.include_subject_line else "Do not include a subject line"}
2. Open with a hook that references the recipient personally or their company
3. Quickly establish relevance and value
4. Keep the email scannable - short paragraphs
5. End with a clear, low-friction call to action
6. NO spam triggers or overused sales phrases
7. Sound human, not like a template
8. Generate {input_data.num_variations} variation(s)

{f'Generate {input_data.num_variations} different variations of this email, each with a unique angle or approach. Separate each variation with "---VARIATION---"' if input_data.num_variations > 1 else 'Generate the email now:'}
"""

        response = await self.client.chat.complete_async(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert cold email copywriter. You write emails that get opened and replied to. Your emails are personalized, concise, and provide clear value. Never use spam triggers or generic templates."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,  # Higher temperature for more creative variations
            max_tokens=2000
        )
        
        email_content = response.choices[0].message.content
        
        # Parse variations if multiple were requested
        if input_data.num_variations > 1 and "---VARIATION---" in email_content:
            variations = [v.strip() for v in email_content.split("---VARIATION---") if v.strip()]
        else:
            variations = [email_content]
        
        result = {
            "emails": variations,
            "metadata": {
                "recipient_name": input_data.recipient_name,
                "recipient_company": input_data.recipient_company,
                "tone": input_data.tone.value,
                "length": input_data.length.value,
                "variations_generated": len(variations)
            }
        }
        
        return result


# Singleton instance
email_generator = EmailGenerator()
