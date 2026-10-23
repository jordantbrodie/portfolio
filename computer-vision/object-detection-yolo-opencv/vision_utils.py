"""Drawing and bookkeeping helpers shared by detect.py and the classic OpenCV demo.

Kept free of any deep-learning imports so they can be unit-tested on their own.
"""
from __future__ import annotations

import time
from collections import Counter, deque
from dataclasses import dataclass

import cv2
import numpy as np

# One fixed BGR colour per class id, so a class keeps its colour between frames.
PALETTE = [
    (66, 135, 245), (245, 105, 66), (80, 200, 120),
    (200, 80, 200), (240, 200, 60), (60, 200, 220),
]


@dataclass
class Detection:
    x1: int
    y1: int
    x2: int
    y2: int
    cls_id: int
    label: str
    conf: float

    @property
    def centre(self) -> tuple[int, int]:
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2


def colour_for(cls_id: int) -> tuple[int, int, int]:
    return PALETTE[cls_id % len(PALETTE)]


def draw_detections(frame: np.ndarray, detections: list[Detection]) -> np.ndarray:
    """Draw a box and a 'label 97%' tag for every detection (in place)."""
    for d in detections:
        c = colour_for(d.cls_id)
        cv2.rectangle(frame, (d.x1, d.y1), (d.x2, d.y2), c, 2)
        tag = f"{d.label} {d.conf * 100:.0f}%"
        (tw, th), _ = cv2.getTextSize(tag, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
        top = max(d.y1 - th - 6, 0)
        cv2.rectangle(frame, (d.x1, top), (d.x1 + tw + 6, top + th + 6), c, -1)
        cv2.putText(frame, tag, (d.x1 + 3, top + th + 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    return frame


def count_by_label(detections: list[Detection]) -> dict[str, int]:
    return dict(Counter(d.label for d in detections))


def draw_hud(frame: np.ndarray, fps: float, counts: dict[str, int]) -> np.ndarray:
    """Top-left overlay with frame rate and per-class object counts."""
    lines = [f"FPS {fps:5.1f}"] + [f"{k}: {v}" for k, v in sorted(counts.items())]
    for i, text in enumerate(lines):
        y = 22 + i * 22
        cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    return frame


class FpsMeter:
    """Frame rate averaged over the last `window` frames."""

    def __init__(self, window: int = 30):
        self.stamps: deque[float] = deque(maxlen=window)

    def tick(self, now: float | None = None) -> float:
        self.stamps.append(time.perf_counter() if now is None else now)
        if len(self.stamps) < 2:
            return 0.0
        span = self.stamps[-1] - self.stamps[0]
        return (len(self.stamps) - 1) / span if span > 0 else 0.0
