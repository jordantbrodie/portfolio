import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "classic_cv"))

from colour_tracker import CentroidTracker, colour_mask, find_blobs, process, synthetic_frames  # noqa: E402
from vision_utils import Detection, FpsMeter, count_by_label, draw_detections  # noqa: E402


def test_finds_two_red_blobs_and_ignores_blue():
    frame = next(synthetic_frames())
    assert len(find_blobs(colour_mask(frame, "red"))) == 2
    assert len(find_blobs(colour_mask(frame, "blue"))) == 1


def test_tracker_keeps_ids_stable_while_objects_move():
    tracker, frames = CentroidTracker(), list(synthetic_frames(n=30))
    first = {d.label for d in process(frames[0], "red", tracker)}
    for f in frames[1:]:
        labels = {d.label for d in process(f, "red", tracker)}
    assert labels == first == {"red#0", "red#1"}


def test_tracker_assigns_new_id_after_a_big_jump():
    t = CentroidTracker(max_jump=50)
    assert t.update([(0, 0)]) == [0]
    assert t.update([(500, 500)]) == [1]


def test_count_and_draw():
    dets = [Detection(10, 10, 50, 50, 0, "purk", 0.97), Detection(60, 60, 90, 90, 1, "hiir", 0.88),
            Detection(5, 70, 30, 95, 0, "purk", 0.91)]
    assert count_by_label(dets) == {"purk": 2, "hiir": 1}
    img = np.zeros((100, 100, 3), np.uint8)
    draw_detections(img, dets)
    assert img.any()


def test_fps_meter():
    m = FpsMeter()
    for i in range(11):
        fps = m.tick(now=i * 0.1)
    assert abs(fps - 10.0) < 1e-6
