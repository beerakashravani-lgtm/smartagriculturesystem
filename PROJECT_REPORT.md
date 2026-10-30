# COLLEGE MINI-PROJECT REPORT

## Project Title:
# SMART AGRICULTURE SYSTEM FOR SOIL HEALTH ANALYSIS, CROP RECOMMENDATION AND YIELD PREDICTION

---

### A Mini-Project Submitted in Partial Fulfillment of the Requirements for the Degree of
### Bachelor of Technology (B.Tech) / Master of Computer Applications (MCA)
**Department of Computer Science & Engineering / Information Technology**

---

## TABLE OF CONTENTS
1. Abstract
2. Introduction
3. Problem Statement
4. Existing System vs. Proposed System
5. Objectives
6. Scope of the Project
7. Methodology
8. System Architecture
9. Modules Description
10. Dataset Description
11. Data Preprocessing & Pipeline
12. Machine Learning Algorithms
13. Model Training
14. Model Evaluation & Benchmarking
15. Results & Discussion
16. Advantages & Benefits
17. Limitations
18. Future Scope
19. Conclusion
20. References

---

## 1. ABSTRACT
Agriculture constitutes the socio-economic backbone of developing economies, employing a substantial fraction of the rural workforce and sustaining national food security. Nevertheless, traditional agricultural decision-making relies largely on anecdotal experience, historical habits, and subjective observations. Consequently, farmers frequently suffer from mismatched crop selection, soil nutrient depletion due to uncalibrated fertilizer application, and inaccurate yield expectations.

This project introduces the **Smart Agriculture System for Soil Health Analysis, Crop Recommendation and Yield Prediction**, an end-to-end Machine Learning decision-support web application. The platform integrates three interconnected computational modules:
1. **Soil Health Analysis**: Diagnostic scoring of macronutrient concentrations (Nitrogen, Phosphorus, Potassium), soil pH reaction, and moisture content with categorization into *Healthy*, *Moderate*, and *Needs Improvement* classes accompanied by actionable agronomic corrective advice.
2. **Crop Recommendation**: Multi-class supervised classification benchmarking Decision Trees, Random Forests, K-Nearest Neighbors (KNN), and Support Vector Machines (SVM) across 22 crops, delivering high-confidence crop recommendations accompanied by explicit agronomic suitability reasoning.
3. **Crop Yield Prediction**: Multi-variable regression modeling using Linear Regression, Decision Tree Regressor, and Random Forest Regressor to forecast crop yield in Tonnes per Hectare and calculate total expected production and gross farm-gate revenue based on benchmark Minimum Support Prices (MSP).

The system is deployed via an interactive, modern Streamlit dashboard styled with agricultural aesthetics, Plotly interactive radar/gauge visualizations, and SQLite database audit persistence. Experimental evaluation reveals that the Random Forest Classifier achieves **97.50% test accuracy (97.52% F1-score)** on 22 crops, while the Random Forest Regressor achieves an **$R^2$ score of 0.9677 (RMSE 3.062)** for yield forecasting.

---

## 2. INTRODUCTION
Modern agriculture faces the multifaceted challenge of feeding an expanding global population under constraints of climate change, water scarcity, and land degradation. Precision Agriculture (PA) has emerged as an indispensable paradigm, leveraging information technology, sensor telemetry, and predictive modeling to ensure that crops and soils receive precisely what they require for optimum productivity.

Key components of agricultural success involve knowing:
1. The physiological and chemical state of the soil.
2. What crop variety is ecologically best aligned to the microclimate and soil nutrients.
3. The projected harvest volume to organize storage, logistics, credit, and marketing.

Machine learning offers significant potential in this domain due to its ability to extract complex non-linear relationships from multi-dimensional agro-climatic datasets. By bridging empirical agronomy and artificial intelligence, this project develops a practical, easy-to-demonstrate software artifact tailored for academic and operational demonstration.

---

## 3. PROBLEM STATEMENT
Traditional farming systems in developing regions exhibit several critical vulnerabilities:
- **Blind Fertilization**: Injudicious, unbalanced application of urea and synthetic fertilizers without soil testing causes soil acidification, groundwater eutrophication, and secondary micronutrient deficiencies.
- **Suboptimal Crop Selection**: Farmers frequently cultivate traditional monocultures or crops unsuited to their localized soil chemistry and rainfall patterns, leading to crop failure or depressed yields.
- **Unpredictable Harvest Forecasts**: Lack of quantitative pre-harvest yield estimation leaves farmers vulnerable to price volatility, post-harvest distress sales, and inadequate storage planning.
- **Accessibility Barriers**: Advanced agricultural analytics are often confined to expensive proprietary enterprise platforms inaccessible to smallholders, extension agents, and rural co-operatives.

---

## 4. EXISTING SYSTEM VS. PROPOSED SYSTEM

### 4.1 Existing System
- **Manual Soil Testing Laboratories (STLs)**: Soil samples sent to centralized laboratories take weeks to deliver paper reports, frequently after sowing deadlines have passed.
- **Heuristic / Rule-of-Thumb Guesswork**: Sowing decisions are dictated by ancestral tradition rather than scientific climate-soil matching.
- **Fragmented Tools**: Isolated calculators exist for single tasks (e.g., a simple fertilizer calculator) without end-to-end integration with crop suitability and harvest forecasting.

### 4.2 Proposed System
- **Instantaneous Web-Based Diagnosis**: Farmers and agronomists enter soil test figures and receive immediate diagnostic scoring and targeted remedies.
- **Multi-Algorithm AI Selection**: Evaluates several machine learning algorithms and selects the mathematically optimal model for 22 agricultural varieties.
- **Comprehensive Agronomic Justifications**: Provides transparent explanations ("Why is this crop suitable?") rather than treating AI as an opaque black box.
- **End-to-End Economic Integration**: Converts physical yield predictions (Tonnes/Ha) into tangible harvest volumes (Quintals/kg) and gross market valuation.
- **Zero-Cost Embedded Architecture**: Built completely on open-source Python, Scikit-learn, Streamlit, and SQLite.

---

## 5. OBJECTIVES
1. **Soil Diagnostic Engine**: Formulate an agronomic soil health scoring algorithm evaluating N, P, K, pH, moisture, and climatic factors against ICAR/FAO baselines.
2. **Predictive Crop Matching**: Train, benchmark, and deploy multi-class classifiers to recommend optimal crops among 22 choices based on 7 environmental variables.
3. **Yield & Revenue Forecasting**: Formulate regression models to predict crop yield (Tonnes/Ha) and estimate gross farm-gate income.
4. **Interactive Dashboard Development**: Create a modern, responsive web frontend with Plotly visualizations (radar charts, gauge meters, sensitivity analysis).
5. **Operational Audit Trail**: Integrate SQLite persistence for logging user queries, assessments, and predictions.

---

## 6. SCOPE OF THE PROJECT
- **Geographic Applicability**: Covers major tropical, subtropical, and temperate agro-climatic zones with data representations for cereals, pulses, fruits, commercial cash crops, and plantations.
- **Target Audience**: Agricultural students, researchers, rural extension officers, farmer collectives (FPOs), and smallholder farmers.
- **Operational Scope**: Desktop, tablet, and mobile web browser accessible via local network or cloud hosting.

---

## 7. METHODOLOGY
The system development follows a structured engineering workflow:
```
[Problem Formulation & Domain Research]
                │
                ▼
[Dataset Acquisition & Preprocessing]
                │
                ▼
[Feature Engineering & Normalization Pipeline]
                │
                ▼
[Model Training & Comparative Benchmarking]
                │
                ▼
[Model Serialization (Joblib) & Metric Auditing]
                │
                ▼
[Modular Application Logic Implementation (src/)]
                │
                ▼
[Streamlit Frontend Development & Plotly Integration]
                │
                ▼
[Automated Verification, Testing & Demonstration]
```

---

## 8. SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                       │
│        (Streamlit Web Dashboard + Custom CSS)           │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│               Data Preprocessing & Validation           │
│        (Range Checks, Sanitization, Transformers)       │
└────────────┬───────────────────────────────┬────────────┘
             │                               │
             ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│  Soil Health Evaluator  │     │   Scikit-Learn Models   │
│  - Agronomic Rules Engine│     │  - Random Forest Clf    │
│  - Parameter Diagnostics │     │  - Random Forest Reg    │
│  - Plotly Radar & Gauge │     │  - Label & Col Preproc  │
└────────────┬────────────┘     └────────────┬────────────┘
             │                               │
             └───────────────┬───────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│           Persistence Layer: SQLite Database            │
│   (soil_analysis_logs, crop_logs, yield_prediction_logs) │
└─────────────────────────────────────────────────────────┘
```

---

## 9. MODULES DESCRIPTION

### 9.1 Module 1: Soil Health Analysis
- **Inputs**: Available Nitrogen (N), Phosphorus (P), Potassium (K), Soil pH, Volumetric Soil Moisture (%), Ambient Temperature (°C), Humidity (%), Seasonal Rainfall (mm).
- **Processing**: Parameters are benchmarked against optimal ranges. Individual status indicators (Low, Deficient, Optimal, High, Excessive) are calculated. A weighted composite Soil Health Index (0-100) is generated.
- **Outputs**: Classification (*Healthy* [$\ge 78$], *Moderate* [$55-77$], *Needs Improvement* [$<55$]), Plotly radar comparison chart, Dual Gauge meters, deficiency alerts, and organic/chemical improvement advice.

### 9.2 Module 2: Crop Recommendation
- **Inputs**: Soil macronutrients (N, P, K), pH, and climate variables (temperature, humidity, rainfall).
- **Processing**: The input vector is fed to a trained Random Forest Classifier. `predict_proba` extracts class probabilities across all 22 candidate crops.
- **Outputs**: Top recommended crop with confidence score, 2nd and 3rd alternate crop suggestions, agronomic profile (crop category, water requirement, soil type, season), and justification narrative.

### 9.3 Module 3: Crop Yield Prediction
- **Inputs**: Selected Crop, Season, State/Zone, Farm Area (ha), Seasonal Rainfall (mm), Temperature (°C), Fertilizer Application (kg/ha), Pesticide Application (kg/ha).
- **Processing**: One-hot encoding of categorical variables, standard scaling of numerical variables, followed by Random Forest Regression.
- **Outputs**: Yield in Tonnes/Hectare, Total Expected Harvest (Tonnes, Quintals, kg), Estimated Gross Mandi/MSP Revenue (INR & USD), and dynamic sensitivity response curves.

### 9.4 Module 4: Model Performance & Benchmark Analytics
- **Features**: Visual comparative dashboards detailing performance of all tested models (Accuracy, Precision, Recall, F1 for classifiers; MAE, MSE, RMSE, $R^2$ for regressors).
- **Raw Data Explorer**: Interactive data tables displaying summary statistics and distributions.

### 9.5 Module 5: SQLite Database & Audit Logs
- Automatically persists all user transactions with timestamps. Provides interactive filtering and CSV export capabilities.

---

## 10. DATASET DESCRIPTION

### 10.1 Crop Recommendation Dataset (`crop_recommendation.csv`)
- **Total Records**: 2,200 rows.
- **Distribution**: 100 balanced records across each of 22 crops.
- **Features**:
  1. `N`: Nitrogen ratio in soil (0 - 140 kg/ha).
  2. `P`: Phosphorus ratio in soil (5 - 145 kg/ha).
  3. `K`: Potassium ratio in soil (5 - 205 kg/ha).
  4. `temperature`: Ambient temperature (8.8 - 43.7 °C).
  5. `humidity`: Relative humidity (14.3 - 99.8 %).
  6. `ph`: Soil pH (3.5 - 9.9).
  7. `rainfall`: Precipitation (20.2 - 298.6 mm).
  8. `label`: Target crop class (22 distinct crops).

### 10.2 Crop Yield Dataset (`yield_prediction.csv`)
- **Total Records**: 1,250 observations.
- **Features**:
  1. `Crop`: 15 commercial and food crops.
  2. `Season`: Kharif, Rabi, Summer, Whole Year.
  3. `State`: 10 major agricultural states.
  4. `Area_ha`: Landholding size in hectares.
  5. `Rainfall_mm`: Annual/seasonal precipitation.
  6. `Temperature_C`: Seasonal average temperature.
  7. `Fertilizer_kg_per_ha`: Application rate.
  8. `Pesticide_kg_per_ha`: Application rate.
  9. `Yield_tonnes_per_ha`: Continuous target variable.

---

## 11. DATA PREPROCESSING & PIPELINE
1. **Input Validation**: Bound validation prevents erroneous entries (e.g., negative rainfall, pH > 14).
2. **Missing Value Auditing**: Verified zero missing values across both datasets.
3. **Categorical Encoding**:
   - Label Encoding for 22 classification crop classes.
   - `OneHotEncoder(handle_unknown='ignore')` for yield features (`Crop`, `Season`, `State`).
4. **Feature Normalization**: `StandardScaler()` applied to numerical regressors to ensure zero mean and unit variance.
5. **ColumnTransformer Integration**: Packaging categorical encoders and numerical scalers into an integrated pipeline.

---

## 12. MACHINE LEARNING ALGORITHMS

### 12.1 Decision Tree Classifier & Regressor
- Non-parametric supervised method that recursively partitions the feature space using information gain (entropy / Gini impurity) or variance reduction.
- Offers intuitive interpretability but prone to high variance and overfitting.

### 12.2 Random Forest Classifier & Regressor
- Ensemble bagging algorithm constructing an uncorrelated forest of randomized decision trees.
- Reduces variance without increasing bias through bootstrap aggregating and random feature subspace selection.

### 12.3 K-Nearest Neighbors (KNN)
- Instance-based non-parametric classifier determining class membership based on majority vote of $k$ nearest Euclidean neighbors.

### 12.4 Support Vector Machine (SVM / SVC)
- Finds the optimal maximum-margin hyperplane separating classes in high-dimensional feature space using Radial Basis Function (RBF) kernel mapping.

### 12.5 Multiple Linear Regression
- Standard linear parametric baseline modeling target yield as a weighted linear combination of input predictors:
  $$Y = \beta_0 + \sum_{i=1}^{n} \beta_i X_i + \epsilon$$

---

## 13. MODEL TRAINING
- **Environment**: Python 3.11, Scikit-learn 1.9+, Pandas 3.0+.
- **Split Strategy**: 80% Training Split (1,760 samples for classification; 1,000 samples for regression), 20% Testing Split (440 samples for classification; 250 samples for regression).
- **Stratification**: Crop classes were stratified to maintain equal representation across train and test folds.

---

## 14. MODEL EVALUATION & BENCHMARKING

### 14.1 Classification Metrics
1. **Accuracy**:
   $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
2. **Precision**:
   $$\text{Precision} = \frac{TP}{TP + FP}$$
3. **Recall**:
   $$\text{Recall} = \frac{TP}{TP + FN}$$
4. **F1-Score**:
   $$\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

### 14.2 Regression Metrics
1. **Mean Absolute Error (MAE)**:
   $$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$
2. **Root Mean Squared Error (RMSE)**:
   $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$
3. **Coefficient of Determination ($R^2$)**:
   $$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$

---

## 15. RESULTS & DISCUSSION

### 15.1 Crop Recommendation Model Comparison
| Algorithm | Accuracy (%) | Precision (%) | Recall (%) | F1-Score (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest** | **97.50%** | **97.68%** | **97.50%** | **97.52%** |
| Support Vector Machine (SVC) | 95.91% | 96.18% | 95.91% | 95.97% |
| K-Nearest Neighbors (KNN) | 95.68% | 95.89% | 95.68% | 95.71% |
| Decision Tree | 92.95% | 93.18% | 92.95% | 92.98% |

*Discussion*: Random Forest outperformed single decision trees by 4.55% in accuracy due to ensemble variance reduction, effectively handling boundary overlaps between closely related pulse varieties (e.g., mungbean vs. mothbeans).

### 15.2 Crop Yield Model Comparison
| Algorithm | MAE | MSE | RMSE | R² Score |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest Regressor** | **1.590** | **9.376** | **3.062** | **0.9677** |
| Linear Regression | 1.866 | 11.109 | 3.333 | 0.9617 |
| Decision Tree Regressor | 1.923 | 16.785 | 4.097 | 0.9422 |

*Discussion*: The non-linear agronomic responses (such as diminishing yield returns from excessive fertilizers or waterlogging) were captured most effectively by the Random Forest Regressor ($R^2 = 0.9677$).

---

## 16. ADVANTAGES & BENEFITS
1. **Holistic Tri-Focal Approach**: Integrates soil testing, crop choice, and yield prediction into one workflow.
2. **Explainable AI (XAI)**: Provides human-readable agronomic justifications for every recommended crop.
3. **Economic Empowerment**: Converts abstract yield figures into anticipated gross rupee revenue based on current MSP rates.
4. **Actionable Remediation**: Offers practical advice (e.g., agricultural lime for acidic soil, gypsum for alkaline soil, organic compost).
5. **Lightweight & Rapid**: Runs locally with sub-second inference times without requiring GPU hardware.

---

## 17. LIMITATIONS
1. **Soil Depth & Texture**: Analysis is based on chemical topsoil attributes; subsoil compaction and drainage profiles are not directly modeled.
2. **Manual Weather Input**: The current prototype requires manual entry of climate parameters rather than automated GPS weather API fetching.
3. **Pest & Disease Dynamics**: Yield predictions assume standard pest control practices and do not simulate catastrophic pest infestations (e.g., locust attacks).

---

## 18. FUTURE SCOPE
1. **IoT Sensor Integration**: Deploying field sensor probes transmitting live telemetry over LoRaWAN or NB-IoT.
2. **Computer Vision Leaf Pathology**: Adding a mobile camera CNN model to detect leaf blights, rusts, and nutrient chlorosis.
3. **Automated Weather API Integration**: Auto-populating rainfall, temperature, and humidity based on farm geolocation.
4. **Multilingual Regionalization**: Localizing the interface into regional Indian languages (Hindi, Telugu, Marathi, Tamil, Kannada).

---

## 19. CONCLUSION
The **Smart Agriculture System for Soil Health Analysis, Crop Recommendation and Yield Prediction** successfully demonstrates how modern Machine Learning techniques can be applied to optimize agricultural productivity. By integrating soil diagnostics, classification models, and regression pipelines into an accessible, responsive web interface, the project bridges the gap between complex data science algorithms and practical farming needs. The high model performance (**97.50% classification accuracy** and **0.9677 regression $R^2$**) highlights the robustness of ensemble learning in agricultural modeling.

---

## 20. REFERENCES
1. Indian Council of Agricultural Research (ICAR), *Handbook of Agriculture: Facts and Figures for Farmers, Students, and all Interested in Farming*, ICAR Publications, New Delhi.
2. Food and Agriculture Organization (FAO), *Soil Nutrient Management and Fertilizer Use Guidelines*, FAO Agricultural Services Bulletins, Rome.
3. Pedregosa, F., et al., "Scikit-learn: Machine Learning in Python", *Journal of Machine Learning Research*, Vol. 12, pp. 2825–2830, 2011.
4. Breiman, L., "Random Forests", *Machine Learning*, Vol. 45, No. 1, pp. 5–32, 2001.
5. Ministry of Agriculture & Farmers Welfare, Government of India, *Agricultural Statistics at a Glance*, Directorate of Economics and Statistics.
