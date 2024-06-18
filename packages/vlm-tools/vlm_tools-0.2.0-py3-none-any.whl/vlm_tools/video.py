from dataclasses import dataclass
from itertools import islice
from typing import Iterable

import cv2
import numpy as np
from nos.common import tqdm
from nos.common.io import VideoReader  # noqa

try:
    from nos.models import CLIP
except ImportError:
    raise ImportError("Please install the `vlm-tools[torch]` extra to use this module.")


@dataclass
class VideoItertools:
    model = None

    def __post_init__(self):
        self.model = CLIP()

    def islice(
        self,
        stream: Iterable[np.ndarray],
        start: int = 0,
        step: int = 10,
        end: int | None = None,
        similarity_threshold: float = 0.9,
    ) -> Iterable[np.ndarray]:
        last_emb = None

        for img in tqdm(islice(stream, start, end, step)):
            assert isinstance(img, np.ndarray), f"Expected np.ndarray, got {type(img)}"
            _img = cv2.resize(img, (224, 224))
            emb = self.model.encode_image(_img)
            emb /= np.linalg.norm(emb)
            if last_emb is None:
                last_emb = emb
                yield img
            else:
                sim = (emb @ last_emb.T).item()
                if sim < similarity_threshold:
                    last_emb = emb
                    yield img

    def __del__(self):
        del self.model
