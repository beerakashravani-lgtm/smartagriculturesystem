# Smart Agriculture System for Soil Health Analysis, Crop Recommendation and Yield Prediction

An AI/ML-powered agricultural decision-support web application designed to evaluate soil health parameters, recommend the most suitable crops, and forecast harvest yield with economic valuation. Developed as a comprehensive B.Tech / MCA college mini-project using Python, Scikit-learn, Streamlit, and SQLite.

---

## 📌 Project Overview

Agriculture is vital to economic sustainability and food security. However, traditional farming often faces low crop productivity, imbalanced fertilizer application, soil degradation, and inaccurate harvest forecasting. 

The **Smart Agriculture System** provides a data-driven approach by synthesizing soil chemistry, ambient agro-climatic conditions, and management factors to deliver:
1. **Diagnostic Soil Health Analysis**: Rapid classification of soil fertility (Healthy, Moderate, Needs Improvement) with targeted chemical and organic corrective remedies.
2. **AI Crop Recommendation**: Predictive multi-class classification determining the best crop variety among 22 agricultural options, complete with suitability explanations and probability scores.
3. **Crop Yield Prediction**: Precision regression estimating expected crop output (Tonnes/Ha, Total Harvest Quintals/Tonnes) and gross farm-gate revenue based on MSP benchmarks.

---

## 🎯 Objectives
- Provide smallholder farmers, agronomists, and extension officers with an intuitive, accessible web dashboard.
- Prevent soil nutrient depletion by diagnosing macronutrient (N, P, K) and pH imbalances.
- Maximize agricultural yield and profitability by matching optimal crop varieties to localized soil and weather profiles.
- Maintain an audit trail of agricultural assessments using an embedded SQLite database.

---

## 🏗️ Project Architecture

```
smart-agriculture/
│
├── app.py                         # Main Streamlit web application & UI dashboard
├── requirements.txt               # Project library dependencies
├── README.md                      # Complete setup, usage & documentation guide
├── PROJECT_REPORT.md              # Academic B.Tech/MCA mini-project report
├── VIVA_QUESTIONS_AND_ANSWERS.md  # 25+ Comprehensive Viva exam Q&A
│
├── data/
│   ├── crop_recommendation.csv    # 2,200 samples across 22 crops (N, P, K, pH, climate)
│   ├── yield_prediction.csv       # 1,250 samples multi-crop agro-climatic yield dataset
│   └── agriculture.db             # Embedded SQLite database for historical logs
│
├── models/
│   ├── crop_model.pkl             # Trained Random Forest classifier
│   ├── label_encoder.pkl          # Target crop label encoder
│   ├── yield_model.pkl            # Trained Random Forest regressor
│   ├── yield_preprocessor.pkl     # ColumnTransformer (OneHot + StandardScaler)
│   └── metrics_summary.json       # Live JSON of genuine computed evaluation metrics
│
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py      # Input sanitation, range validation, bounds checking
│   ├── soil_analysis.py           # Soil health scoring, diagnostics, radar/gauge charts
│   ├── crop_recommendation.py     # Crop predictor, top-3 probabilities, agronomic reasoning
│   ├── yield_prediction.py        # Yield predictor, revenue estimation, sensitivity chart
│   └── db.py                      # SQLite database operations & query management
│
├── scripts/
│   ├── generate_datasets.py       # Dataset generation script for crop & yield data
│   └── train_models.py            # Automated training, benchmarking & serialization pipeline
│
├── notebooks/
│   └── model_training.ipynb       # Jupyter notebook documenting EDA & training
│
└── tests/
    └── test_pipeline.py           # Automated unit & integration tests
```

---

## 💻 Technologies Used

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit, HTML5, Vanilla CSS | Interactive, responsive web dashboard with emerald agricultural theme |
| **Visualizations** | Plotly Graph Objects, Express | Radar charts, gauge indicators, sensitivity graphs, and probability bars |
| **Machine Learning** | Scikit-learn (v1.9+) | Random Forest, Decision Trees, KNN, SVM, Linear Regression |
| **Data Processing** | Pandas, NumPy | Data cleaning, one-hot encoding, standard scaling, array transformations |
| **Model Persistence** | Joblib | Model and pipeline serialization (`.pkl`) |
| **Database** | SQLite 3 | Query audit logging for soil checks, crop queries, and yield runs |
| **Language** | Python 3.11 | Core application programming language |

---

## ⚙️ System Requirements
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: Version 3.9, 3.10, or 3.11
- **RAM**: Minimum 4 GB (8 GB recommended)
- **Disk Space**: ~500 MB free space

---

## 🚀 Installation & Setup Steps

### 1. Clone or Open the Project Directory
```bash
cd "shravani mini project"
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Re-generate Datasets and Retrain Models
Datasets and trained models are already bundled. If you wish to re-train from scratch:
```bash
python scripts/generate_datasets.py
python scripts/train_models.py
```

### 5. Run the Automated Test Suite
Verify that all modules, validations, and database connections work correctly:
```bash
python -m unittest tests/test_pipeline.py
```

### 6. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser and navigate to:
```
http://localhost:8501
```

---

## 📊 Dataset Details

### 1. Crop Recommendation Dataset (`data/crop_recommendation.csv`)
- **Records**: 2,200 samples (100 per crop class).
- **Target**: `label` (22 crops: *Rice, Maize, Chickpea, Kidneybeans, Pigeonpeas, Mothbeans, Mungbean, Blackgram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee*).
- **Features**:
  - `N` (Nitrogen content in soil): 0 to 140 kg/ha
  - `P` (Phosphorus content in soil): 5 to 145 kg/ha
  - `K` (Potassium content in soil): 5 to 205 kg/ha
  - `temperature`: 8 to 45 °C
  - `humidity`: 14 to 100%
  - `ph`: 3.5 to 9.5
  - `rainfall`: 20 to 300 mm

### 2. Crop Yield Prediction Dataset (`data/yield_prediction.csv`)
- **Records**: 1,250 multi-regional agro-climatic records.
- **Target**: `Yield_tonnes_per_ha` (Productivity in Tonnes/Hectare).
- **Features**:
  - `Crop`: Categorical (Rice, Wheat, Maize, Cotton, Sugarcane, Chickpea, Banana, etc.)
  - `Season`: Categorical (Kharif, Rabi, Summer, Whole Year)
  - `State`: Categorical (Punjab, Haryana, Uttar Pradesh, Maharashtra, Karnataka, etc.)
  - `Area_ha`: Landholding area in hectares (0.1 to 50 ha)
  - `Rainfall_mm`: Annual/seasonal precipitation (100 to 3,200 mm)
  - `Temperature_C`: Mean seasonal temperature (12 to 44 °C)
  - `Fertilizer_kg_per_ha`: Mineral fertilizer application (10 to 500 kg/ha)
  - `Pesticide_kg_per_ha`: Agrochemical pesticide dosage (0.2 to 25 kg/ha)

---

## 🏆 Model Benchmarking & True Calculated Metrics

The models were evaluated on an 80/20 train-test split using Scikit-learn:

### Classification (Crop Recommendation)
| Algorithm | Accuracy (%) | Precision (%) | Recall (%) | F1-Score (%) | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Random Forest** | **97.50%** | **97.68%** | **97.50%** | **97.52%** | **Selected & Deployed** |
| Support Vector Machine (SVC) | 95.91% | 96.18% | 95.91% | 95.97% | Benchmarked |
| K-Nearest Neighbors (KNN) | 95.68% | 95.89% | 95.68% | 95.71% | Benchmarked |
| Decision Tree | 92.95% | 93.18% | 92.95% | 92.98% | Benchmarked |

### Regression (Yield Prediction)
| Algorithm | MAE | MSE | RMSE | R² Score | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Random Forest Regressor** | **1.590** | **9.376** | **3.062** | **0.9677** | **Selected & Deployed** |
| Linear Regression | 1.866 | 11.109 | 3.333 | 0.9617 | Benchmarked |
| Decision Tree Regressor | 1.923 | 16.785 | 4.097 | 0.9422 | Benchmarked |

---

## 🧪 Sample Inputs and Expected Outputs

### Test Case 1: Alluvial Paddy Field (Rice)
- **Inputs**: N = 85 kg/ha, P = 48 kg/ha, K = 42 kg/ha, pH = 6.5, Moisture = 75%, Temp = 25 °C, Humidity = 82%, Rainfall = 225 mm.
- **Expected Soil Result**: Status = **Healthy** (Score: ~84/100). Balanced nutrients with slight nitrogen management advice.
- **Expected Crop Result**: **Rice (Paddy)** (Match Confidence: >90%). Alternate: Jute.
- **Expected Yield Result** (2.5 ha, Kharif, Punjab): Yield ≈ **3.8 Tonnes/Ha** | Total Harvest: **~9.5 Tonnes (95 Quintals)** | Revenue: **~₹2,09,000**.

### Test Case 2: Semi-Arid Cotton Land
- **Inputs**: N = 118 kg/ha, P = 46 kg/ha, K = 20 kg/ha, pH = 7.0, Moisture = 50%, Temp = 24.5 °C, Humidity = 78%, Rainfall = 82 mm.
- **Expected Soil Result**: Status = **Healthy / Moderate**.
- **Expected Crop Result**: **Cotton (White Gold)** (Match Confidence: >92%).
- **Expected Yield Result** (3.0 ha, Kharif, Maharashtra): Yield ≈ **2.2 Tonnes/Ha** | Total Harvest: **~6.6 Tonnes (66 Quintals)** | Revenue: **~₹4,36,000**.

---

## ⚠️ Limitations & Future Enhancements

### Limitations
1. **Micronutrient Omission**: Current soil evaluation focuses on primary N-P-K macronutrients and pH; secondary micronutrients (Zinc, Boron, Sulfur, Iron) are not yet integrated.
2. **Offline Climate Data**: The system currently uses manual farmer climate entries rather than live GPS-based weather API streaming.

### Future Enhancements
- **IoT Sensor Integration**: Interfacing ESP32/Arduino LoRaWAN soil probes for real-time telemetry.
- **Satellite Remote Sensing**: Integrating Sentinel-2 NDVI imagery to assess vegetative chlorophyll indices.
- **Multilingual Support**: Providing regional vernacular interfaces (Hindi, Telugu, Marathi, Tamil, Bengali).
- **Pest & Disease Vision Classifier**: Expanding with a Convolutional Neural Network (CNN) leaf disease scanner.
