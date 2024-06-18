import os
from pathlib import Path

VLM_BASE_URL = os.getenv("VLM_BASE_URL", "https://api.vlm.run/v1")

VLM_TOOLS_HOME = Path(os.getenv("VLM_TOOLS_HOME", str(Path.home() / ".vlm-tools")))
VLM_TOOLS_CACHE_DIR = VLM_TOOLS_HOME / "cache"
VLM_TOOLS_HOME.mkdir(parents=True, exist_ok=True)
VLM_TOOLS_CACHE_DIR.mkdir(parents=True, exist_ok=True)
