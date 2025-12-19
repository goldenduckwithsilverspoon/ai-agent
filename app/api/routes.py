"""
API Routes for Cold Outreach Email Agent

MIP-003 compliant endpoints for the Masumi Network.
"""
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
        name=settings.APP_NAME,
        version=settings.APP_VERSION
    )


@router.get("/input_schema", response_model=InputSchemaResponse)
async def get_input_schema():
    """
    MIP-003 Endpoint: Get the input schema for the agent.
    Returns the expected input data structure for cold outreach email generation.
    """
    schema = [
        {
            "name": "sender_name",
            "type": "string",
            "required": True,
            "description": "Your full name"
        },
        {
            "name": "sender_company",
            "type": "string",
            "required": True,
            "description": "Your company name"
        },
        {
            "name": "sender_role",
            "type": "string",
            "required": True,
            "description": "Your job title/role"
        },
        {
            "name": "sender_email",
            "type": "string",
            "required": False,
            "description": "Your email address (optional)"
        },
        {
            "name": "recipient_name",
            "type": "string",
            "required": True,
            "description": "Recipient's name"
        },
        {
            "name": "recipient_company",
            "type": "string",
            "required": True,
            "description": "Recipient's company name"
        },
        {
            "name": "recipient_role",
            "type": "string",
            "required": False,
            "description": "Recipient's job title/role"
        },
        {
            "name": "recipient_industry",
            "type": "string",
            "required": False,
            "description": "Recipient's industry"
        },
        {
            "name": "product_or_service",
            "type": "string",
            "required": True,
            "description": "What product/service are you offering?"
        },
        {
            "name": "value_proposition",
            "type": "string",
            "required": True,
            "description": "Key value proposition - what problem do you solve?"
        },
        {
            "name": "personalization_notes",
            "type": "string",
            "required": False,
            "description": "Any personal details about the recipient (recent news, shared connections, etc.)"
        },
        {
            "name": "call_to_action",
            "type": "string",
            "required": False,
            "description": "Desired call to action (e.g., 'schedule a 15-min call')"
        },
        {
            "name": "tone",
            "type": "string",
            "required": False,
            "description": "Desired tone: 'professional', 'casual', 'friendly', 'formal', 'persuasive', or 'consultative'",
            "default": "professional"
        },
        {
            "name": "length",
            "type": "string",
            "required": False,
            "description": "Desired length: 'short' (~50-75 words), 'medium' (~100-150 words), or 'long' (~200-250 words)",
            "default": "medium"
        },
        {
            "name": "include_subject_line",
            "type": "boolean",
            "required": False,
            "description": "Whether to generate a subject line",
            "default": True
        },
        {
            "name": "num_variations",
            "type": "integer",
            "required": False,
            "description": "Number of email variations to generate (1-3)",
            "default": 1,
            "minimum": 1,
            "maximum": 3
        },
        {
            "name": "previous_interaction",
            "type": "string",
            "required": False,
            "description": "Any previous interaction or context"
        },
        {
            "name": "specific_pain_points",
            "type": "array",
            "required": False,
            "description": "Specific pain points to address",
            "items": {"type": "string"}
        },
        {
            "name": "competitor_mentions",
            "type": "string",
            "required": False,
            "description": "Any competitor context to reference"
        }
    ]
    
    return InputSchemaResponse(input_data=schema)


@router.post("/start_job", response_model=StartJobResponse)
async def start_job(request: StartJobRequest, background_tasks: BackgroundTasks):
    """
    MIP-003 Endpoint: Start a new cold outreach email generation job.
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
        message=f"Cold outreach email generation started for {request.input_data.recipient_name} at {request.input_data.recipient_company}"
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
