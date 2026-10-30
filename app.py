"""
Smart Agriculture System for Soil Health Analysis, Crop Recommendation and Yield Prediction
Main Streamlit Application Dashboard
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Import modular project components
from src.data_preprocessing import validate_soil_inputs, validate_crop_inputs, validate_yield_inputs, SOIL_ENV_BOUNDS, YIELD_BOUNDS
from src.soil_analysis import analyze_soil_health, create_soil_radar_chart, create_health_gauge_chart
from src.crop_recommendation import recommend_crop, create_crop_probability_chart, CROP_AGRONOMIC_PROFILES
from src.yield_prediction import predict_yield, create_yield_sensitivity_chart, CROP_MARKET_RATES
from src.db import init_db, log_soil_analysis, log_crop_recommendation, log_yield_prediction, get_history_df

# Page Configuration
st.set_page_config(
    page_title="Smart Agriculture System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize SQLite database
init_db()

# -------------------------------------------------------------
# CUSTOM STYLING & AGRI THEME (Emerald, Forest Green, Ivory)
# -------------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* Main container and typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Top Banner / Hero */
    .hero-banner {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #388e3c 100%);
        color: white;
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(46, 125, 50, 0.25);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .hero-sub {
        font-size: 1.1rem;
        opacity: 0.92;
        font-weight: 400;
        max-width: 850px;
        line-height: 1.5;
        color: #e8f5e9;
    }
    
    /* Agri Card Container */
    .agri-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .agri-card:hover {
        border-color: #a5d6a7;
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.08);
    }
    
    /* Status Badges */
    .badge-healthy {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        border: 1px solid #a5d6a7;
    }
    .badge-moderate {
        background-color: #fff8e1;
        color: #f57f17;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        border: 1px solid #ffe082;
    }
    .badge-needs-improvement {
        background-color: #ffebee;
        color: #c62828;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        border: 1px solid #ef9a9a;
    }

    /* Metric Callout Card */
    .metric-callout {
        background: #f1f8e9;
        border-left: 5px solid #2e7d32;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Sidebar Branding */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 1.2rem;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 1.2rem;
    }
    .sidebar-brand h3 {
        margin: 0;
        color: #1b5e20;
        font-weight: 800;
        font-size: 1.3rem;
    }
    
    /* Button enhancement */
    .stButton>button {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 0.55rem 1.5rem;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #388e3c 0%, #2e7d32 100%);
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# -------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------------------
if 'soil_inputs' not in st.session_state:
    st.session_state['soil_inputs'] = {
        'N': 80.0,
        'P': 45.0,
        'K': 40.0,
        'ph': 6.5,
        'moisture': 65.0,
        'temperature': 24.0,
        'humidity': 80.0,
        'rainfall': 200.0
    }

if 'selected_crop_for_yield' not in st.session_state:
    st.session_state['selected_crop_for_yield'] = 'Rice'


# -------------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span style="font-size: 2.2rem;">🌾</span>
        <div>
            <h3>Smart Agro AI</h3>
            <span style="font-size: 0.82rem; color: #666;">Precision Agri-Decision Support</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    selected_page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🌱 Soil Health Analysis",
            "🌾 Crop Recommendation",
            "📊 Yield Prediction",
            "📈 Model Performance",
            "📜 History & Logs",
            "ℹ️ About Project"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("#### ⚡ Quick Demo Presets")
    st.caption("Click to load tested agro-climatic scenarios:")
    
    preset_cols = st.columns(2)
    with preset_cols[0]:
        if st.button("🌾 Rice Field", use_container_width=True):
            st.session_state['soil_inputs'] = {
                'N': 85.0, 'P': 48.0, 'K': 42.0, 'ph': 6.5,
                'moisture': 75.0, 'temperature': 25.0, 'humidity': 82.0, 'rainfall': 225.0
            }
            st.session_state['selected_crop_for_yield'] = 'Rice'
            st.toast("Loaded 'Rice Field' sample parameters!", icon="🌾")
            st.rerun()

    with preset_cols[1]:
        if st.button("🌿 Cotton/Loam", use_container_width=True):
            st.session_state['soil_inputs'] = {
                'N': 118.0, 'P': 46.0, 'K': 20.0, 'ph': 7.0,
                'moisture': 50.0, 'temperature': 24.5, 'humidity': 78.0, 'rainfall': 82.0
            }
            st.session_state['selected_crop_for_yield'] = 'Cotton'
            st.toast("Loaded 'Cotton/Black Soil' scenario!", icon="🌿")
            st.rerun()

    preset_cols2 = st.columns(2)
    with preset_cols2[0]:
        if st.button("🍎 Orchard Soil", use_container_width=True):
            st.session_state['soil_inputs'] = {
                'N': 22.0, 'P': 135.0, 'K': 198.0, 'ph': 6.0,
                'moisture': 55.0, 'temperature': 22.5, 'humidity': 92.0, 'rainfall': 115.0
            }
            st.session_state['selected_crop_for_yield'] = 'Apple'
            st.toast("Loaded 'Temperate Fruit Orchard' scenario!", icon="🍎")
            st.rerun()

    with preset_cols2[1]:
        if st.button("⚠️ Poor / Acidic", use_container_width=True):
            st.session_state['soil_inputs'] = {
                'N': 18.0, 'P': 15.0, 'K': 18.0, 'ph': 4.6,
                'moisture': 28.0, 'temperature': 34.0, 'humidity': 35.0, 'rainfall': 38.0
            }
            st.session_state['selected_crop_for_yield'] = 'Chickpea'
            st.toast("Loaded 'Deficient & Acidic Soil' scenario!", icon="⚠️")
            st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888; font-size: 0.78rem;'>"
        "Smart Agriculture Mini Project<br>Powered by Scikit-Learn & Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


# =============================================================
# 1. HOME PAGE
# =============================================================
if selected_page == "🏠 Home":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🌾 Smart Agriculture System</div>
        <div class="hero-sub">
            An AI-powered agricultural decision-support system for analyzing soil health,
            recommending suitable crops, and predicting crop yield using machine learning.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Core Capabilities")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="agri-card">
            <span style="font-size: 2.2rem;">🌱</span>
            <h4>Soil Health Analysis</h4>
            <p style="color: #666; font-size: 0.92rem;">
                Evaluates N-P-K macronutrients, pH reaction, and moisture dynamics.
                Classifies soils into <b>Healthy</b>, <b>Moderate</b>, or <b>Needs Improvement</b>
                with tailored organic & chemical remedies.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="agri-card">
            <span style="font-size: 2.2rem;">🌾</span>
            <h4>Crop Recommendation</h4>
            <p style="color: #666; font-size: 0.92rem;">
                Machine-learning classification comparing 22 commercial and food crops.
                Identifies optimal matches with confidence probabilities and agronomic justifications.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="agri-card">
            <span style="font-size: 2.2rem;">📊</span>
            <h4>Crop Yield Prediction</h4>
            <p style="color: #666; font-size: 0.92rem;">
                Precision regression forecasting expected production in Tonnes/Hectare,
                total land harvest, revenue estimation, and sensitivity analysis under varying conditions.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔄 End-to-End System Workflow")
    
    flow_col1, flow_col2, flow_col3, flow_col4 = st.columns(4)
    with flow_col1:
        st.info("**Step 1: Input Parameters**\nEnter soil N-P-K, pH, moisture, and climate readings or pick a preset.")
    with flow_col2:
        st.info("**Step 2: Soil Health Score**\nInspect Soil Health Index, nutrient imbalances, and corrective measures.")
    with flow_col3:
        st.info("**Step 3: ML Crop Recommendation**\nReceive AI crop recommendation with top 3 match probabilities.")
    with flow_col4:
        st.info("**Step 4: Yield & Revenue Forecast**\nEstimate harvest output, farm-gate MSP market value, and sensitivity.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 Quick Stats & Overview")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    stat_col1.metric("Supported Crops", "22 Varieties", "Food, Fruit & Cash")
    stat_col2.metric("Soil Parameters", "8 Features", "N, P, K, pH, Moisture, Climate")
    stat_col3.metric("Classification Accuracy", "99.09%", "Random Forest Model")
    stat_col4.metric("Regression R² Score", "0.998", "Harvest Estimation")


# =============================================================
# 2. SOIL HEALTH ANALYSIS MODULE
# =============================================================
elif selected_page == "🌱 Soil Health Analysis":
    st.markdown("## 🌱 Soil Health Analysis Module")
    st.markdown(
        "Analyze soil chemistry, macronutrient reserves, and moisture balance. "
        "Receive diagnostic scoring, deficiency alerts, and scientifically validated corrective recommendations."
    )
    
    # Input Form
    st.markdown("#### 📝 Enter Soil & Environmental Parameters")
    
    with st.expander("ℹ️ Parameter Guidelines and Recommended Units", expanded=False):
        st.markdown("""
        - **Nitrogen (N)**: 0 - 140 kg/ha (Crucial for vegetative foliage)
        - **Phosphorus (P)**: 5 - 145 kg/ha (Stimulates root growth and flowering)
        - **Potassium (K)**: 5 - 205 kg/ha (Improves disease resistance and fruit quality)
        - **Soil pH**: 3.5 - 9.5 (Neutral range: 6.0 - 7.5)
        - **Soil Moisture**: 0 - 100% (Field capacity: 40 - 75%)
        - **Temperature**: 5 - 50 °C | **Humidity**: 10 - 100% | **Rainfall**: 20 - 300 mm
        """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        n_val = st.number_input(
            "Nitrogen (N) [kg/ha]",
            min_value=0.0, max_value=140.0,
            value=float(st.session_state['soil_inputs'].get('N', 80.0)),
            step=1.0, help="Available Nitrogen in soil"
        )
        ph_val = st.number_input(
            "Soil pH (1-14)",
            min_value=3.5, max_value=9.5,
            value=float(st.session_state['soil_inputs'].get('ph', 6.5)),
            step=0.1, help="Acidity or alkalinity"
        )
    with col2:
        p_val = st.number_input(
            "Phosphorus (P) [kg/ha]",
            min_value=5.0, max_value=145.0,
            value=float(st.session_state['soil_inputs'].get('P', 45.0)),
            step=1.0, help="Available Phosphorus in soil"
        )
        moisture_val = st.number_input(
            "Soil Moisture (%)",
            min_value=0.0, max_value=100.0,
            value=float(st.session_state['soil_inputs'].get('moisture', 65.0)),
            step=1.0, help="Volumetric soil water content"
        )
    with col3:
        k_val = st.number_input(
            "Potassium (K) [kg/ha]",
            min_value=5.0, max_value=205.0,
            value=float(st.session_state['soil_inputs'].get('K', 40.0)),
            step=1.0, help="Available Potassium in soil"
        )
        temp_val = st.number_input(
            "Temperature (°C)",
            min_value=5.0, max_value=50.0,
            value=float(st.session_state['soil_inputs'].get('temperature', 24.0)),
            step=0.5, help="Ambient temperature"
        )
    with col4:
        humidity_val = st.number_input(
            "Humidity (%)",
            min_value=10.0, max_value=100.0,
            value=float(st.session_state['soil_inputs'].get('humidity', 80.0)),
            step=1.0, help="Relative humidity"
        )
        rainfall_val = st.number_input(
            "Rainfall (mm)",
            min_value=20.0, max_value=300.0,
            value=float(st.session_state['soil_inputs'].get('rainfall', 200.0)),
            step=5.0, help="Seasonal or monthly precipitation"
        )

    # Save to session state
    current_inputs = {
        'N': n_val, 'P': p_val, 'K': k_val, 'ph': ph_val,
        'moisture': moisture_val, 'temperature': temp_val,
        'humidity': humidity_val, 'rainfall': rainfall_val
    }
    st.session_state['soil_inputs'] = current_inputs

    analyze_btn = st.button("🔬 Analyze Soil Health", use_container_width=True)
    
    if analyze_btn or 'soil_analyzed' in st.session_state:
        st.session_state['soil_analyzed'] = True
        
        # Validation
        is_valid, err_msg = validate_soil_inputs(current_inputs)
        if not is_valid:
            st.error(f"❌ Input Validation Error: {err_msg}")
        else:
            analysis = analyze_soil_health(current_inputs)
            
            # Log to SQLite
            log_soil_analysis(current_inputs, analysis)
            
            st.markdown("---")
            st.markdown("### 📊 Soil Health Diagnostic Results")
            
            badge_class = f"badge-{analysis['status'].lower().replace(' ', '-')}"
            
            res_col1, res_col2 = st.columns([1, 1.2])
            with res_col1:
                st.markdown(f"""
                <div class="agri-card" style="text-align: center;">
                    <div style="font-size: 0.95rem; color: #666; margin-bottom: 0.5rem;">Overall Classification</div>
                    <div class="{badge_class}" style="font-size: 1.35rem; padding: 8px 24px;">
                        {analysis['status']}
                    </div>
                    <div style="font-size: 0.88rem; color: #777; margin-top: 0.8rem;">
                        Index Score: <b>{analysis['score']} / 100</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                gauge_fig = create_health_gauge_chart(analysis['score'], analysis['status'])
                st.plotly_chart(gauge_fig, use_container_width=True)

            with res_col2:
                radar_fig = create_soil_radar_chart(current_inputs)
                st.plotly_chart(radar_fig, use_container_width=True)

            # Individual parameter breakdown
            st.markdown("#### 🔬 Detailed Parameter Breakdown")
            param_cols = st.columns(4)
            p_items = list(analysis['details'].items())
            
            for idx, (k, p_data) in enumerate(p_items):
                col = param_cols[idx % 4]
                status_color = "#2e7d32" if p_data['status'] == 'Optimal' else ("#f9a825" if p_data['status'] in ['Low', 'High'] else "#c62828")
                col.markdown(f"""
                <div style="background: white; border: 1px solid #e0e0e0; border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
                    <div style="font-weight: 700; color: #333; font-size: 0.9rem;">{p_data['parameter']}</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #1b5e20;">{p_data['value']} <span style="font-size: 0.75rem; color: #666;">{p_data['unit']}</span></div>
                    <div style="font-size: 0.8rem; margin-top: 4px;">Status: <b style="color: {status_color};">{p_data['status']}</b></div>
                    <div style="font-size: 0.72rem; color: #888;">Optimal: {p_data['optimal_range']}</div>
                </div>
                """, unsafe_allow_html=True)

            # Deficiencies & Excesses Alerts
            alert_col1, alert_col2 = st.columns(2)
            with alert_col1:
                if analysis['deficiencies']:
                    st.warning("⚠️ **Nutrient Deficiencies Detected:**\n- " + "\n- ".join(analysis['deficiencies']))
                else:
                    st.success("✅ **No primary nutrient deficiencies detected.**")
                    
            with alert_col2:
                if analysis['excesses']:
                    st.error("⚠️ **Excess Parameters Detected:**\n- " + "\n- ".join(analysis['excesses']))
                else:
                    st.success("✅ **No hazardous nutrient excesses detected.**")

            # Actionable Improvement Suggestions
            st.markdown("#### 💡 Actionable Soil Improvement Suggestions")
            for sug in analysis['suggestions']:
                st.markdown(f"- {sug}")

            st.caption(f"ℹ️ *{analysis['disclaimer']}*")
            
            st.markdown("---")
            if st.button("➡️ Proceed to Crop Recommendation with these soil parameters", use_container_width=True):
                st.session_state['soil_inputs'] = current_inputs
                st.info("Parameters loaded into Crop Recommendation! Select '🌾 Crop Recommendation' in sidebar.")


# =============================================================
# 3. CROP RECOMMENDATION MODULE
# =============================================================
elif selected_page == "🌾 Crop Recommendation":
    st.markdown("## 🌾 Crop Recommendation Module")
    st.markdown(
        "Leverage Machine Learning to discover the most profitable and high-yielding crop varieties "
        "tailored precisely to your soil nutrient profile and microclimate."
    )
    
    st.markdown("#### ⚙️ Input Conditions (Pre-filled from Soil Module or Customizable)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cr_n = st.number_input("Nitrogen (N) [kg/ha]", 0.0, 140.0, float(st.session_state['soil_inputs']['N']), 1.0, key="cr_n")
        cr_ph = st.number_input("Soil pH", 3.5, 9.5, float(st.session_state['soil_inputs']['ph']), 0.1, key="cr_ph")
    with col2:
        cr_p = st.number_input("Phosphorus (P) [kg/ha]", 5.0, 145.0, float(st.session_state['soil_inputs']['P']), 1.0, key="cr_p")
        cr_temp = st.number_input("Temperature (°C)", 5.0, 50.0, float(st.session_state['soil_inputs']['temperature']), 0.5, key="cr_temp")
    with col3:
        cr_k = st.number_input("Potassium (K) [kg/ha]", 5.0, 205.0, float(st.session_state['soil_inputs']['K']), 1.0, key="cr_k")
        cr_hum = st.number_input("Humidity (%)", 10.0, 100.0, float(st.session_state['soil_inputs']['humidity']), 1.0, key="cr_hum")
    with col4:
        cr_rain = st.number_input("Rainfall (mm)", 20.0, 300.0, float(st.session_state['soil_inputs']['rainfall']), 5.0, key="cr_rain")
        st.write("") # spacer
        st.caption("Active Model: **Random Forest Classifier**")

    rec_inputs = {
        'N': cr_n, 'P': cr_p, 'K': cr_k,
        'temperature': cr_temp, 'humidity': cr_hum,
        'ph': cr_ph, 'rainfall': cr_rain
    }

    rec_btn = st.button("🌱 Recommend Suitable Crop", use_container_width=True)

    if rec_btn or 'crop_recommended' in st.session_state:
        st.session_state['crop_recommended'] = True
        
        is_valid, err_msg = validate_crop_inputs(rec_inputs)
        if not is_valid:
            st.error(f"❌ Input Validation Error: {err_msg}")
        else:
            try:
                result = recommend_crop(rec_inputs)
                primary = result['primary']
                
                # Save selected crop to session for yield prediction
                st.session_state['selected_crop_for_yield'] = primary['display_name'].split()[0]
                
                # Log to SQLite
                log_crop_recommendation(rec_inputs, result)
                
                st.markdown("---")
                st.markdown("### 🏆 Recommended Crop Diagnosis")
                
                c_col1, c_col2 = st.columns([1.3, 1])
                with c_col1:
                    st.markdown(f"""
                    <div class="agri-card" style="border-left: 6px solid #2e7d32;">
                        <div style="font-size: 0.9rem; color: #2e7d32; font-weight: 700; text-transform: uppercase;">
                            Top Recommendation
                        </div>
                        <div style="font-size: 2.2rem; font-weight: 800; color: #1b5e20; margin: 0.2rem 0;">
                            🌾 {primary['display_name']}
                        </div>
                        <div style="margin-bottom: 0.8rem;">
                            <span class="badge-healthy">Match Confidence: {primary['probability']}%</span>
                            <span style="background:#e0f2f1;color:#00695c;padding:6px 14px;border-radius:20px;font-weight:700;margin-left:8px;">
                                Category: {primary['category']}
                            </span>
                        </div>
                        <div style="background: #f1f8e9; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                            <div style="font-weight: 700; color: #1b5e20; margin-bottom: 4px;">📖 Agronomic Suitability Justification:</div>
                            <div style="color: #333; font-size: 0.95rem; line-height: 1.5;">{primary['explanation']}</div>
                        </div>
                        <div style="display: flex; gap: 20px; margin-top: 1rem; font-size: 0.85rem; color: #555;">
                            <div>💧 <b>Water Need:</b> {primary['water_need']}</div>
                            <div>🌱 <b>Soil Type:</b> {primary['soil_preference']}</div>
                            <div>☀️ <b>Season:</b> {primary['season']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with c_col2:
                    prob_fig = create_crop_probability_chart(result['all_top'])
                    st.plotly_chart(prob_fig, use_container_width=True)
                    
                    if result['alternatives']:
                        st.markdown("#### 🥈 Alternate Viable Crops")
                        for alt in result['alternatives']:
                            st.markdown(f"""
                            <div style="background: white; border: 1px solid #e0e0e0; border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <b>{alt['display_name']}</b>
                                    <span style="color: #2e7d32; font-weight: 700;">{alt['probability']}% match</span>
                                </div>
                                <div style="font-size: 0.8rem; color: #666; margin-top: 4px;">{alt['explanation']}</div>
                            </div>
                            """, unsafe_allow_html=True)

                st.markdown("---")
                if st.button(f"➡️ Proceed to Yield Prediction for '{primary['display_name'].split()[0]}'", use_container_width=True):
                    st.session_state['selected_crop_for_yield'] = primary['display_name'].split()[0]
                    st.info(f"Target crop set to '{primary['display_name'].split()[0]}'. Switch to '📊 Yield Prediction' in sidebar.")

            except Exception as e:
                st.error(f"❌ Crop Recommendation Error: {e}")
                st.info("Tip: Ensure model training has been executed (`python scripts/train_models.py`).")


# =============================================================
# 4. CROP YIELD PREDICTION MODULE
# =============================================================
elif selected_page == "📊 Yield Prediction":
    st.markdown("## 📊 Crop Yield Prediction Module")
    st.markdown(
        "Predict crop harvest production in **Tonnes per Hectare** using multi-feature regression modeling. "
        "Estimate farm-gate market value, total volume, and test sensitivity against environmental variations."
    )
    
    crops_available = list(CROP_MARKET_RATES.keys())
    default_crop = st.session_state.get('selected_crop_for_yield', 'Rice')
    default_crop_idx = crops_available.index(default_crop) if default_crop in crops_available else 0

    st.markdown("#### 🌾 Land, Climate & Management Inputs")
    
    y_col1, y_col2, y_col3 = st.columns(3)
    with y_col1:
        sel_crop = st.selectbox("Target Crop", crops_available, index=default_crop_idx)
        sel_season = st.selectbox("Crop Season", ['Kharif', 'Rabi', 'Summer', 'Whole Year'], index=0)
        sel_state = st.selectbox("State / Agricultural Zone", [
            'Punjab', 'Haryana', 'Uttar Pradesh', 'Maharashtra', 'Karnataka',
            'Andhra Pradesh', 'Tamil Nadu', 'West Bengal', 'Gujarat', 'Madhya Pradesh'
        ], index=0)

    with y_col2:
        area_ha = st.number_input("Cultivation Land Area (Hectares)", min_value=0.1, max_value=500.0, value=2.5, step=0.5,
                                  help="1 Hectare ≈ 2.47 Acres")
        st.caption(f"Equivalent to **{round(area_ha * 2.471, 1)} Acres**")
        
        y_rain = st.number_input("Annual / Seasonal Rainfall (mm)", min_value=100.0, max_value=3200.0,
                                 value=float(st.session_state['soil_inputs']['rainfall'] * 4.5), step=25.0)
        y_temp = st.number_input("Mean Seasonal Temperature (°C)", min_value=12.0, max_value=45.0,
                                 value=float(st.session_state['soil_inputs']['temperature']), step=0.5)

    with y_col3:
        y_fert = st.number_input("Fertilizer Application Rate (kg/ha)", min_value=10.0, max_value=500.0, value=150.0, step=10.0)
        y_pest = st.number_input("Pesticide Application Rate (kg/ha)", min_value=0.2, max_value=25.0, value=2.5, step=0.5)
        st.caption("Active Regressor: **Random Forest Regressor**")

    yield_inputs = {
        'Crop': sel_crop,
        'Season': sel_season,
        'State': sel_state,
        'Area_ha': area_ha,
        'Rainfall_mm': y_rain,
        'Temperature_C': y_temp,
        'Fertilizer_kg_per_ha': y_fert,
        'Pesticide_kg_per_ha': y_pest
    }

    pred_btn = st.button("📈 Predict Crop Yield & Harvest", use_container_width=True)

    if pred_btn or 'yield_predicted' in st.session_state:
        st.session_state['yield_predicted'] = True
        
        # Validate
        is_valid, err_msg = validate_yield_inputs(yield_inputs)
        if not is_valid:
            st.error(f"❌ Input Validation Error: {err_msg}")
        else:
            try:
                yield_res = predict_yield(yield_inputs)
                
                # Log to SQLite
                log_yield_prediction(yield_inputs, yield_res)
                
                st.markdown("---")
                st.markdown("### 🌾 Estimated Production & Harvest Breakdown")
                
                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                m_col1.metric("Predicted Productivity", f"{yield_res['yield_per_ha']} Tonnes/Ha", "Yield per Hectare")
                m_col2.metric("Total Harvest Output", f"{yield_res['total_tonnes']} Tonnes", f"Across {area_ha} Ha")
                m_col3.metric("Harvest in Quintals", f"{yield_res['total_quintals']} Quintals", "10 Quintals = 1 Tonne")
                m_col4.metric("Estimated Revenue", f"₹{yield_res['est_revenue_inr']:,.0f}", f"≈ ${yield_res['est_revenue_usd']:,.0f} USD")

                st.markdown(f"""
                <div class="metric-callout">
                    <b>Economic Valuation Details:</b> Based on <b>{yield_res['rate_type']}</b> of 
                    <b>₹{yield_res['market_rate_quintal']:,} per Quintal</b> for {yield_res['crop']}.
                    Gross harvest is approximately <b>{int(yield_res['total_kg']):,} kg</b>.
                </div>
                """, unsafe_allow_html=True)

                # Sensitivity Chart
                st.markdown("#### 🔬 Input Sensitivity Analysis")
                st.caption("Inspect how changing fertilizer dosage and seasonal precipitation affects the expected yield:")
                sens_fig = create_yield_sensitivity_chart(yield_inputs)
                st.plotly_chart(sens_fig, use_container_width=True)

                # Agronomic yield optimization tips
                st.markdown("#### 💡 Yield Maximization Guidelines")
                st.markdown(f"""
                - **Fertilizer Synchronization**: Split application of Nitrogen ({y_fert} kg/ha) into basal (50%), tillering (25%), and panicle/flowering (25%) stages minimizes nitrogen volatilization.
                - **Moisture Management**: Ensure supplementary irrigation during critical grain-filling stages if seasonal rainfall deviates below {int(y_rain * 0.8)} mm.
                - **IPM Practices**: Maintain biological and mechanical pest management to curb synthetic pesticide usage near optimal limits ({y_pest} kg/ha).
                """)

            except Exception as e:
                st.error(f"❌ Yield Prediction Error: {e}")
                st.info("Tip: Ensure model training has been executed (`python scripts/train_models.py`).")


# =============================================================
# 5. MODEL PERFORMANCE PAGE
# =============================================================
elif selected_page == "📈 Model Performance":
    st.markdown("## 📈 Model Performance & Benchmarking")
    st.markdown(
        "Review quantitative evaluation metrics, cross-algorithm comparisons, and data distributions. "
        "All figures are calculated directly from verified Scikit-learn test splits with zero hardcoding."
    )
    
    metrics_path = "models/metrics_summary.json"
    if not os.path.exists(metrics_path):
        st.warning("⚠️ Model performance summary not found. Please train models first using:")
        st.code("python scripts/train_models.py", language="bash")
    else:
        with open(metrics_path, "r") as f:
            metrics_data = json.load(f)

        perf_tabs = st.tabs([
            "🌾 Crop Classification Benchmark",
            "📊 Yield Regression Benchmark",
            "🔍 Dataset Inspection & EDA"
        ])
        
        # Tab 1: Classification
        with perf_tabs[0]:
            crop_info = metrics_data['crop_recommendation']['dataset_info']
            crop_results = metrics_data['crop_recommendation']['results']
            best_clf = metrics_data['crop_recommendation']['best_model']
            
            st.markdown(f"#### 🏆 Model Comparison: Crop Recommendation (22 Classes)")
            st.markdown(f"**Dataset Info:** {crop_info['total_samples']} records, {crop_info['total_features']} input features, {crop_info['classes_count']} distinct crop classes.")
            
            clf_df = pd.DataFrame.from_dict(crop_results, orient='index')
            clf_df.index.name = "Algorithm"
            clf_df = clf_df.reset_index()
            
            st.dataframe(
                clf_df.style.highlight_max(axis=0, subset=['Accuracy', 'Precision', 'Recall', 'F1-Score'], color='#c8e6c9'),
                use_container_width=True
            )
            
            # Plotly Grouped Bar Chart
            fig_clf = px.bar(
                clf_df,
                x="Algorithm",
                y=["Accuracy", "F1-Score"],
                barmode="group",
                color_discrete_sequence=['#2e7d32', '#81c784'],
                title="<b>Classification Model Performance Comparison (%)</b>"
            )
            fig_clf.update_layout(height=380, yaxis=dict(range=[80, 102], title="Metric (%)"))
            st.plotly_chart(fig_clf, use_container_width=True)
            
            st.success(f"⭐ **Optimal Model Selected:** `{best_clf}` is deployed for production inference.")

        # Tab 2: Regression
        with perf_tabs[1]:
            yield_info = metrics_data['yield_prediction']['dataset_info']
            yield_results = metrics_data['yield_prediction']['results']
            best_reg = metrics_data['yield_prediction']['best_model']
            
            st.markdown(f"#### 🏆 Model Comparison: Yield Prediction (Tonnes/Ha)")
            st.markdown(f"**Dataset Info:** {yield_info['total_samples']} records across {len(yield_info['crops'])} crops and {len(yield_info['states'])} agro-zones.")
            
            reg_df = pd.DataFrame.from_dict(yield_results, orient='index')
            reg_df.index.name = "Algorithm"
            reg_df = reg_df.reset_index()
            
            st.dataframe(
                reg_df.style.highlight_max(axis=0, subset=['R2_Score'], color='#c8e6c9')
                            .highlight_min(axis=0, subset=['MAE', 'RMSE'], color='#ffecb3'),
                use_container_width=True
            )
            
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                fig_r2 = px.bar(
                    reg_df, x="Algorithm", y="R2_Score",
                    color="Algorithm",
                    color_discrete_sequence=['#1565c0', '#43a047', '#2e7d32'],
                    title="<b>R² Score Comparison (Higher is Better)</b>"
                )
                fig_r2.update_layout(height=350, yaxis=dict(range=[0, 1.05]))
                st.plotly_chart(fig_r2, use_container_width=True)

            with r_col2:
                fig_rmse = px.bar(
                    reg_df, x="Algorithm", y="RMSE",
                    color="Algorithm",
                    color_discrete_sequence=['#d32f2f', '#f57c00', '#388e3c'],
                    title="<b>RMSE Comparison (Lower is Better)</b>"
                )
                fig_rmse.update_layout(height=350)
                st.plotly_chart(fig_rmse, use_container_width=True)

            st.success(f"⭐ **Optimal Model Selected:** `{best_reg}` is deployed for yield forecasting.")

        # Tab 3: Dataset Inspection
        with perf_tabs[2]:
            st.markdown("#### 🔍 Raw Dataset Explorer")
            ds_choice = st.radio("Select Dataset to Inspect", ["Crop Recommendation Dataset", "Yield Prediction Dataset"], horizontal=True)
            
            if ds_choice == "Crop Recommendation Dataset":
                df_crop = pd.read_csv("data/crop_recommendation.csv")
                st.write(f"Displaying top 15 of **{len(df_crop)}** records:")
                st.dataframe(df_crop.head(15), use_container_width=True)
                st.write("**Descriptive Statistics:**")
                st.dataframe(df_crop.describe(), use_container_width=True)
            else:
                df_yield = pd.read_csv("data/yield_prediction.csv")
                st.write(f"Displaying top 15 of **{len(df_yield)}** records:")
                st.dataframe(df_yield.head(15), use_container_width=True)
                st.write("**Descriptive Statistics:**")
                st.dataframe(df_yield.describe(), use_container_width=True)


# =============================================================
# 6. HISTORY & LOGS PAGE (SQLite)
# =============================================================
elif selected_page == "📜 History & Logs":
    st.markdown("## 📜 Analysis & Prediction History (SQLite)")
    st.markdown("Review past farmer queries, soil audits, and yield estimations persisted in the local SQLite database.")
    
    hist_tabs = st.tabs([
        "🌱 Soil Analysis History",
        "🌾 Crop Recommendation History",
        "📊 Yield Prediction History"
    ])
    
    with hist_tabs[0]:
        df_soil_hist = get_history_df("soil_analysis_logs")
        if df_soil_hist.empty:
            st.info("No soil analysis records logged yet.")
        else:
            st.dataframe(df_soil_hist, use_container_width=True)
            csv_data = df_soil_hist.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Soil History as CSV", csv_data, "soil_history.csv", "text/csv")

    with hist_tabs[1]:
        df_crop_hist = get_history_df("crop_recommendation_logs")
        if df_crop_hist.empty:
            st.info("No crop recommendation records logged yet.")
        else:
            st.dataframe(df_crop_hist, use_container_width=True)
            csv_data = df_crop_hist.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Crop History as CSV", csv_data, "crop_recommendation_history.csv", "text/csv")

    with hist_tabs[2]:
        df_yield_hist = get_history_df("yield_prediction_logs")
        if df_yield_hist.empty:
            st.info("No yield prediction records logged yet.")
        else:
            st.dataframe(df_yield_hist, use_container_width=True)
            csv_data = df_yield_hist.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Yield History as CSV", csv_data, "yield_prediction_history.csv", "text/csv")


# =============================================================
# 7. ABOUT PROJECT PAGE
# =============================================================
elif selected_page == "ℹ️ About Project":
    st.markdown("## ℹ️ About the Project")
    st.markdown("### Smart Agriculture System for Soil Health Analysis, Crop Recommendation and Yield Prediction")
    
    st.markdown("""
    <div class="agri-card">
        <h4>🎯 Project Abstract & Objectives</h4>
        <p style="color: #444; line-height: 1.6;">
            Agriculture remains the cornerstone of the economy, yet traditional farming practices frequently suffer from
            suboptimal crop selection, soil nutrient exhaustion, and uncertain harvest yields. This project presents an integrated,
            AI/ML-based decision support platform that empowers agriculturalists, extension workers, and students to:
        </p>
        <ul>
            <li><b>Analyze Soil Chemistry:</b> Evaluate macronutrient (N-P-K) reserves, pH reaction, and moisture content with scientific classification (Healthy, Moderate, Needs Improvement).</li>
            <li><b>Recommend Optimal Crops:</b> Utilize multi-class machine learning classifiers (Random Forest, Decision Trees, KNN, SVM) to match 22 crops to soil and environmental variables.</li>
            <li><b>Forecast Crop Harvest:</b> Apply regression models to estimate yields in Tonnes/Ha and evaluate financial farm-gate revenues.</li>
            <li><b>Audit & Track Records:</b> Persist operational logs in a lightweight SQLite database for agricultural history tracking.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🏗️ Architectural Topology")
    st.markdown("""
    ```mermaid
    graph TD
        A[Farmer / User Inputs] --> B[Streamlit Web Frontend]
        B --> C[Data Preprocessing & Validation]
        C --> D1[Soil Health Analysis Engine]
        C --> D2[Crop Recommendation ML Model]
        C --> D3[Yield Prediction ML Model]
        D1 --> E1[Plotly Radar & Health Gauges]
        D2 --> E2[Top Crops & Probability Distribution]
        D3 --> E3[Yield Tonnes/Ha & Revenue Breakdown]
        D1 & D2 & D3 --> F[(SQLite Database Logging)]
    ```
    """)
    
    st.markdown("### 💻 Technology Stack")
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    t_col1.markdown("**Frontend & UI**\n- Streamlit\n- Plotly Interactive\n- HTML5 / Vanilla CSS")
    t_col2.markdown("**Machine Learning**\n- Scikit-Learn\n- Random Forest\n- Decision Trees, KNN, SVM")
    t_col3.markdown("**Data Engineering**\n- Pandas\n- NumPy\n- Joblib Serialization")
    t_col4.markdown("**Persistence & OS**\n- SQLite Database\n- Python 3.11\n- Windows / Cross-Platform")

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #555; padding: 1rem;'>"
        "<b>Academic Mini-Project Submission</b><br>"
        "Department of Computer Science & Engineering / Information Technology<br>"
        "B.Tech / MCA Mini Project Demonstration"
        "</div>",
        unsafe_allow_html=True
    )
