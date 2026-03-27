from pydantic import BaseModel, Field
from typing import Dict, Optional
from enum import Enum


class IrisClass(str, Enum):
    setosa = "setosa"
    versicolor = "versicolor"
    virginica = "virginica"


class PredictionInput(BaseModel):
    sepal_length: float = Field(..., gt=0, description="Longueur du sépale > 0")
    sepal_width: float = Field(..., gt=0, description="Largeur du sépale > 0")
    petal_length: float = Field(..., gt=0, description="Longueur du pétale > 0")
    petal_width: float = Field(..., gt=0, description="Largeur du pétale ≥ 0")

class PredictionOutput(BaseModel):
    prediction: IrisClass
    confidence: float = Field(..., gt=0, le=1, description="Confiance de la prédiction")
    probabilities: Dict[str, float]

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    accuracy: Optional[float] = None