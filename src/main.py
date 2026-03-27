from fastapi import FastAPI, HTTPException, status
import numpy as np
import logging
from src.models import PredictionInput, PredictionOutput, HealthResponse
from src.ml_utils import MLModel
from src.config import get_settings

settings = get_settings()

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="API de classification Iris",
    version="1.0.0"
)

model = MLModel(model_path="./models/model.pkl", report_path="./models/training_report.json")



@app.on_event("startup")
def load_model():
    try:
        model.load_model()
        logger.info("Modèle chargé avec succès")
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle : {e}")

@app.get("/health", response_model=HealthResponse)
def health():
    model_loaded = model.model is not None
    accuracy = model.get_accuracy()

    if not model_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modèle non chargé"
        )

    return HealthResponse(
        status="ok",
        model_loaded=model_loaded,
        accuracy=accuracy
    )

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    if model.model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modèle non chargé"
        )

    try:
        features = np.array([[
            input_data.sepal_length,
            input_data.sepal_width,
            input_data.petal_length,
            input_data.petal_width
        ]])

        prediction_class, confidence, probs_dict = model.predict(features)

        return PredictionOutput(
            prediction=prediction_class,
            confidence=confidence,
            probabilities=probs_dict
        )

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'inférence"
        )


@app.get("/info")
def info():
    if model.report is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Rapport non disponible"
        )

    try:
        report = model.report

        return {
            "accuracy": report.get("accuracy"),
            "f1_score": report.get("f1_score"),
            "recall_score": report.get("recall_score"),
            "precision_score": report.get("precision_score"),
            "date": report.get("date"),
        }

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des infos : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des métadonnées"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)