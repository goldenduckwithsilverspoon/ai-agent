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
    JobStatus,
    DemoResponse,
    DemoOutput
)
from app.services.job_manager import job_manager
from app.config import settings

router = APIRouter()


@router.get("/availability", response_model=AvailabilityResponse)
async def check_availability():
    """
    MIP-003 Endpoint: Check if the agent is available.
    Returns the availability status, agent name, type, and version.
    """
    return AvailabilityResponse(
        status="available",
        type="masumi-agent",
        name=settings.APP_NAME,
        version=settings.APP_VERSION,
        message="Cold Outreach Email Agent is ready to accept jobs"
    )


@router.get("/input_schema", response_model=InputSchemaResponse)
async def get_input_schema():
    """
    MIP-003 Endpoint: Get the input schema for the agent.
    Returns the expected input data structure for cold outreach email generation.
    """
    schema = [
        {
            "id": "sender_name",
            "name": "Sender Name",
            "type": "string",
            "required": True,
            "description": "Your full name"
        },
        {
            "id": "sender_company",
            "name": "Sender Company",
            "type": "string",
            "required": True,
            "description": "Your company name"
        },
        {
            "id": "sender_role",
            "name": "Sender Role",
            "type": "string",
            "required": True,
            "description": "Your job title/role"
        },
        {
            "id": "sender_email",
            "name": "Sender Email",
            "type": "string",
            "required": False,
            "description": "Your email address (optional)"
        },
        {
            "id": "recipient_name",
            "name": "Recipient Name",
            "type": "string",
            "required": True,
            "description": "Recipient's name"
        },
        {
            "id": "recipient_company",
            "name": "Recipient Company",
            "type": "string",
            "required": True,
            "description": "Recipient's company name"
        },
        {
            "id": "recipient_role",
            "name": "Recipient Role",
            "type": "string",
            "required": False,
            "description": "Recipient's job title/role"
        },
        {
            "id": "recipient_industry",
            "name": "Recipient Industry",
            "type": "string",
            "required": False,
            "description": "Recipient's industry"
        },
        {
            "id": "product_or_service",
            "name": "Product or Service",
            "type": "string",
            "required": True,
            "description": "What product/service are you offering?"
        },
        {
            "id": "value_proposition",
            "name": "Value Proposition",
            "type": "string",
            "required": True,
            "description": "Key value proposition - what problem do you solve?"
        },
        {
            "id": "personalization_notes",
            "name": "Personalization Notes",
            "type": "string",
            "required": False,
            "description": "Any personal details about the recipient (recent news, shared connections, etc.)"
        },
        {
            "id": "call_to_action",
            "name": "Call to Action",
            "type": "string",
            "required": False,
            "description": "Desired call to action (e.g., 'schedule a 15-min call')"
        },
        {
            "id": "tone",
            "name": "Tone",
            "type": "option",
            "required": False,
            "description": "Desired tone of the email",
            "data": {
                "options": ["professional", "casual", "friendly", "formal", "persuasive", "consultative"]
            }
        },
        {
            "id": "length",
            "name": "Length",
            "type": "option",
            "required": False,
            "description": "Desired length: 'short' (~50-75 words), 'medium' (~100-150 words), or 'long' (~200-250 words)",
            "data": {
                "options": ["short", "medium", "long"]
            }
        },
        {
            "id": "include_subject_line",
            "name": "Include Subject Line",
            "type": "boolean",
            "required": False,
            "description": "Whether to generate a subject line"
        },
        {
            "id": "num_variations",
            "name": "Number of Variations",
            "type": "number",
            "required": False,
            "description": "Number of email variations to generate (1-3)",
            "validations": [
                {"min": 1},
                {"max": 3}
            ]
        },
        {
            "id": "previous_interaction",
            "name": "Previous Interaction",
            "type": "string",
            "required": False,
            "description": "Any previous interaction or context"
        },
        {
            "id": "specific_pain_points",
            "name": "Specific Pain Points",
            "type": "string",
            "required": False,
            "description": "Specific pain points to address (comma-separated)"
        },
        {
            "id": "competitor_mentions",
            "name": "Competitor Mentions",
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


@router.get("/demo", response_model=DemoResponse)
async def get_demo():
    """
    MIP-003 Optional Endpoint: Get demo data for marketing purposes.
    Returns example input and output to showcase the service's capabilities.
    """
    return DemoResponse(
        input={
            "sender_name": "Alex Chen",
            "sender_company": "TechStartup AI",
            "sender_role": "Founder & CEO",
            "sender_email": "alex@techstartupai.com",
            "recipient_name": "Sarah Johnson",
            "recipient_company": "Enterprise Corp",
            "recipient_role": "VP of Engineering",
            "recipient_industry": "Financial Services",
            "product_or_service": "AI-powered code review platform",
            "value_proposition": "Reduce code review time by 60% while catching 3x more bugs before production",
            "personalization_notes": "Recently spoke at DevConf about scaling engineering teams",
            "call_to_action": "15-minute demo call",
            "tone": "professional",
            "length": "medium"
        },
        output=DemoOutput(
            result="""Subject: Scaling engineering at Enterprise Corp - quick thought

Hi Sarah,

Caught your DevConf talk on scaling engineering teams - your point about review bottlenecks really resonated with us.

We built an AI code review platform that's helping teams like yours cut review time by 60% while actually catching more bugs (3x more, based on customer data). Given Enterprise Corp's growth, thought this might be worth a quick conversation.

Would you be open to a 15-minute call next week to see if this could help your team ship faster?

Best,
Alex Chen
Founder, TechStartup AI"""
        )
    )
