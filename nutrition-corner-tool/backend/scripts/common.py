from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MASTER = DATA / "annotations_master"
IMG_WORK = DATA / "images_working"

def read_master():
    return [json.loads(p.read_text()) for p in sorted(MASTER.glob("*.json"))]

def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False))

def size(img_path: Path):
    with Image.open(img_path) as im:
        return im.width, im.height
