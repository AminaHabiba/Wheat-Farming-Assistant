# API Documentation
## AI-Powered Wheat Farming Assistant

---

## Base URL
```bash
http://localhost:5000
```
---

## Endpoints

### GET /
Root endpoint - confirms API is running.

**Response:**
```json
{
  "status": "running",
  "message": "Welcome to AI-Powered Wheat Farming Assistant API",
  "developer": "Amina Habiba",
  "city": "Faisalabad",
  "university": "University of Agriculture, Faisalabad",
  "year": "2026"
}
```

---

### GET / health
Health check endpoint.

**Response:**
```json
{
  "status": "running",
  "model": "MobileNetV2",
  "classes": ["healthy", "leaf_rust", "stripe_rust", "powdery_mildew"],
  "version": "1.0"
}
```

---

### POST /predict
Upload wheat leaf image and get disease prediction.

**Request:** multipart/form-data
**Field:** image (JPG or PNG, max 10MB)

**Response:**
```json
{
  "status": "success",
  "prediction": {
    "disease": "leaf_rust",
    "confidence": 93.74,
    "is_healthy": false,
    "is_uncertain": false,
    "message": "Leaf Rust detected..."
  },
  "recommendation": {
    "disease_info": {},
    "treatment": {},
    "fertilizer": {}
  }
}
```

---

### GET /classes
Returns list of detectable disease classes.

---

### GET /model-info
Returns model performance details.
**Val Accuracy:** 93.55%
**Test Accuracy:** 92.69% 
