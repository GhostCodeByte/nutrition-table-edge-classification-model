from common import read_master, IMG_WORK
errs=[]
for ann in read_master():
    img = IMG_WORK / ann['filename']
    if not img.exists(): errs.append((ann['image_id'],'missing_image'))
    for obj in ann.get('objects',[]):
        c = obj.get('corners_px',{})
        if any(k not in c for k in ['top_left','top_right','bottom_right','bottom_left']): errs.append((ann['image_id'],'missing_corner'))
print({'errors':errs,'count':len(errs)})
