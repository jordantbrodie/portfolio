"""Fine-tune a pretrained YOLO model on a Roboflow dataset export.

Usage:
    python train.py --data data.yaml --epochs 50 --model yolov8n.pt
"""
import argparse

from ultralytics import YOLO


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="data.yaml", help="dataset YAML (see data.yaml.example)")
    ap.add_argument("--model", default="yolov8n.pt", help="pretrained weights to start from")
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--device", default=None, help="'cpu', '0' for first GPU, or leave empty for auto")
    args = ap.parse_args()

    model = YOLO(args.model)
    model.train(data=args.data, epochs=args.epochs, imgsz=args.imgsz,
                device=args.device, project="runs", name="cans-and-mice")
    metrics = model.val()
    print(f"mAP50: {metrics.box.map50:.3f}   mAP50-95: {metrics.box.map:.3f}")


if __name__ == "__main__":
    main()
