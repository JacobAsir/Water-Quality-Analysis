import streamlit as st
import pandas as pd
from main import predict_potability, get_chatbot_response
import plotly.graph_objects as go
import os
import time

# Page configuration
st.set_page_config(
    page_title="Water Quality Analysis System",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme similar to the soil quality app
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Dark theme background */
    .stApp {
        background-color: #1a1f2e;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        color: #8892b0;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Language selector specific styling */
    .language-selector-container {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        margin-top: 0.5rem;
    }
    
    .language-selector-container .stSelectbox > div > div {
        background-color: #2d3548;
        border: 1px solid #3d4558;
        border-radius: 8px;
        color: #ffffff;
        min-width: 200px;
    }
    
    .language-selector-container .stSelectbox label {
        color: #8892b0 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    /* Container styling */
    .parameter-container {
        background-color: #232937;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #2d3548;
    }
    
    /* Input field styling */
    .stNumberInput > div > div > input {
        background-color: #2d3548;
        color: #ffffff;
        border: 1px solid #3d4558;
        border-radius: 8px;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #667eea;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #5a67d8;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Chat container styling - matching the image */
    .chat-container {
        background-color: #232937;
        border-radius: 12px;
        border: 1px solid #2d3548;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Scrollable messages area */
    .messages-container {
        height: 400px;
        overflow-y: auto;
        overflow-x: hidden;
        padding-right: 0.5rem;
    }
    
    /* Custom scrollbar for chat */
    .messages-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .messages-container::-webkit-scrollbar-track {
        background: #1a1f2e;
        border-radius: 3px;
    }
    
    .messages-container::-webkit-scrollbar-thumb {
        background: #4a5568;
        border-radius: 3px;
    }
    
    .messages-container::-webkit-scrollbar-thumb:hover {
        background: #667eea;
    }
    
    /* Chat messages styling */
    .stChatMessage {
        margin-bottom: 0.75rem;
    }
    
    /* User message styling */
    [data-testid="chatMessageContent"] {
        background-color: #2d3548 !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    
    /* Labels */
    label {
        color: #8892b0 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        margin-bottom: 0.25rem !important;
    }
    
    /* Analysis Results Alert Box */
    .analysis-result-box {
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .analysis-result-box.success {
        background-color: #10b981;
        color: white;
    }
    
    .analysis-result-box.warning {
        background-color: #f59e0b;
        color: white;
    }
    
    .analysis-result-box.error {
        background-color: #ef4444;
        color: white;
    }
    
    /* Sidebar buttons */
    .sidebar-button {
        background-color: #3b82f6;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .sidebar-button:hover {
        background-color: #2563eb;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1f2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4a5568;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #667eea;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background-color: #2d3548;
        color: #ffffff;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'water_params' not in st.session_state:
    st.session_state.water_params = {}
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None
if 'language' not in st.session_state:
    st.session_state.language = "English"

# Header with language selector on the same line
header_col1, header_col2, header_col3 = st.columns([1, 4, 1.2])

with header_col1:
    st.write("")  # Empty space for alignment

with header_col2:
    st.markdown('<h1 class="main-header">💧 Water Quality Analysis System</h1>', unsafe_allow_html=True)

with header_col3:
    with st.container():
        st.markdown('<div class="language-selector-container">', unsafe_allow_html=True)
        language = st.selectbox(
            "Select Language / 言語を選択",
            ["English", "Japanese"],
            index=0 if st.session_state.language == "English" else 1,
            key="language_selector"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()

# Subtitle
st.markdown('<p class="sub-header">Analyze water quality for irrigation and get expert recommendations</p>', unsafe_allow_html=True)

# Translation dictionary
translations = {
    "English": {
        "water_params": "📊 Water Quality Parameters",
        "ph": "pH",
        "hardness": "Hardness (mg/L)",
        "solids": "Total Dissolved Solids (ppm)",
        "chloramines": "Chloramines (mg/L)",
        "sulfate": "Sulfate (mg/L)",
        "conductivity": "Conductivity (μS/cm)",
        "organic_carbon": "Organic Carbon (mg/L)",
        "trihalomethanes": "Trihalomethanes (μg/L)",
        "turbidity": "Turbidity (NTU)",
        "analyze_btn": "🔍 Analyze Water Quality",
        "expert_chat": "💬 Water Expert Chat",
        "chat_placeholder": "Ask about water quality improvements, crop recommendations, or treatment options...",
        "success_title": "Water is Suitable for Irrigation",
        "success_desc": "The water quality parameters indicate safe levels for agricultural use.",
        "warning_title": "Water Needs Treatment",
        "warning_desc": "Consider treatment before using for irrigation.",
        "settings": "⚙️ Settings",
        "clear_chat": "Clear Chat",
        "reset_params": "Reset Params",
        "optimal_ranges": "📊 Optimal Ranges",
        "analyze_first": "Please analyze water parameters first before starting the consultation."
    },
    "Japanese": {
        "water_params": "📊 水質パラメータ",
        "ph": "pH",
        "hardness": "硬度 (mg/L)",
        "solids": "総溶解固形物 (ppm)",
        "chloramines": "クロラミン (mg/L)",
        "sulfate": "硫酸塩 (mg/L)",
        "conductivity": "導電率 (μS/cm)",
        "organic_carbon": "有機炭素 (mg/L)",
        "trihalomethanes": "トリハロメタン (μg/L)",
        "turbidity": "濁度 (NTU)",
        "analyze_btn": "🔍 水質を分析する",
        "expert_chat": "💬 水質専門家チャット",
        "chat_placeholder": "水質改善、作物の推奨事項、または処理オプションについて質問してください...",
        "success_title": "灌漑に適した水質です",
        "success_desc": "水質パラメータは農業利用に安全なレベルを示しています。",
        "warning_title": "水処理が必要です",
        "warning_desc": "灌漑に使用する前に処理を検討してください。",
        "settings": "⚙️ 設定",
        "clear_chat": "チャットをクリア",
        "reset_params": "パラメータをリセット",
        "optimal_ranges": "📊 最適範囲",
        "analyze_first": "相談を開始する前に、まず水質パラメータを分析してください。"
    }
}

# Get current language translations
t = translations[st.session_state.language]

# Create two columns for main content
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown(f"### {t['water_params']}")
    
    with st.container():
        st.markdown('<div class="parameter-container">', unsafe_allow_html=True)
        
        # Water quality parameters inputs
        ph = st.number_input(t["ph"], min_value=0.0, max_value=14.0, value=7.0, step=0.1, key="ph_input")
        
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            hardness = st.number_input(t["hardness"], min_value=0.0, max_value=500.0, value=100.0, step=1.0)
            chloramines = st.number_input(t["chloramines"], min_value=0.0, max_value=10.0, value=4.0, step=0.1)
            conductivity = st.number_input(t["conductivity"], min_value=0.0, max_value=1000.0, value=400.0, step=1.0)
            trihalomethanes = st.number_input(t["trihalomethanes"], min_value=0.0, max_value=100.0, value=50.0, step=0.1)
        
        with col1_2:
            solids = st.number_input(t["solids"], min_value=0.0, max_value=50000.0, value=500.0, step=1.0)
            sulfate = st.number_input(t["sulfate"], min_value=0.0, max_value=500.0, value=250.0, step=1.0)
            organic_carbon = st.number_input(t["organic_carbon"], min_value=0.0, max_value=20.0, value=10.0, step=0.1)
            turbidity = st.number_input(t["turbidity"], min_value=0.0, max_value=10.0, value=3.0, step=0.1)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Analyze button
        if st.button(t["analyze_btn"], key="analyze_btn", use_container_width=True):
            # Store parameters
            st.session_state.water_params = {
                'pH': ph,
                'Hardness': hardness,
                'Solids': solids,
                'Chloramines': chloramines,
                'Sulfate': sulfate,
                'Conductivity': conductivity,
                'Organic_carbon': organic_carbon,
                'Trihalomethanes': trihalomethanes,
                'Turbidity': turbidity
            }
            
            # Make prediction
            features = [ph, hardness, solids, chloramines, sulfate, conductivity, 
                       organic_carbon, trihalomethanes, turbidity]
            
            try:
                prediction = predict_potability(features)
                st.session_state.prediction_result = prediction
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

with col2:
    st.markdown(f"### {t['expert_chat']}")
    
    # Show Analysis Results at the top of the chat section if available
    if st.session_state.prediction_result is not None:
        if st.session_state.prediction_result == 1:
            st.markdown(f"""
                <div class="analysis-result-box success">
                    <span>✅</span>
                    <div>
                        <strong>{t['success_title']}</strong><br>
                        <small>{t['success_desc']}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="analysis-result-box warning">
                    <span>⚠️</span>
                    <div>
                        <strong>{t['warning_title']}</strong><br>
                        <small>{t['warning_desc']}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Chat container with background
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Messages container with scroll
        messages_container = st.container(height=400)
        
        with messages_container:
            # Display chat history
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.chat_message("user", avatar="🧑‍🌾").write(message['content'])
                else:
                    st.chat_message("assistant", avatar="🤖").write(message['content'])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input (outside the chat container)
    if prompt := st.chat_input(t["chat_placeholder"]):
        if st.session_state.water_params:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': prompt
            })
            
            # Get response
            params_str = ', '.join([f"{k}: {v}" for k, v in st.session_state.water_params.items()])
            history_str = '\n'.join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_history[:-1]])
            
            with st.spinner("Analyzing..." if st.session_state.language == "English" else "分析中..."):
                response = get_chatbot_response(params_str, history_str, prompt, st.session_state.language)
            
            # Add assistant response
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            
            st.rerun()
        else:
            st.warning(t["analyze_first"])

# Sidebar
with st.sidebar:
    st.markdown(f"### {t['settings']}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t["clear_chat"], use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button(t["reset_params"], use_container_width=True):
            st.session_state.water_params = {}
            st.session_state.prediction_result = None
            st.rerun()
    
    st.markdown("---")
    
    st.markdown(f"### {t['optimal_ranges']}")
    st.markdown("""
    - **pH:** 6.5 - 8.5
    - **Hardness:** < 300 mg/L
    - **TDS:** < 1000 ppm
    - **Conductivity:** < 750 μS/cm
    - **Turbidity:** < 5 NTU
    """)
