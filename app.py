import streamlit as st
import asyncio

# UI Utils
from src.ui.style_utils import inject_custom_css
from src.ui.views.sandbox import render_sandbox, render_sandbox_sidebar
from src.ui.views.intel import render_intel, render_intel_sidebar
from src.ui.views.settings import render_settings, render_settings_sidebar

# Backend Logic
from src.workflows.interactive_pipeline import InteractivePipeline
from src.memory.portfolio_manager import PortfolioManager

# --- Runtime Setup ---
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

st.set_page_config(
    page_title="Ely-Agent COO Dashboard", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def get_pipeline():
    return InteractivePipeline()

def get_portfolio():
    return PortfolioManager()

pipeline = get_pipeline()
portfolio = get_portfolio()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Custom Styling ---
inject_custom_css()

# --- Top Navigation (Segmented Control - "Elegant Tabs") ---
st.markdown('<div style="display: flex; justify-content: center; margin-bottom: 20px;">', unsafe_allow_html=True)
view = st.segmented_control(
    "Navigation", 
    ["💬 逻辑沙盘", "🗞️ 情报中心", "⚙️ 配置中心"], 
    default="💬 逻辑沙盘",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# --- Router Logic (Contextual Sidebar + Main Content) ---
if view == "💬 逻辑沙盘":
    render_sandbox_sidebar(portfolio)
    render_sandbox(pipeline, portfolio)

elif view == "🗞️ 情报中心":
    render_intel_sidebar()
    render_intel()

elif view == "⚙️ 配置中心":
    render_settings_sidebar()
    render_settings()
