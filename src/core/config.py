import os

PROJECT_ID: str = str(os.environ.get("PROJECT_ID", "default"))
CLOUD: bool = bool(os.environ.get("CLOUD", False))