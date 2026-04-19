import streamlit as st
import os
import subprocess
import threading
from datetime import datetime

REPORT_DIR = "reports/daily_briefings"

def run_mission_async():
    """Runs run_mission.py in a background thread to avoid blocking UI."""
    def target():
        try:
            st.session_state.intel_running = True
            # Use sys.executable to ensure we use the same environment
            import sys
            process = subprocess.Popen(
                [sys.executable, "run_mission.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd()
            )
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                st.session_state.intel_status = "success"
                st.session_state.intel_message = "✅ 情报简报生成成功！"
            else:
                st.session_state.intel_status = "error"
                st.session_state.intel_message = f"❌ 生成失败: {stderr}"
        except Exception as e:
            st.session_state.intel_status = "error"
            st.session_state.intel_message = f"❌ 运行异常: {str(e)}"
        finally:
            st.session_state.intel_running = False

    thread = threading.Thread(target=target)
    thread.start()

def render_intel():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("🗞️ 情报简报中心")
    
    # Header logic for status
    if st.session_state.get("intel_running"):
        st.info("⚡ Ely 正在后台全力抓取全球情报，这通常需要 1-2 分钟。您可以继续切换板块聊天。")
        st.progress(0.5) # Indeterminate or simulated progress
    elif st.session_state.get("intel_status") == "success":
        st.success(st.session_state.get("intel_message"))
    elif st.session_state.get("intel_status") == "error":
        st.error(st.session_state.get("intel_message"))

    # Report Browser
    selected_report = st.session_state.get("selected_report_file")
    if selected_report and os.path.exists(os.path.join(REPORT_DIR, selected_report)):
        with open(os.path.join(REPORT_DIR, selected_report), "r", encoding="utf-8") as f:
            content = f.read()
            st.markdown("---")
            st.markdown(content)
    else:
        st.info("💡 请在左侧选择一份历史报告，或者点击‘生成最新日报’。")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_intel_sidebar():
    st.sidebar.markdown("### 🎯 操作面板")
    if st.sidebar.button("🚀 生成今日简报", disabled=st.session_state.get("intel_running", False)):
        st.session_state.intel_status = "running"
        run_mission_async()
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 历史存证")
    
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)
        
    files = sorted([f for f in os.listdir(REPORT_DIR) if f.endswith(".md")], reverse=True)
    if files:
        report_choice = st.sidebar.radio("选择报告日期", files, key="intel_report_radio")
        st.session_state.selected_report_file = report_choice
    else:
        st.sidebar.caption("暂无存量报告")
