import time
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# Configure logging so errors print clearly in your Docker terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Enterprise AI Deployment & Cost Tracker")

try:
    logger.info("Initializing Hugging Face sentiment-analysis pipeline...")
    classifier = pipeline(
        "sentiment-analysis", 
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )
    logger.info("Model pipeline loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model pipeline: {str(e)}")
    classifier = None

class TextRequest(BaseModel):
    text: str

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "AI Cost Tracker Pipeline"}

@app.post("/predict")
def predict_sentiment(request: TextRequest):
    if classifier is None:
        raise HTTPException(status_code=500, detail="AI Model engine is offline.")
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        start_time = time.time()
        
        # Explicitly pass string into classifier to prevent matrix mapping errors
        model_output = classifier(str(request.text))
        
        end_time = time.time()
        latency = float(end_time - start_time)
        
        # Precise cloud infrastructure tracking math
        aws_cost_per_second = 0.085 / 3600.0
        computed_cost = float(latency * aws_cost_per_second)

        return {
            "text": request.text,
            "sentiment": model_output[0]["label"],
            "confidence": round(float(model_output[0]["score"]), 4),
            "metrics": {
                "execution_latency_seconds": round(latency, 4),
                "estimated_infrastructure_cost_usd": f"${computed_cost:.8f}"
            }
        }
    except Exception as e:
        logger.error(f"Prediction execution crash: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Runtime error: {str(e)}")
