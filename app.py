import streamlit as st
import time
from src.memory.portfolio_manager import PortfolioManager
from src.workflows.interactive_pipeline import InteractivePipeline

# Required for asyncio or httpx errors in Streamlit
import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

st.set_page_config(page_title="Ely-Agent COO 沙盘", page_icon="📈", layout="wide")

# Initialize backend
@st.cache_resource
def get_pipeline():
    return InteractivePipeline()

@st.cache_resource
def get_portfolio():
    return PortfolioManager()

pipeline = get_pipeline()
portfolio = get_portfolio()

# --- Sidebar: Data Snapshot ---
with st.sidebar:
    st.header("🛡️ Portfolio Snapshot")
    st.metric(label="Cash Reserves", value=f"${portfolio.get_cash_balance():,.2f}")
    
    st.subheader("Core Holdings")
    for pos in portfolio.get_all_positions():
        cat = pos.get("category", "")
        if cat == "Core":
            st.write(f"- **{pos['asset']}**: {pos['shares']} qty @ ${pos['avg_cost']:.2f}")

    st.subheader("Satellite Holdings")
    for pos in portfolio.get_all_positions():
        cat = pos.get("category", "")
        if cat == "Satellite":
            st.write(f"- **{pos['asset']}**: {pos['shares']} qty @ ${pos['avg_cost']:.2f}")

    risk = portfolio.get_risk_parameters()
    if risk:
        st.subheader("Risk Redlines")
        st.caption(f"Max Drawdown Alert: {risk.get('max_drawdown_alert')}")
        st.caption(f"Target Core/Sat: {risk.get('core_satellite_ratio')}")


# --- Main Window: Interaction ---
st.title("🧠 Ely-Agent 逻辑沙盘")
st.markdown("欢迎使用深度互动控制台。数据感知层已桥接 **Yahoo Finance** 与 **CoinGecko**。")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("询问市场行情，或者请求盘点持仓..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Agent Response
    with st.chat_message("assistant"):
        with st.spinner("Ely 正在进行底层数据推演..."):
            response = pipeline.process_query(prompt)
            st.markdown(response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
