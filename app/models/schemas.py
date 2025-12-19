"""
Pydantic models and schemas for Cold Outreach Email Agent
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class JobStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class EmailTone(str, Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FRIENDLY = "friendly"
    FORMAL = "formal"
    PERSUASIVE = "persuasive"
    CONSULTATIVE = "consultative"


class EmailLength(str, Enum):
    SHORT = "short"       # ~50-75 words
    MEDIUM = "medium"     # ~100-150 words
    LONG = "long"         # ~200-250 words


class EmailInput(BaseModel):
    """Input data for cold outreach email generation"""
    
    # Sender Information
    sender_name: str = Field(..., description="Your full name")
    sender_company: str = Field(..., description="Your company name")
    sender_role: str = Field(..., description="Your job title/role")
    sender_email: Optional[str] = Field(None, description="Your email address")
    
    # Recipient Information
    recipient_name: str = Field(..., description="Recipient's name")
    recipient_company: str = Field(..., description="Recipient's company name")
    recipient_role: Optional[str] = Field(None, description="Recipient's job title/role")
    recipient_industry: Optional[str] = Field(None, description="Recipient's industry")
    
    # Context & Personalization
    product_or_service: str = Field(..., description="What product/service are you offering?")
    value_proposition: str = Field(..., description="Key value proposition - what problem do you solve?")
    personalization_notes: Optional[str] = Field(None, description="Any personal details about the recipient (recent news, shared connections, etc.)")
    call_to_action: Optional[str] = Field(None, description="Desired call to action (e.g., 'schedule a 15-min call', 'reply with interest')")
    
    # Email Preferences
    tone: EmailTone = Field(EmailTone.PROFESSIONAL, description="Desired tone of the email")
    length: EmailLength = Field(EmailLength.MEDIUM, description="Desired length of the email")
    include_subject_line: bool = Field(True, description="Generate a subject line")
    num_variations: int = Field(1, ge=1, le=3, description="Number of email variations to generate (1-3)")
    
    # Optional Context
    previous_interaction: Optional[str] = Field(None, description="Any previous interaction or context")
    specific_pain_points: Optional[List[str]] = Field(default_factory=list, description="Specific pain points to address")
    competitor_mentions: Optional[str] = Field(None, description="Any competitor context to reference")


class StartJobRequest(BaseModel):
    """Request body for /start_job endpoint"""
    identifier_from_purchaser: str = Field(..., description="Unique identifier from the purchaser")
    input_data: EmailInput = Field(..., description="Email generation input data")


class JobStatusResponse(BaseModel):
    """Response body for /status endpoint"""
    job_id: str
    status: JobStatus
    result: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    error: Optional[str] = None


class AvailabilityResponse(BaseModel):
    """Response body for /availability endpoint"""
    status: str = "available"
    name: str
    version: str


class InputSchemaResponse(BaseModel):
    """Response body for /input_schema endpoint"""
    input_data: List[Dict[str, Any]]


class StartJobResponse(BaseModel):
    """Response body for /start_job endpoint"""
    job_id: str
    status: JobStatus
    payment_info: Optional[Dict[str, Any]] = None
    message: str
