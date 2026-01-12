"""
FastAPI backend for railway safety agent
Refactored with thin routes and service layer
"""
import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.models import SafetyInput, SafetyOutput
from backend.services import get_service, RiskAssessmentService
from backend.config import settings
from backend.ml_model import get_model

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Railway Safety Agent API",
    description="AI-powered railway safety risk assessment and alert system",
    version="1.0.0"
)

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize models and services on startup"""
    try:
        logger.info("Initializing Railway Safety Agent...")
        # Initialize model (will train if configured)
        model = get_model()
        logger.info(f"Model initialized: {model.model_type}")
        # Initialize service
        service = get_service()
        logger.info("Service initialized")
        logger.info("Railway Safety Agent ready")
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Railway Safety Agent API",
        "status": "operational",
        "version": "1.0.0",
        "model_type": settings.MODEL_TYPE
    }


@app.post("/assess-risk", response_model=SafetyOutput)
async def assess_risk(
    input_data: SafetyInput,
    service: RiskAssessmentService = Depends(get_service)
):
    """
    Main endpoint for risk assessment.
    Accepts safety parameters and returns risk classification with alerts and explainability.
    """
    try:
        logger.info(f"Risk assessment request: visibility={input_data.visibility}, "
                   f"speed={input_data.speed}, weather={input_data.weather}")
        
        # Delegate to service layer
        result = service.assess_risk(input_data)
        
        logger.info(f"Risk assessment completed: {result.risk_level}")
        return result
    
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing risk assessment: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="Internal server error processing risk assessment"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        model = get_model()
        return {
            "status": "healthy",
            "service": "railway-safety-agent",
            "model_trained": model.is_trained,
            "model_type": model.model_type
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.get("/model/info")
async def model_info():
    """Get model information"""
    try:
        model = get_model()
        return {
            "model_type": model.model_type,
            "is_trained": model.is_trained,
            "feature_importance": model.feature_importance_.tolist() if model.feature_importance_ is not None else None
        }
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
