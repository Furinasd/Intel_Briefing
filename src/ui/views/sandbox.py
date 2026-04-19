import streamlit as st
from src.workflows.interactive_pipeline import InteractivePipeline
from src.memory.portfolio_manager import PortfolioManager

def render_sandbox(pipeline: InteractivePipeline, portfolio: PortfolioManager):
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("🧠 Ely-Agent 逻辑沙盘")
    st.markdown("欢迎进入深度逻辑推演区。这里会结合您的 **实时报价** 与 **持仓红线** 给出 COO 视角的建议。")

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
    st.markdown('</div>', unsafe_allow_html=True)

def render_sandbox_sidebar(portfolio: PortfolioManager):
    st.sidebar.markdown("### 🛡️ Portfolio 快照")
    st.sidebar.metric(label="USD 现金", value=f"${portfolio.get_cash_balance():,.2f}")
    
    st.sidebar.subheader("核心持仓 (Core)")
    for pos in portfolio.get_all_positions():
        if pos.get("category") == "Core":
            st.sidebar.caption(f"**{pos['asset']}**: {pos['shares']} @ ${pos['avg_cost']}")

    st.sidebar.subheader("卫星持仓 (Satellite)")
    for pos in portfolio.get_all_positions():
        if pos.get("category") == "Satellite":
            st.sidebar.caption(f"**{pos['asset']}**: {pos['shares']} @ ${pos['avg_cost']}")
