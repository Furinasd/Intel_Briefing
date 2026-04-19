import streamlit as st
import yaml
import os
from dotenv import set_key, load_dotenv

PORTFOLIO_FILE = "portfolio.yaml"
ENV_FILE = ".env"

def load_portfolio_data():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {}

def save_portfolio_data(data):
    with open(PORTFOLIO_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)

def render_settings():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("⚙️ COO 架构与配置")
    
    tab_cfg = st.selectbox("配置子项", ["资产仓位管理", "API 秘钥与环境"])

    if tab_cfg == "资产仓位管理":
        st.subheader("📊 持仓底稿 (portfolio.yaml)")
        st.caption("修改下方表格并点击‘保存更改’，数据将实时同步至 Ely 的推演大脑。")
        
        data = load_portfolio_data()
        positions = data.get("positions", [])
        
        # UI for editing positions
        edited_positions = st.data_editor(
            positions, 
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "asset": "标的代码",
                "type": "资产类型",
                "avg_cost": st.column_config.NumberColumn("平均成本", format="$%.2f"),
                "shares": "持有数量",
                "category": st.column_config.SelectboxColumn("分类", options=["Core", "Satellite"]),
                "notes": "投资备忘录"
            }
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("💾 保存持仓更改"):
                data["positions"] = edited_positions
                save_portfolio_data(data)
                st.success("持仓配置已固化到本地。")
                st.rerun()

    elif tab_cfg == "API 秘钥与环境":
        st.subheader("🔑 核心中枢密钥")
        st.caption("此处管理的敏感密钥用于情报抓取与模型分析。")
        
        load_dotenv(ENV_FILE)
        
        # Display and edit specific keys
        keys_to_manage = [
            "GITHUB_TOKEN", "GEMINI_API_KEY", "XAI_API_KEY", 
            "PRODUCTHUNT_TOKEN", "FEISHU_APP_ID", "FEISHU_APP_SECRET"
        ]
        
        for key in keys_to_manage:
            val = os.getenv(key, "")
            new_val = st.text_input(f"**{key}**", value=val, type="password" if "SECRET" in key or "KEY" in key or "TOKEN" in key else "default")
            if new_val != val:
                set_key(ENV_FILE, key, new_val)
                st.toast(f"已更新 {key}")
        
        st.info("💡 修改密钥后可能需要重启 Streamlit 服务或重新触发任务以生效。")

    st.markdown('</div>', unsafe_allow_html=True)

def render_settings_sidebar():
    st.sidebar.markdown("### 🛠️ 系统状态")
    st.sidebar.success("本地服务器: 运行中")
    st.sidebar.info(f"配置路径: {os.path.abspath(PORTFOLIO_FILE)}")
