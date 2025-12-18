from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

class JobStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ResumeStyle(str, Enum):
    PROFESSIONAL = "professional"
    MODERN = "modern"
    CREATIVE = "creative"
    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    ACADEMIC = "academic"

class ResumeFormat(str, Enum):
    CHRONOLOGICAL = "chronological"
    FUNCTIONAL = "functional"
    COMBINATION = "combination"

class WorkExperience(BaseModel):
    job_title: str = Field(..., description="Job title/position")
    company: str = Field(..., description="Company name")
    location: Optional[str] = Field(None, description="City, Country")
    start_date: str = Field(..., description="Start date (e.g., 'Jan 2020')")
    end_date: Optional[str] = Field("Present", description="End date or 'Present'")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities and achievements")

class Education(BaseModel):
    degree: str = Field(..., description="Degree name (e.g., 'Bachelor of Science in Computer Science')")
    institution: str = Field(..., description="University/College name")
    location: Optional[str] = Field(None, description="City, Country")
    graduation_date: str = Field(..., description="Graduation date (e.g., 'May 2020')")
    gpa: Optional[str] = Field(None, description="GPA if notable")
    honors: Optional[List[str]] = Field(default_factory=list, description="Honors, awards, relevant coursework")

class Project(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Brief description")
    technologies: Optional[List[str]] = Field(default_factory=list, description="Technologies used")
    link: Optional[str] = Field(None, description="Project URL if available")

class Certification(BaseModel):
    name: str = Field(..., description="Certification name")
    issuer: str = Field(..., description="Issuing organization")
    date: Optional[str] = Field(None, description="Date obtained")
    credential_id: Optional[str] = Field(None, description="Credential ID if applicable")

class ResumeInput(BaseModel):
    # Personal Information
    full_name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="City, Country")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    portfolio: Optional[str] = Field(None, description="Portfolio/Personal website URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    
    # Professional Summary
    professional_summary: Optional[str] = Field(None, description="Brief professional summary or objective (optional - AI will generate if not provided)")
    
    # Target Role
    target_role: str = Field(..., description="Target job title/role you're applying for")
    target_industry: Optional[str] = Field(None, description="Target industry")
    
    # Experience & Education
    work_experience: List[WorkExperience] = Field(default_factory=list, description="Work experience entries")
    education: List[Education] = Field(default_factory=list, description="Education entries")
    
    # Skills
    technical_skills: List[str] = Field(default_factory=list, description="Technical/hard skills")
    soft_skills: List[str] = Field(default_factory=list, description="Soft skills")
    languages: Optional[List[str]] = Field(default_factory=list, description="Languages spoken")
    
    # Additional Sections
    projects: Optional[List[Project]] = Field(default_factory=list, description="Notable projects")
    certifications: Optional[List[Certification]] = Field(default_factory=list, description="Certifications")
    achievements: Optional[List[str]] = Field(default_factory=list, description="Key achievements/awards")
    volunteer_work: Optional[List[str]] = Field(default_factory=list, description="Volunteer experience")
    interests: Optional[List[str]] = Field(default_factory=list, description="Professional interests")
    
    # Resume Preferences
    style: ResumeStyle = Field(ResumeStyle.PROFESSIONAL, description="Resume style")
    format: ResumeFormat = Field(ResumeFormat.CHRONOLOGICAL, description="Resume format")
    include_cover_letter: bool = Field(False, description="Generate a cover letter as well")
    job_description: Optional[str] = Field(None, description="Job description to tailor resume to")

class StartJobRequest(BaseModel):
    identifier_from_purchaser: str = Field(..., description="Unique identifier from the purchaser")
    input_data: ResumeInput = Field(..., description="Resume input data")

class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    result: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    error: Optional[str] = None

class AvailabilityResponse(BaseModel):
    status: str = "available"
    agent_name: str
    version: str

class InputSchemaResponse(BaseModel):
    input_data: List[Dict[str, Any]]

class StartJobResponse(BaseModel):
    job_id: str
    status: JobStatus
    payment_info: Optional[Dict[str, Any]] = None
    message: str
