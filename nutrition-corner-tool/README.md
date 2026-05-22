# Nutrition Corner Tool (MVP)

Lokales Tool für:
- 4-Ecken-Labeling im Browser
- neutrales Master-Annotationsformat (JSON)
- Export für YOLO-Pose + Direct Regression
- Training/Prediction/Benchmark/Export als Scripts (MVP-Stubs)

## Struktur
Siehe `backend/data` und `backend/scripts` gemäß Zielstruktur.

## Schnellstart
```bash
cd nutrition-corner-tool
docker compose up --build
```

## Backend API
- `GET /api/images`
- `GET /api/images/{id}`
- `POST /api/annotations/{id}`
- `POST /api/annotations/{id}/approve`
- `POST /api/annotations/{id}/bad`
- `POST /api/predict/{id}`
- `POST /api/predict-batch`
- `POST /api/train/yolo-pose`
- `POST /api/train/direct-regression`
- `GET /api/train/status`
- `POST /api/benchmark`
- `POST /api/export/mobile`

## Master-Format
Annotationen liegen in `backend/data/annotations_master/*.json`.
`bbox_px` wird automatisch aus den 4 Ecken berechnet.

## Scripts
- `python backend/scripts/import_openfoodfacts.py`
- `python backend/scripts/dataset_validate.py`
- `python backend/scripts/export_yolo_pose.py`
- weitere Scripts als MVP-Stubs vorhanden.

## Hinweis
MVP priorisiert lokalen Workflow ohne Auth/Cloud/DB und mit klarer Trennung zwischen Frontend/Backend/Dataset/Training/Export.
