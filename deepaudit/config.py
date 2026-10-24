"""
Configuration Loader for DeepAudit: Forensic Corporate & Due Diligence Agent.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY", "")
NEBIUS_BASE_URL = os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "nvidia/Nemotron-3_5-Lightning")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "3500"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))
