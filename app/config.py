import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "Resume Generator Agent"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-powered professional resume and CV generator"
    
    # Mistral AI Configuration
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_MODEL: str = "mistral-large-latest"
    
    # Payment Service Configuration
    PAYMENT_SERVICE_URL: str = os.getenv("PAYMENT_SERVICE_URL", "http://localhost:3001/api/v1")
    PAYMENT_API_KEY: str = os.getenv("PAYMENT_API_KEY", "")
    AGENT_IDENTIFIER: str = os.getenv("AGENT_IDENTIFIER", "")
    NETWORK: str = os.getenv("NETWORK", "Preprod")
    
    # Agent Pricing (in lovelace - 1 ADA = 1,000,000 lovelace)
    PAYMENT_AMOUNT: int = 5000000  # 5 ADA
    PAYMENT_UNIT: str = "lovelace"

settings = Settings()
