"""
Configuration settings for Cold Outreach Email Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Agent Identity
    APP_NAME: str = "Cold Outreach Email Agent"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-powered personalized cold outreach email generator for B2B sales and business development"
    
    # Mistral AI Configuration
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_MODEL: str = "mistral-large-latest"
    
    # Payment Service Configuration (for Masumi integration)
    PAYMENT_SERVICE_URL: str = os.getenv("PAYMENT_SERVICE_URL", "http://localhost:3001/api/v1")
    PAYMENT_API_KEY: str = os.getenv("PAYMENT_API_KEY", "")
    AGENT_IDENTIFIER: str = os.getenv("AGENT_IDENTIFIER", "")
    NETWORK: str = os.getenv("NETWORK", "Preprod")
    
    # Agent Pricing (in tUSDM - 1 USDM = 1,000,000 smallest unit)
    PAYMENT_AMOUNT: int = 1000000  # 1 USDM
    PAYMENT_UNIT: str = "16a55b2a349361ff88c03788f93e1e966e5d689605d044fef722ddde0014df10745553444d"


settings = Settings()
