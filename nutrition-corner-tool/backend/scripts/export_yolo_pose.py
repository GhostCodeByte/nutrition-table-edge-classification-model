from common import read_master, DATA, write_json
from pathlib import Path

root = DATA / 'exports' / 'yolo_pose'
labels = root / 'labels'; labels.mkdir(parents=True, exist_ok=True)
for ann in read_master():
    if ann.get('status') not in {'corrected','approved'} or not ann.get('objects'): continue
    o = ann['objects'][0]
    b = o['bbox_px']; w,h = ann['width'],ann['height']
    cx=((b['x1']+b['x2'])/2)/w; cy=((b['y1']+b['y2'])/2)/h; bw=(b['x2']-b['x1'])/w; bh=(b['y2']-b['y1'])/h
    line=[0,cx,cy,bw,bh]
    for k in ['top_left','top_right','bottom_right','bottom_left']:
        p=o['corners_norm'][k]; line += [p['x'],p['y'],2]
    (labels / f"{ann['image_id']}.txt").write_text(" ".join(map(str,line))+"\n")
(root/'dataset.yaml').write_text("path: ./data/exports/yolo_pose\ntrain: images/train\nval: images/val\ntest: images/test\nkpt_shape: [4, 3]\nnames:\n  0: nutrition_table\n")
print('exported')
