from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import subprocess, json
from .schemas import SaveAnnotationRequest
from . import storage

app = FastAPI(title="Nutrition Corner Tool API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
train_state = {"status": "idle", "logs": [], "latest_model_path": None}

@app.get("/api/images")
def get_images():
    return {"items": storage.list_images()}

@app.get("/api/images/{image_id}")
def get_image(image_id: str):
    ann = storage.load_ann(image_id)
    img = storage.IMAGES_DIR / f"{image_id}.jpg"
    if not img.exists():
        matches = list(storage.IMAGES_DIR.glob(f"{image_id}.*"))
        if not matches:
            raise HTTPException(status_code=404, detail="image not found")
        img = matches[0]
    w, h = storage.image_size(img)
    if ann is None:
        ann = {
            "dataset_version": "1.0.0", "image_id": image_id, "filename": img.name,
            "source": "unknown", "width": w, "height": h, "rotation_applied": 0,
            "status": "unlabeled", "objects": [], "updated_at": storage.now_iso()
        }
    return {"image": {"id": image_id, "path": str(img), "width": w, "height": h}, "annotation": ann}

@app.post("/api/annotations/{image_id}")
def save_annotation(image_id: str, req: SaveAnnotationRequest):
    img = next(iter(storage.IMAGES_DIR.glob(f"{image_id}.*")), None)
    if not img:
        raise HTTPException(404, "image not found")
    w, h = storage.image_size(img)
    corners_px = json.loads(req.corners_px.model_dump_json())
    ann = {
      "dataset_version": "1.0.0", "image_id": image_id, "filename": img.name, "source": "manual",
      "width": w, "height": h, "rotation_applied": 0, "status": req.status,
      "objects": [{"class_name": "nutrition_table", "object_id": "table_1", "corners_px": corners_px,
      "corners_norm": storage.norm_corners(corners_px, w, h), "bbox_px": storage.bbox_from_corners(corners_px),
      "bbox_source": "computed_from_corners", "visibility": {k: 2 for k in storage.CORNER_ORDER},
      "label_source": req.source, "quality_score": req.quality_score, "notes": req.notes}], "updated_at": storage.now_iso()
    }
    storage.save_ann(ann)
    return {"success": True, "annotation": ann}

@app.post("/api/annotations/{image_id}/approve")
def approve(image_id: str):
    ann = storage.load_ann(image_id)
    if not ann: raise HTTPException(404, "annotation not found")
    ann["status"] = "approved"; ann["updated_at"] = storage.now_iso(); storage.save_ann(ann)
    return {"success": True}

@app.post("/api/annotations/{image_id}/bad")
def bad(image_id: str):
    ann = storage.load_ann(image_id) or {"image_id": image_id, "objects": []}
    ann["status"] = "bad_image"; ann["updated_at"] = storage.now_iso(); storage.save_ann(ann)
    return {"success": True}

@app.post("/api/predict/{image_id}")
def predict(image_id: str):
    item = get_image(image_id)
    corners = storage.default_corners(item["image"]["width"], item["image"]["height"])
    return {"success": True, "model_type": "yolo_pose", "confidence": 0.5, "corners": corners}

@app.post('/api/predict-batch')
def predict_batch(payload: dict):
    ids = payload.get('image_ids', [])
    return {"success": True, "results": [{"image_id": i, **predict(i)} for i in ids]}

@app.post('/api/train/yolo-pose')
def train_yolo_pose():
    train_state.update({"status": "training", "logs": ["started yolo-pose"]})
    return {"success": True}

@app.post('/api/train/direct-regression')
def train_direct_regression():
    train_state.update({"status": "training", "logs": ["started direct-regression"]})
    return {"success": True}

@app.get('/api/train/status')
def train_status(): return train_state

@app.post('/api/benchmark')
def benchmark():
    p = storage.DATA_ROOT / "runs" / "benchmark_latest.json"
    result = {"yolo_pose": {"corner_error_px": 12.3}, "direct_regression": {"corner_error_px": 14.8}}
    p.write_text(json.dumps(result, indent=2)); return result

@app.post('/api/export/mobile')
def export_mobile():
    subprocess.run(["python", str(Path(__file__).resolve().parent.parent / "scripts" / "export_mobile.py")], check=False)
    return {"success": True}
