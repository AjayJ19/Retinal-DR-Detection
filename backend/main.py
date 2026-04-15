# ============================================================
#  RETINAL DR DETECTION — FASTAPI BACKEND
#  Run: uvicorn main:app --reload --port 8000
# ============================================================

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

from model import load_model, predict_and_gradcam
from suggestions import get_suggestions

# ==============================================================
# APP SETUP
# ==============================================================

app = FastAPI(
    title="Retinal DR Detection API",
    description="AI-powered diabetic retinopathy detection using EfficientNet-B4",
    version="2.0.0"
)

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================
# STARTUP — preload model
# ==============================================================

@app.on_event("startup")
async def startup():
    """Preload the model at server startup."""
    print("[Server] Preloading model...")
    load_model()
    print("[Server] Model ready!")


# ==============================================================
# ENDPOINTS
# ==============================================================

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "model": "EfficientNet-B4", "version": "2.0.0"}


@app.post("/api/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze a retinal fundus image for diabetic retinopathy.

    Accepts: JPG/PNG image upload
    Returns: DR grade, confidence, Grad-CAM heatmap, care suggestions
    """

    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image (JPG/PNG)")

    try:
        # Read image
        contents = await file.read()
        pil_image = Image.open(io.BytesIO(contents))

        # Run prediction + Grad-CAM
        result = predict_and_gradcam(pil_image)

        # Get built-in care suggestions
        suggestions = get_suggestions(result["grade"])

        return {
            **result,
            "suggestions": suggestions
        }

    except Exception as e:
        print(f"[Error] Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")



# ==============================================================
# MAIN
# ==============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
