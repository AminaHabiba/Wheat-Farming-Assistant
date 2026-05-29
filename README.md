# 🌾 AI-Powered Wheat Farming Assistant with Disease Detection

> **Final Year Project - BS Computer Science**

> University of Agriculture, Faisalabad (UAF)

> Submitted by: **Amina Habiba** (Batch 2022-2026)

> Supervisor: **Sir Dr. Ahsan Latif**

---

## 📌 Project Overview

An intelligent system that helps farmers detect wheat crop diseases from leaf images using **Digital Image Processing (DIP)** and **Deep Learning (CNN)**. The system classifies wheat leaves into 4 categories and provides treatment recommendations, preventive measures and general farming guidance.

The project also includes an **AI-Powered Chatbot** using Ollama + Llama3.2 that answers any wheat farming question locally without internet.

**Detected Diseases:**
- ✅ Healthy
- 🔴 Leaf Rust
- 🟡 Stripe Rust (Yellow Rust)
- ⚪ Powdery Mildew

---

## 📊 Model Performance

|      Metric     |             Value               |
|       ---       |              ---                |
|      Model      | MobileNetV2 (Transfer Learning) |
|   Val Accuracy  |           **93.55%**            |
|  Test Accuracy  |           **92.69%**            |
| Training Images |             2,978               |
|   Test Images   |              643                |
|  Total Dataset  |           4,257 images          |

---

## 🗂️ Project Structure

```bash
Wheat_Farming_Assistant/
├── dataset/                        # All image data
│   ├── raw/                        # Original images
│       ├── plantvillage_wheat/     # From PlantVillage dataset
│       └── local_field_photos/     # UAF farm photos
│   └── processed/                  # Preprocessed & split
│       ├── train/                  # 70% training
│       ├── val/                    # 15% validation
│       └── test/                   # 15% testing
│
├── notebooks/                      # Jupyter experiments
│   ├── 01_data_exploration.ipynb
│   ├── 02_image_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   ├── 04_model_evaluation.ipynb
│   └── 05_augmentation_test.ipynb
│
├── src/                            # Main source code
│   ├── preprocessing/              # DIP pipeline
│   ├── model/                      # CNN model
│   ├── recommendation/             # Disease advice
│   ├── chatbot/                    # AI chatbot
│   └── utils/                      # Helpers
│
├── backend/                        # Flask REST API
│   ├── app.py
│   ├── routes.py
│   ├── config.py
│   └── uploads/
├── frontend/                       # Streamlit UI
│   ├── app_streamlit.py            
│   └── assets/
├── saved_models/                   # Trained model
├── results/                        # Evaluation charts
├── docs/                           # Documentation
│   ├── screenshots/
│   ├── user_manual.md          
│   └── api_documentation.md    
├── main.py                         # Start everything
├── requirements.txt
└── README.md
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/AminaHabiba/wheat-farming-assistant.git
cd wheat-farming-assistant
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Ollama (for AI Chatbot)
Download from: https://ollama.com/download

Then pull the AI model:
```bash
ollama pull llama3.2:3b
```

### 4. Prepare Dataset
- Download wheat disease images from Kaggle
- Place in `dataset/raw/plantvillage_wheat/`
- Run `notebooks/02_image_preprocessing.ipynb`

### 5. Train Model (Already Done)
```bash
# Model already trained and saved
# Only run if retraining needed
jupyter notebook notebooks/03_model_training.ipynb
```
The trained model will be saved to `saved_models/wheat_disease_model.h5`

## 🚀 Running the Application

### ✅ One Command Start (Recommended)
```bash
python main.py
```

This automatically:
- ✅ Starts Ollama AI Model (port 11434)
- ✅ Starts Flask Backend (port 5000)
- ✅ Starts Streamlit Frontend (port 8501)
- ✅ Opens browser automatically
- ✅ Shows status of all services
- ✅ Press CTRL+C to stop everything

### Manual Start (if needed)
```bash
# Terminal 1
ollama serve

# Terminal 2
python backend/app.py

# Terminal 3
streamlit run frontend/app_streamlit.py
```

---

## 🧠 System Architecture
```
User uploads image
        ↓
Image Preprocessing (OpenCV DIP)
  → Resize & Normalize (224×224)
  → Noise Removal (Gaussian Filter)
  → Contrast Enhancement (CLAHE)
        ↓
CNN Disease Classification
  → MobileNetV2 (Transfer Learning)
  → 93.55% Validation Accuracy
  → Output:4 Disease Classes i.e Healthy / Leaf Rust / Stripe Rust / Powdery Mildew
        ↓
Recommendation Engine
  → Disease Info & Symptoms
  → Treatment & Fungicides
  → Fertilizer Advice
  → Farming Guidelines
        ↓
AI Chatbot (Ollama + Llama3.2)
  → Answers any farming question
  → Uses local knowledge base
  → No internet required
        ↓
Streamlit Web Interface
```

---

## 📊 Model Performance

| Metric    | Value        |
|-----------|--------------|
| Accuracy  | (to be updated after training) |
| Precision | (to be updated after training) |
| Recall    | (to be updated after training) |
| F1-Score  | (to be updated after training) |

Confusion matrix and accuracy/loss curves are saved in `results/`.

---

## 🛠️ Tools & Technologies

| Category        | Tools / Libraries                        |
|-----------------|------------------------------------------|
| Language        | Python 3.10+                             |
| DIP             | OpenCV, Pillow                           |
| Deep Learning   | TensorFlow 2.13, Keras                   |
| CNN Models      | MobileNetV2 (Transfer Learning)          |
| AI Chatbot      | Ollama + Llama3.2:3b                     |
| Backend         | Flask / Flask-CORS                       |
| Frontend        | Streamlit                                |
| IDE             | VS Code, Jupyter Notebook                |
| Version Control | Git, GitHub                              |

---

## 🤖 AI Chatbot Features

- Answers **any wheat farming question**
- Runs **completely offline** — no internet needed
- Uses **Llama3.2:3b** local AI model
- Reads Pakistan-specific knowledge base
- Remembers conversation history
- Suggested questions for quick access

**Example questions:**
- *"What is leaf rust?"*
- *"Which fungicide for stripe rust?"*
- *"When should I irrigate wheat?"*
- *"Best wheat varieties in Pakistan?"*

---

## 📋 API Documentation

Full API documentation available in:
`docs/api_documentation.md`

---

## 🌐 API Endpoints

| Method |  Endpoint   | Description                 |
|--------|-------------|-----------------------------|
| GET    | `/health`   | Check API status            |
| POST   | `/predict`  | Upload image, get disease   |
| GET    | `/classes`  | List disease classes        |
| GET    |`/model-info`| Model details               |


**Example POST request:**
```bash
curl -X POST http://localhost:5000/predict \
  -F "image=@wheat_leaf.jpg"
```

**Example response:**
```json
{
  "status": "success",
  "prediction": {
    "disease": "leaf_rust",
    "confidence": 93.74,
    "is_healthy": false,
    "message": "Leaf Rust detected..."
  },
  "recommendation": {
    "disease_info": {...},
    "treatment": {...},
    "fertilizer": {...}
  }
}
```
---
## 🌱 Future Enhancements

- Support for multiple crops
- IoT-based soil monitoring
- Drone-based image capture
- Voice assistant in Urdu/Punjabi for local farmers
- Mobile app (Android) version
- Weather-based disease prediction

---

## 📄 License

This project is developed for academic purposes at the
**University of Agriculture, Faisalabad**.
© 2026 Amina Habiba - All rights reserved.

---

## 👩‍💻 Developer

**Amina Habiba**
BS Computer Science
Batch: 2022-2026
University of Agriculture, Faisalabad
Supervisor: Dr. Ahsan Latif
Year: 2026 