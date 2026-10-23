"""Classic (non-deep-learning) OpenCV pipeline: find and track coloured objects.

Pipeline: BGR -> HSV -> colour threshold -> morphological clean-up -> contours
-> bounding boxes + centroids -> nearest-neighbour ID tracking between frames.

Usage:
    python classic_cv/colour_tracker.py --source 0 --colour red
    python classic_cv/colour_tracker.py --demo          # synthetic video, no camera needed
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from vision_utils import Detection, FpsMeter, count_by_label, draw_detections, draw_hud  # noqa: E402

# HSV ranges (OpenCV hue runs 0-179). Red wraps around 0, so it has two ranges.
COLOUR_RANGES = {
    "red": [((0, 120, 70), (10, 255, 255)), ((170, 120, 70), (179, 255, 255))],
    "green": [((40, 70, 70), (85, 255, 255))],
    "blue": [((95, 120, 70), (130, 255, 255))],
}


def colour_mask(frame: np.ndarray, colour: str) -> np.ndarray:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = np.zeros(hsv.shape[:2], np.uint8)
    for lo, hi in COLOUR_RANGES[colour]:
        mask |= cv2.inRange(hsv, np.array(lo), np.array(hi))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # remove speckle noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # fill small holes
    return mask


def find_blobs(mask: np.ndarray, min_area: int = 300) -> list[tuple[int, int, int, int]]:
    """Bounding boxes (x1, y1, x2, y2) of every blob larger than min_area pixels."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for c in contours:
        if cv2.contourArea(c) < min_area:
            continue
        x, y, w, h = cv2.boundingRect(c)
        boxes.append((x, y, x + w, y + h))
    return sorted(boxes)


class CentroidTracker:
    """Gives each blob a stable ID by matching it to the nearest centroid from the last frame."""

    def __init__(self, max_jump: float = 60.0):
        self.max_jump = max_jump
        self.next_id = 0
        self.tracks: dict[int, tuple[int, int]] = {}

    def update(self, centres: list[tuple[int, int]]) -> list[int]:
        ids, unused = [], dict(self.tracks)
        new_tracks = {}
        for c in centres:
            best = min(unused.items(), key=lambda kv: math.dist(kv[1], c), default=None)
            if best and math.dist(best[1], c) <= self.max_jump:
                tid = best[0]
                del unused[tid]
            else:
                tid, self.next_id = self.next_id, self.next_id + 1
            new_tracks[tid] = c
            ids.append(tid)
        self.tracks = new_tracks
        return ids


def synthetic_frames(n: int = 120, size: tuple[int, int] = (480, 640)):
    """Two coloured discs moving across a grey background: a camera-free test video."""
    h, w = size
    for i in range(n):
        frame = np.full((h, w, 3), 90, np.uint8)
        cv2.circle(frame, (40 + 4 * i, 150), 30, (0, 0, 220), -1)          # red disc, left to right
        cv2.circle(frame, (w - 40 - 3 * i, 330), 35, (0, 0, 220), -1)      # red disc, right to left
        cv2.circle(frame, (320, 60 + 2 * i), 25, (200, 60, 0), -1)         # blue disc (ignored when tracking red)
        yield frame


def process(frame: np.ndarray, colour: str, tracker: CentroidTracker) -> list[Detection]:
    boxes = find_blobs(colour_mask(frame, colour))
    centres = [((x1 + x2) // 2, (y1 + y2) // 2) for x1, y1, x2, y2 in boxes]
    ids = tracker.update(centres)
    return [Detection(*b, cls_id=tid, label=f"{colour}#{tid}", conf=1.0) for b, tid in zip(boxes, ids)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default="0")
    ap.add_argument("--colour", choices=sorted(COLOUR_RANGES), default="red")
    ap.add_argument("--demo", action="store_true", help="use a synthetic video instead of a camera")
    ap.add_argument("--save", help="save the annotated video (mp4)")
    ap.add_argument("--headless", action="store_true", help="don't open a window")
    args = ap.parse_args()

    if args.demo:
        frames = synthetic_frames()
    else:
        cap = cv2.VideoCapture(int(args.source) if args.source.isdigit() else args.source)
        frames = iter(lambda: cap.read()[1], None)

    tracker, fps, writer = CentroidTracker(), FpsMeter(), None
    for frame in frames:
        dets = process(frame, args.colour, tracker)
        draw_detections(frame, dets)
        draw_hud(frame, fps.tick(), {args.colour: len(dets)})
        if args.save:
            if writer is None:
                h, w = frame.shape[:2]
                writer = cv2.VideoWriter(args.save, cv2.VideoWriter_fourcc(*"mp4v"), 30, (w, h))
            writer.write(frame)
        if not args.headless:
            cv2.imshow("colour tracker (q to quit)", frame)
            if cv2.waitKey(30) & 0xFF == ord("q"):
                break
    if writer:
        writer.release()
    if not args.headless:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
