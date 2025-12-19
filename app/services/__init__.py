"""
Service layer exports for Cold Outreach Email Agent
"""
from .email_generator import email_generator, EmailGenerator
from .job_manager import job_manager, JobManager

__all__ = [
    "email_generator",
    "EmailGenerator",
    "job_manager", 
    "JobManager"
]
