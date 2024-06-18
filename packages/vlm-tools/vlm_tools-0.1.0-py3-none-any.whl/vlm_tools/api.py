import os

import requests
from PIL import Image

from vlm_tools.constants import VLM_BASE_URL
from vlm_tools.utils import encode_image


def vlm(image: Image.Image, domain: str):
    """Send an image to the VLM API."""
    VLM_API_KEY = os.getenv("VLM_API_KEY", None)
    if VLM_API_KEY is None:
        raise ValueError("VLM_API_KEY is not set, please set your API key in your environment variable `VLM_API_KEY`.")
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": VLM_API_KEY,
    }
    data = {
        "model": "vlm-1",
        "domain": domain,
        "image": encode_image(image),
    }
    response = requests.post(f"{VLM_BASE_URL}/generate", headers=headers, json=data)
    response.raise_for_status()
    return response.json()
