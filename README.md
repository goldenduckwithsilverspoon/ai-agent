# Resume Generator Agent

AI-powered professional resume and CV generator built for the Masumi Network.

## Features

- **Smart Resume Generation**: Creates professional, ATS-optimized resumes
- **Multiple Styles**: Professional, Modern, Creative, Executive, Technical, Academic
- **Multiple Formats**: Chronological, Functional, Combination
- **Cover Letter Generation**: Optional tailored cover letters
- **Job Description Tailoring**: Customize resume for specific job postings
- **MIP-003 Compliant**: Full Masumi protocol compatibility

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/availability` | GET | Check agent availability |
| `/input_schema` | GET | Get input data structure |
| `/start_job` | POST | Start resume generation |
| `/status` | GET | Check job status |
| `/docs` | GET | Interactive API documentation |

## Quick Start

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your MISTRAL_API_KEY

# Run the server
uvicorn app.main:app --reload --port 8000
```

### Example Request

```bash
curl -X POST "http://localhost:8000/start_job" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "user123",
    "input_data": {
      "full_name": "John Doe",
      "email": "john@example.com",
      "phone": "+1 555-123-4567",
      "location": "San Francisco, USA",
      "target_role": "Senior Software Engineer",
      "target_industry": "Technology",
      "work_experience": [
        {
          "job_title": "Software Engineer",
          "company": "Tech Corp",
          "location": "San Francisco, USA",
          "start_date": "Jan 2020",
          "end_date": "Present",
          "responsibilities": [
            "Developed microservices architecture",
            "Led team of 5 engineers",
            "Reduced deployment time by 50%"
          ]
        }
      ],
      "education": [
        {
          "degree": "B.S. Computer Science",
          "institution": "Stanford University",
          "graduation_date": "May 2019"
        }
      ],
      "technical_skills": ["Python", "JavaScript", "AWS", "Docker", "Kubernetes"],
      "soft_skills": ["Leadership", "Communication", "Problem Solving"],
      "style": "professional",
      "format": "chronological",
      "include_cover_letter": true
    }
  }'
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MISTRAL_API_KEY` | Mistral AI API key | Yes |
| `PAYMENT_SERVICE_URL` | Masumi payment service URL | For production |
| `PAYMENT_API_KEY` | Masumi payment API key | For production |
| `AGENT_IDENTIFIER` | Registered agent identifier | For production |
| `NETWORK` | Cardano network (Preprod/Mainnet) | For production |

## Resume Styles

- **Professional**: Formal, business-appropriate language
- **Modern**: Clean, contemporary with action verbs
- **Creative**: Personality-forward for creative fields
- **Executive**: Leadership and strategic focus for C-level
- **Technical**: Skills-prominent for engineering roles
- **Academic**: Research and publication focused

## Author

Dhanush Kenkiri

## License

MIT
