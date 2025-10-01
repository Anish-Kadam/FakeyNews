# main.py

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from PIL import Image
import pytesseract

app = FastAPI(
    title="FakeyNews API",
    description="Fake news detection backend",
    version="1.0"
)

# ----------------------------
# CORS configuration
# ----------------------------
origins = [
    "http://localhost:5173",   # Vite dev server
    "http://127.0.0.1:5173"    # Alternate local host
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Dummy ML model function
# ----------------------------
def predict_text(text: str):
    """
    Replace this function with your actual ML model prediction.
    For now, it returns 'fake' if 'fake' is in text, else 'real'.
    """
    text_lower = text.lower()
    if "fake" in text_lower:
        return "fake", 0.95
    else:
        return "real", 0.90

# ----------------------------
# Health check endpoint
# ----------------------------
@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"message": "API is running!"}

# ----------------------------
# Predict endpoint
# ----------------------------
@app.post("/predict")
async def predict(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
    
):
    """
    Predict fake/real news from text or image.
    - text: string input (optional)
    - file: image file input (optional)
    """

    # Ensure at least one input is provided
    if not text and not file:
        return {"error": "Please provide either 'text' or 'file'."}

    # If text is provided, use it
    if text:
        input_text = text

    # If file is provided, extract text using Tesseract
    elif file:
        try:
            image = Image.open(file.file)
            input_text = pytesseract.image_to_string(image)
            if not input_text.strip():
                return {"error": "OCR did not extract any text. Try a clearer image."}
        except Exception as e:
            return {"error": f"OCR processing failed: {str(e)}"}

    # Run prediction
    prediction, confidence = predict_text(input_text)

    # Return structured response
    return {
        "prediction": prediction,
        "confidence": confidence,
        "text_extracted": input_text
    }
