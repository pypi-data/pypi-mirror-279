import json
from itertools import islice
from pathlib import Path

import typer
from loguru import logger
from PIL import Image
from tqdm import tqdm

from vlm_tools.api import vlm
from vlm_tools.video import VideoItertools, VideoReader

app = typer.Typer()


@app.command("submit-image")
def submit_image(path: Path, domain: str):
    """Submit an image to the VLM API."""
    typer.echo(f"Submitting image at path={path} to domain={domain}.")
    if not path.exists():
        raise ValueError(f"Path={path} does not exist.")
    if path.suffix not in [".jpg", ".jpeg", ".png"]:
        raise ValueError(f"Path={path} is not a valid image file.")

    image = Image.open(path)
    response = vlm(image, domain)
    logger.info("Response")
    logger.info("\n" + json.dumps(response, indent=2))


@app.command("submit-video")
def submit_video(path: Path, domain: str, max_frames: int = 10):
    """Submit a video in a streaming fashion to the VLM API."""
    typer.echo(f"Submitting video at path={path} to domain={domain}.")
    if not path.exists():
        raise ValueError(f"Path={path} does not exist.")
    if path.suffix not in [".mp4", ".avi", ".mov"]:
        raise ValueError(f"Path={path} is not a valid video file.")

    v_itertools = VideoItertools()
    video = VideoReader(path)
    stream = v_itertools.islice(video, similarity_threshold=0.9)
    n = len(video)
    for _idx, img in tqdm(enumerate(islice(stream, max_frames)), desc="Processing frames"):
        img = Image.fromarray(img).convert("RGB")
        response = vlm(img, domain)
        logger.info("\n" + json.dumps(response, indent=2))
    logger.info(f"video={path}, nframes={n}, processed={_idx+1}, sampling_rate={(_idx + 1) * 100. / n:.2f}%")


if __name__ == "__main__":
    app()
