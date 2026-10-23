"""Run a trained YOLO model on a webcam, video file or image and draw the results with OpenCV.

Examples:
    python detect.py --weights runs/cans-and-mice/weights/best.pt --source 0        # webcam
    python detect.py --weights best.pt --source clip.mp4 --save out.mp4 --log log.csv
    python detect.py --weights best.pt --source desk.jpg --save desk_detected.jpg
"""
import argparse
import csv
from pathlib import Path

import cv2
from ultralytics import YOLO

from vision_utils import Detection, FpsMeter, count_by_label, draw_detections, draw_hud

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".bmp"}


def to_detections(result, min_conf: float) -> list[Detection]:
    out = []
    for box in result.boxes:
        conf = float(box.conf[0])
        if conf < min_conf:
            continue
        x1, y1, x2, y2 = (int(v) for v in box.xyxy[0])
        cls_id = int(box.cls[0])
        out.append(Detection(x1, y1, x2, y2, cls_id, result.names[cls_id], conf))
    return out


def run_image(model, path: str, min_conf: float, save: str | None) -> None:
    frame = cv2.imread(path)
    if frame is None:
        raise SystemExit(f"Could not read image {path}")
    dets = to_detections(model(frame, verbose=False)[0], min_conf)
    draw_detections(frame, dets)
    print(count_by_label(dets))
    if save:
        cv2.imwrite(save, frame)
    cv2.imshow("detections", frame)
    cv2.waitKey(0)


def run_stream(model, source, min_conf: float, save: str | None, log: str | None) -> None:
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise SystemExit(f"Could not open source {source!r}")
    writer = None
    log_file = open(log, "w", newline="") if log else None
    log_csv = csv.writer(log_file) if log_file else None
    if log_csv:
        log_csv.writerow(["frame", "label", "confidence", "x1", "y1", "x2", "y2"])

    fps_meter, frame_no = FpsMeter(), 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            dets = to_detections(model(frame, verbose=False)[0], min_conf)
            draw_detections(frame, dets)
            draw_hud(frame, fps_meter.tick(), count_by_label(dets))

            if log_csv:
                for d in dets:
                    log_csv.writerow([frame_no, d.label, f"{d.conf:.3f}", d.x1, d.y1, d.x2, d.y2])
            if save:
                if writer is None:
                    h, w = frame.shape[:2]
                    fps = cap.get(cv2.CAP_PROP_FPS) or 30
                    writer = cv2.VideoWriter(save, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
                writer.write(frame)

            cv2.imshow("detections (q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            frame_no += 1
    finally:
        cap.release()
        if writer:
            writer.release()
        if log_file:
            log_file.close()
        cv2.destroyAllWindows()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--weights", required=True, help="trained .pt file")
    ap.add_argument("--source", default="0", help="webcam index, video path or image path")
    ap.add_argument("--conf", type=float, default=0.5, help="minimum confidence to keep a box")
    ap.add_argument("--save", help="write the annotated output to this file")
    ap.add_argument("--log", help="write every detection to this CSV file")
    args = ap.parse_args()

    model = YOLO(args.weights)
    if Path(args.source).suffix.lower() in IMAGE_EXT:
        run_image(model, args.source, args.conf, args.save)
    else:
        source = int(args.source) if args.source.isdigit() else args.source
        run_stream(model, source, args.conf, args.save, args.log)


if __name__ == "__main__":
    main()
