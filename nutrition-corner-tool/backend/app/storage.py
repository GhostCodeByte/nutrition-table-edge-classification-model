from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image

DATA_ROOT = Path(__file__).resolve().parent.parent / "data"
MASTER_DIR = DATA_ROOT / "annotations_master"
IMAGES_DIR = DATA_ROOT / "images_working"
RUNS_DIR = DATA_ROOT / "runs"

for p in [MASTER_DIR, IMAGES_DIR, RUNS_DIR]:
    p.mkdir(parents=True, exist_ok=True)

CORNER_ORDER = ["top_left", "top_right", "bottom_right", "bottom_left"]

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.width, im.height

def bbox_from_corners(corners_px: dict) -> dict:
    xs = [corners_px[k]["x"] for k in CORNER_ORDER]
    ys = [corners_px[k]["y"] for k in CORNER_ORDER]
    return {"x1": min(xs), "y1": min(ys), "x2": max(xs), "y2": max(ys)}

def norm_corners(corners_px: dict, width: int, height: int) -> dict:
    out = {}
    for k, p in corners_px.items():
        out[k] = {"x": p["x"] / width, "y": p["y"] / height}
    return out

def default_corners(width: int, height: int) -> dict:
    cx, cy = width / 2, height / 2
    w, h = width * 0.45, height * 0.35
    return {
        "top_left": {"x": cx - w / 2, "y": cy - h / 2},
        "top_right": {"x": cx + w / 2, "y": cy - h / 2},
        "bottom_right": {"x": cx + w / 2, "y": cy + h / 2},
        "bottom_left": {"x": cx - w / 2, "y": cy + h / 2},
    }

def ann_path(image_id: str) -> Path:
    return MASTER_DIR / f"{image_id}.json"

def load_ann(image_id: str) -> dict | None:
    p = ann_path(image_id)
    return json.loads(p.read_text()) if p.exists() else None

def save_ann(data: dict):
    ann_path(data["image_id"]).write_text(json.dumps(data, indent=2, ensure_ascii=False))

def list_images() -> list[dict]:
    out = []
    for p in sorted(IMAGES_DIR.glob("*")):
        if p.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        image_id = p.stem
        ann = load_ann(image_id)
        out.append({
            "image_id": image_id,
            "filename": p.name,
            "status": ann.get("status", "unlabeled") if ann else "unlabeled",
            "quality_score": ann.get("objects", [{}])[0].get("quality_score") if ann and ann.get("objects") else None,
            "annotation": ann,
            "prediction": ann.get("prediction") if ann else None,
        })
    return out
