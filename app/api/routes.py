from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models.schemas import (
    AvailabilityResponse,
    InputSchemaResponse,
    StartJobRequest,
    StartJobResponse,
    JobStatusResponse,
    JobStatus
)
from app.services.job_manager import job_manager
from app.config import settings

router = APIRouter()

@router.get("/availability", response_model=AvailabilityResponse)
async def check_availability():
    """
    MIP-003 Endpoint: Check if the agent is available.
    Returns the availability status, agent name, and version.
    """
    return AvailabilityResponse(
        status="available",
        agent_name=settings.APP_NAME,
        version=settings.APP_VERSION
    )

@router.get("/input_schema", response_model=InputSchemaResponse)
async def get_input_schema():
    """
    MIP-003 Endpoint: Get the input schema for the agent.
    Returns the expected input data structure.
    """
    schema = [
        {
            "name": "full_name",
            "type": "string",
            "required": True,
            "description": "Your full name"
        },
        {
            "name": "email",
            "type": "string",
            "required": True,
            "description": "Your email address"
        },
        {
            "name": "phone",
            "type": "string",
            "required": False,
            "description": "Your phone number"
        },
        {
            "name": "location",
            "type": "string",
            "required": False,
            "description": "Your city and country (e.g., 'San Francisco, USA')"
        },
        {
            "name": "linkedin",
            "type": "string",
            "required": False,
            "description": "Your LinkedIn profile URL"
        },
        {
            "name": "portfolio",
            "type": "string",
            "required": False,
            "description": "Your portfolio or personal website URL"
        },
        {
            "name": "github",
            "type": "string",
            "required": False,
            "description": "Your GitHub profile URL"
        },
        {
            "name": "target_role",
            "type": "string",
            "required": True,
            "description": "The job title/role you're applying for (e.g., 'Senior Software Engineer')"
        },
        {
            "name": "target_industry",
            "type": "string",
            "required": False,
            "description": "Target industry (e.g., 'Technology', 'Finance')"
        },
        {
            "name": "professional_summary",
            "type": "string",
            "required": False,
            "description": "Brief professional summary (AI will generate if not provided)"
        },
        {
            "name": "work_experience",
            "type": "array",
            "required": False,
            "description": "List of work experience entries",
            "items": {
                "type": "object",
                "properties": {
                    "job_title": {"type": "string", "description": "Job title"},
                    "company": {"type": "string", "description": "Company name"},
                    "location": {"type": "string", "description": "City, Country"},
                    "start_date": {"type": "string", "description": "Start date (e.g., 'Jan 2020')"},
                    "end_date": {"type": "string", "description": "End date or 'Present'"},
                    "responsibilities": {"type": "array", "items": {"type": "string"}, "description": "Key responsibilities"}
                }
            }
        },
        {
            "name": "education",
            "type": "array",
            "required": False,
            "description": "List of education entries",
            "items": {
                "type": "object",
                "properties": {
                    "degree": {"type": "string", "description": "Degree name"},
                    "institution": {"type": "string", "description": "Institution name"},
                    "location": {"type": "string", "description": "City, Country"},
                    "graduation_date": {"type": "string", "description": "Graduation date"},
                    "gpa": {"type": "string", "description": "GPA if notable"},
                    "honors": {"type": "array", "items": {"type": "string"}, "description": "Honors/awards"}
                }
            }
        },
        {
            "name": "technical_skills",
            "type": "array",
            "required": False,
            "description": "List of technical/hard skills",
            "items": {"type": "string"}
        },
        {
            "name": "soft_skills",
            "type": "array",
            "required": False,
            "description": "List of soft skills",
            "items": {"type": "string"}
        },
        {
            "name": "languages",
            "type": "array",
            "required": False,
            "description": "Languages spoken",
            "items": {"type": "string"}
        },
        {
            "name": "projects",
            "type": "array",
            "required": False,
            "description": "Notable projects",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "technologies": {"type": "array", "items": {"type": "string"}},
                    "link": {"type": "string"}
                }
            }
        },
        {
            "name": "certifications",
            "type": "array",
            "required": False,
            "description": "Professional certifications",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "issuer": {"type": "string"},
                    "date": {"type": "string"},
                    "credential_id": {"type": "string"}
                }
            }
        },
        {
            "name": "achievements",
            "type": "array",
            "required": False,
            "description": "Key achievements/awards",
            "items": {"type": "string"}
        },
        {
            "name": "style",
            "type": "string",
            "required": False,
            "description": "Resume style: 'professional', 'modern', 'creative', 'executive', 'technical', or 'academic'",
            "default": "professional"
        },
        {
            "name": "format",
            "type": "string",
            "required": False,
            "description": "Resume format: 'chronological', 'functional', or 'combination'",
            "default": "chronological"
        },
        {
            "name": "include_cover_letter",
            "type": "boolean",
            "required": False,
            "description": "Whether to also generate a cover letter",
            "default": False
        },
        {
            "name": "job_description",
            "type": "string",
            "required": False,
            "description": "Job description to tailor the resume to"
        }
    ]
    
    return InputSchemaResponse(input_data=schema)

@router.post("/start_job", response_model=StartJobResponse)
async def start_job(request: StartJobRequest, background_tasks: BackgroundTasks):
    """
    MIP-003 Endpoint: Start a new resume generation job.
    Creates a job and processes it in the background.
    """
    # Create the job
    job_id = job_manager.create_job(
        identifier_from_purchaser=request.identifier_from_purchaser,
        input_data=request.input_data
    )
    
    # Process job in background
    background_tasks.add_task(job_manager.process_job, job_id)
    
    # Return response with payment info for Masumi integration
    return StartJobResponse(
        job_id=job_id,
        status=JobStatus.PENDING,
        payment_info={
            "amount": settings.PAYMENT_AMOUNT,
            "unit": settings.PAYMENT_UNIT,
            "agent_identifier": settings.AGENT_IDENTIFIER,
            "network": settings.NETWORK
        },
        message=f"Resume generation job created. Generating {request.input_data.style.value} resume for {request.input_data.full_name}"
    )

@router.get("/status", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """
    MIP-003 Endpoint: Get the status of a job.
    Returns the current status and result if completed.
    """
    job = job_manager.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatusResponse(
        job_id=job["job_id"],
        status=job["status"],
        result=job["result"],
        created_at=job["created_at"],
        updated_at=job["updated_at"],
        error=job["error"]
    )
