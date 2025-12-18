from typing import Dict, Optional
from datetime import datetime
import uuid
from app.models.schemas import JobStatus, ResumeInput
from app.services.resume_generator import resume_generator
import asyncio

class JobManager:
    def __init__(self):
        self.jobs: Dict[str, dict] = {}
    
    def create_job(self, identifier_from_purchaser: str, input_data: ResumeInput) -> str:
        """Create a new job and return the job ID."""
        job_id = str(uuid.uuid4())
        
        self.jobs[job_id] = {
            "job_id": job_id,
            "identifier_from_purchaser": identifier_from_purchaser,
            "input_data": input_data,
            "status": JobStatus.PENDING,
            "result": None,
            "error": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        return job_id
    
    def get_job(self, job_id: str) -> Optional[dict]:
        """Get job by ID."""
        return self.jobs.get(job_id)
    
    def update_job_status(self, job_id: str, status: JobStatus, result: dict = None, error: str = None):
        """Update job status."""
        if job_id in self.jobs:
            self.jobs[job_id]["status"] = status
            self.jobs[job_id]["updated_at"] = datetime.utcnow()
            
            if result:
                self.jobs[job_id]["result"] = result
            if error:
                self.jobs[job_id]["error"] = error
    
    async def process_job(self, job_id: str):
        """Process the resume generation job."""
        job = self.get_job(job_id)
        if not job:
            return
        
        try:
            self.update_job_status(job_id, JobStatus.IN_PROGRESS)
            
            # Generate the resume
            result = await resume_generator.generate_resume(job["input_data"])
            
            self.update_job_status(job_id, JobStatus.COMPLETED, result=result)
            
        except Exception as e:
            self.update_job_status(job_id, JobStatus.FAILED, error=str(e))

# Singleton instance
job_manager = JobManager()
