import streamlit as st

def inject_custom_css():
    """Injects high-end CSS for a premium COO dashboard look."""
    st.markdown("""
    <style>
        /* Global Font & Background */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@300;400;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        h1, h2, h3 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
        }

        /* Glassmorphism Effect */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 15px !important;
            margin-bottom: 10px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .stChatMessage:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }

        /* Gradient sidebar & Main Header */
        [data-testid="stSidebar"] {
            background-image: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            background-color: transparent;
        }

        /* Pretty buttons */
        div.stButton > button {
            border-radius: 10px;
            padding: 0.5rem 1rem;
            background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            border: none;
            transition: all 0.2s ease;
        }
        
        div.stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
        }

        /* Metric cards */
        [data-testid="stMetricValue"] {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            color: #818cf8;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease forwards;
        }
    </style>
    """, unsafe_allow_html=True)
