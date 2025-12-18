from mistralai import Mistral
from app.config import settings
from app.models.schemas import ResumeInput, ResumeStyle, ResumeFormat
from typing import Dict, Any
import json

class ResumeGenerator:
    def __init__(self):
        self.client = Mistral(api_key=settings.MISTRAL_API_KEY)
        self.model = settings.MISTRAL_MODEL
    
    def _format_work_experience(self, experience: list) -> str:
        if not experience:
            return "No work experience provided."
        
        formatted = []
        for exp in experience:
            entry = f"""
- **{exp.job_title}** at **{exp.company}**
  - Location: {exp.location or 'Not specified'}
  - Duration: {exp.start_date} - {exp.end_date or 'Present'}
  - Responsibilities: {', '.join(exp.responsibilities) if exp.responsibilities else 'Not specified'}
"""
            formatted.append(entry)
        return "\n".join(formatted)
    
    def _format_education(self, education: list) -> str:
        if not education:
            return "No education provided."
        
        formatted = []
        for edu in education:
            entry = f"""
- **{edu.degree}** from **{edu.institution}**
  - Location: {edu.location or 'Not specified'}
  - Graduation: {edu.graduation_date}
  - GPA: {edu.gpa or 'Not specified'}
  - Honors: {', '.join(edu.honors) if edu.honors else 'None specified'}
"""
            formatted.append(entry)
        return "\n".join(formatted)
    
    def _format_projects(self, projects: list) -> str:
        if not projects:
            return ""
        
        formatted = []
        for proj in projects:
            entry = f"""
- **{proj.name}**: {proj.description}
  - Technologies: {', '.join(proj.technologies) if proj.technologies else 'Not specified'}
  - Link: {proj.link or 'Not available'}
"""
            formatted.append(entry)
        return "\n".join(formatted)
    
    def _format_certifications(self, certifications: list) -> str:
        if not certifications:
            return ""
        
        formatted = []
        for cert in certifications:
            entry = f"- **{cert.name}** by {cert.issuer} ({cert.date or 'Date not specified'})"
            formatted.append(entry)
        return "\n".join(formatted)
    
    def _get_style_guidelines(self, style: ResumeStyle) -> str:
        guidelines = {
            ResumeStyle.PROFESSIONAL: "Use formal, business-appropriate language. Focus on achievements and metrics. Keep it concise and structured.",
            ResumeStyle.MODERN: "Use clean, contemporary language. Incorporate action verbs and quantifiable results. Balance professionalism with approachability.",
            ResumeStyle.CREATIVE: "Show personality while maintaining professionalism. Use engaging language and highlight unique accomplishments. Good for marketing, design, creative fields.",
            ResumeStyle.EXECUTIVE: "Emphasize leadership, strategic thinking, and high-level achievements. Focus on business impact, revenue growth, team leadership. Suitable for senior/C-level positions.",
            ResumeStyle.TECHNICAL: "Highlight technical skills prominently. Include specific technologies, methodologies, and technical achievements. Use industry-standard terminology.",
            ResumeStyle.ACADEMIC: "Focus on research, publications, teaching experience, grants. Use academic conventions. Suitable for research and academic positions."
        }
        return guidelines.get(style, guidelines[ResumeStyle.PROFESSIONAL])
    
    def _get_format_guidelines(self, format: ResumeFormat) -> str:
        guidelines = {
            ResumeFormat.CHRONOLOGICAL: "List experience in reverse chronological order. Best for consistent career progression.",
            ResumeFormat.FUNCTIONAL: "Group experience by skills/functions rather than timeline. Good for career changers or those with gaps.",
            ResumeFormat.COMBINATION: "Combine skills section with chronological work history. Balances skills with experience timeline."
        }
        return guidelines.get(format, guidelines[ResumeFormat.CHRONOLOGICAL])
    
    async def generate_resume(self, input_data: ResumeInput) -> Dict[str, Any]:
        """Generate a professional resume based on input data."""
        
        # Build the prompt
        prompt = f"""You are an expert resume writer and career coach with 20+ years of experience helping professionals land their dream jobs. Generate a professional, ATS-friendly resume based on the following information.

## CANDIDATE INFORMATION

**Personal Details:**
- Name: {input_data.full_name}
- Email: {input_data.email}
- Phone: {input_data.phone or 'Not provided'}
- Location: {input_data.location or 'Not provided'}
- LinkedIn: {input_data.linkedin or 'Not provided'}
- Portfolio: {input_data.portfolio or 'Not provided'}
- GitHub: {input_data.github or 'Not provided'}

**Target Role:** {input_data.target_role}
**Target Industry:** {input_data.target_industry or 'Not specified'}

**Professional Summary (if provided):** {input_data.professional_summary or 'Generate a compelling professional summary based on the experience below.'}

**Work Experience:**
{self._format_work_experience(input_data.work_experience)}

**Education:**
{self._format_education(input_data.education)}

**Technical Skills:** {', '.join(input_data.technical_skills) if input_data.technical_skills else 'Not specified'}

**Soft Skills:** {', '.join(input_data.soft_skills) if input_data.soft_skills else 'Not specified'}

**Languages:** {', '.join(input_data.languages) if input_data.languages else 'Not specified'}

**Projects:**
{self._format_projects(input_data.projects) if input_data.projects else 'None specified'}

**Certifications:**
{self._format_certifications(input_data.certifications) if input_data.certifications else 'None specified'}

**Achievements:** {', '.join(input_data.achievements) if input_data.achievements else 'None specified'}

**Volunteer Work:** {', '.join(input_data.volunteer_work) if input_data.volunteer_work else 'None specified'}

**Professional Interests:** {', '.join(input_data.interests) if input_data.interests else 'None specified'}

## RESUME STYLE
{self._get_style_guidelines(input_data.style)}

## RESUME FORMAT
{self._get_format_guidelines(input_data.format)}

## JOB DESCRIPTION TO TAILOR TO
{input_data.job_description if input_data.job_description else 'No specific job description provided. Create a general resume for the target role.'}

## INSTRUCTIONS
1. Create a complete, professional resume in clean Markdown format
2. Write a compelling professional summary (3-4 sentences) that highlights key strengths for the target role
3. Rewrite work experience with powerful action verbs and quantifiable achievements where possible
4. Optimize for ATS (Applicant Tracking Systems) by including relevant keywords
5. Ensure the resume is tailored to the target role: {input_data.target_role}
6. Keep the resume to a reasonable length (1-2 pages worth of content)
7. Use bullet points for readability
8. Include all relevant sections based on the provided information

Generate the complete resume now:
"""

        response = await self.client.chat.complete_async(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional resume writer. Create polished, ATS-optimized resumes that help candidates stand out. Always use clear formatting and powerful language."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        resume_content = response.choices[0].message.content
        
        result = {
            "resume": resume_content,
            "metadata": {
                "target_role": input_data.target_role,
                "style": input_data.style.value,
                "format": input_data.format.value,
                "candidate_name": input_data.full_name
            }
        }
        
        # Generate cover letter if requested
        if input_data.include_cover_letter:
            cover_letter = await self._generate_cover_letter(input_data)
            result["cover_letter"] = cover_letter
        
        return result
    
    async def _generate_cover_letter(self, input_data: ResumeInput) -> str:
        """Generate a tailored cover letter."""
        
        prompt = f"""Write a professional cover letter for the following candidate applying for a {input_data.target_role} position.

**Candidate:** {input_data.full_name}
**Email:** {input_data.email}
**Target Role:** {input_data.target_role}
**Target Industry:** {input_data.target_industry or 'Not specified'}

**Key Experience:**
{self._format_work_experience(input_data.work_experience[:2]) if input_data.work_experience else 'Entry-level candidate'}

**Key Skills:** {', '.join(input_data.technical_skills[:10]) if input_data.technical_skills else 'Various skills'}

**Job Description:**
{input_data.job_description if input_data.job_description else 'General application for ' + input_data.target_role + ' position'}

Write a compelling, professional cover letter (3-4 paragraphs) that:
1. Opens with a strong hook that shows enthusiasm for the role
2. Highlights 2-3 key achievements/skills relevant to the position
3. Shows understanding of the target role/industry
4. Closes with a confident call to action

Format the letter properly with date, greeting, body paragraphs, and professional closing.
"""

        response = await self.client.chat.complete_async(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional career coach who writes compelling cover letters that get interviews."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content


# Singleton instance
resume_generator = ResumeGenerator()
