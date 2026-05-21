AI-Powered Wheat Farming Assistant (Complete Project Structure)

Wheat_Farming_Assistant/            # Root Project Folder
├── dataset/                        # all images data
    ├── raw/                        # original downloaded images
        ├── plantvillage_wheat/     # from PlantVillage dataset
            ├── healthy/
            ├── leaf_rust/
            ├── stripe_rust/
            ├── powdery_mildew/
        ├── local_field_photos/     # UAF farm photos 
    ├── processed/                  # after preproocessing & split
        ├── train/                  # model training (70%)
            ├── healthy/
            ├── leaf_rust/
            ├── stripe_rust/
            ├── powdery_mildew/
        ├── val/                    # tuning and monitoring (15%)
            ├── healthy/
            ├── leaf_rust/
            ├── stripe_rust/
            ├── powdery_mildew/
        ├── test/                   # final evaluation (15%)
            ├── healthy/
            ├── leaf_rust/
            ├── stripe_rust/
            ├── powdery_mildew/

├── notebooks/                          # Jupyter/Colab Experiments
    └── 01_data_exploration.ipynb       # count images, visualize samples
    └── 02_image_preprocessing.ipynb    # OpenCV DIP steps
    └── 03_model_training.ipynb         # CNN fine-tuning, accuracy plots
    └── 04_model_evaluation.ipynb       # confusion matrix, F1, precision/recall
    └── 05_augmentation_test.ipynb      # test augmentation strategies

├── src/                            # Main python source code
    ├── preprocessing/              # DIP Pipeline
        └── __init__.py
        └── resize_normalize.py         # resize to 224×224, scale 0–1
        └── noise_removal.py            # Gaussian & median filter
        └── contrast_enhance.py         # CLAHE, histogram eq.
        └── segmentation.py             # Otsu threshold, Canny edge
        └── augmentation.py             # ImageDataGenerator setup
        └── pipeline.py                 # runs all steps in sequence
    ├── model/                      # CNN training & saving
        └── __init__.py
        └── build_model.py              # load MobileNet/VGG16, add top layers
        └── train.py                    # compile, fit, callbacks
        └── evaluate.py                 # accuracy, F1, confusion matrix
        └── predict.py                  # single image inference function
    ├── recommendation/             # Disease advice engine
        └── __init__.py
        └── disease_info.json           # causes, symptoms per disease
        └── treatment_data.json         # pesticide & preventive measures
        └── farming_tips.json           # fertilizer, irrigation, care tips
        └── recommender.py              # maps prediction → advice dict
    ├── chatbot/              
        └── __init__.py
        └── chatbot.py                  # local chatbot logic
    ├── utils/                          # helper functions
        └── __init__.py
        └── image_utils.py              # load, validate, convert images
        └── plot_utils.py               # plot accuracy curves, conf. matrix
        └── logger.py                   # logging setup

├── backend/                        # Flask REST API
    └── config.py                   # model path, allowed extensions
    └── routes.py                   # POST /predict, GET /health
    └── app.py                      # Flask app, routes definition
    ├── uploads/                    # temp storage for user images
        └── .gitkeep

├── frontend/                       # Web UI
    └── app_streamlit.py            # main Streamlit app
    ├── assets/                     # Images used in UI
        ├── disease_icons/
        └──  uaf_logo.png

├── saved_models/                   # trained model files
    └── wheat_disease_model.h5      # final trained CNN weights
    └── wheat_disease_model_v2.h5   # improved version
    └── model_architecture.json     # layer config (no weights)
    └── training_history.json       # accuracy & loss per epoch

├── results/                        # evaluation outputs
    └── classification_report.txt   # precision, recall, F1 per class

├── docs/                           # project documentation

└── main.py                         # Start everything
└── requirements.txt            
└── README.md                       # project overview & setup instructions
└── .gitignore                      # exclude dataset/, saved_models/, __pycache__/
└── run_backend.sh                  # bash script to start Flask server
└── run_frontend.sh                 # bash script to start Streamlit
