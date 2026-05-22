"""Importiert lokale OpenFoodFacts-artige Bilder und erzeugt Master-JSON."""
from pathlib import Path
import json, shutil
from common import DATA, IMG_WORK, MASTER, size, write_json

src = DATA / "images_original"
for img in src.glob("*"):
    if img.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}: continue
    dst = IMG_WORK / img.name
    if not dst.exists(): shutil.copy2(img, dst)
    w, h = size(dst)
    image_id = dst.stem
    ann_file = MASTER / f"{image_id}.json"
    if ann_file.exists(): continue
    ann = {"dataset_version":"1.0.0","image_id":image_id,"filename":dst.name,"source":"openfoodfacts","width":w,"height":h,
           "rotation_applied":0,"status":"unlabeled","objects":[],"updated_at":""}
    write_json(ann_file, ann)
print("done")
