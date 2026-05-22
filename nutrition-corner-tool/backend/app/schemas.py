from pydantic import BaseModel
from typing import Optional, Dict, List

class Point(BaseModel):
    x: float
    y: float

class Corners(BaseModel):
    top_left: Point
    top_right: Point
    bottom_right: Point
    bottom_left: Point

class SaveAnnotationRequest(BaseModel):
    corners_px: Corners
    status: str = "corrected"
    source: str = "manual"
    quality_score: Optional[float] = None
    notes: str = ""

class ImageItem(BaseModel):
    image_id: str
    filename: str
    status: str
    quality_score: Optional[float] = None
    annotation: Optional[Dict] = None
    prediction: Optional[Dict] = None

class TrainStatus(BaseModel):
    status: str = "idle"
    logs: List[str] = []
    latest_model_path: Optional[str] = None
