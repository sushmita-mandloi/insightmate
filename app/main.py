import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.core_agent import create_agent
from agent.tools.python_repl import python_repl_tool, set_dataframe as set_repl_df
from agent.tools.sql_engine import sql_tool, set_csv_path
from agent.tools.chart_generator import chart_tool, set_dataframe as set_chart_df, get_last_chart, generate_chart
from agent.tools.resume_parser import resume_parser_tool, parse_resume

st.set_page_config(page_title="InsightMate", page_icon="🤖", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "mode" not in st.session_state:
    st.session_state.mode = "Data Analyst"
if "df" not in st.session_state:
    st.session_state.df = None

st.title("🤖 InsightMate")
st.caption("AI-powered Data Analysis + Placement Assistant")
st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("📊 Data Analyst Mode", use_container_width=True,
                 type="primary" if st.session_state.mode == "Data Analyst" else "secondary"):
        st.session_state.mode = "Data Analyst"
        st.session_state.messages = []
        st.session_state.agent = None
        st.rerun()
with col2:
    if st.button("🎯 Placement Assistant Mode", use_container_width=True,
                 type="primary" if st.session_state.mode == "Placement" else "secondary"):
        st.session_state.mode = "Placement"
        st.session_state.messages = []
        st.session_state.agent = None
        st.rerun()

st.divider()

if st.session_state.mode == "Data Analyst":
    st.subheader("📊 Data Analyst Mode")
    uploaded_file = st.file_uploader("CSV file upload karo", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        set_repl_df(df)
        set_chart_df(df)
        temp_path = f"data/temp_{uploaded_file.name}"
        os.makedirs("data", exist_ok=True)
        df.to_csv(temp_path, index=False)
        set_csv_path(temp_path, df)
        st.success(f"✅ '{uploaded_file.name}' loaded — {df.shape[0]} rows, {df.shape[1]} columns")
        with st.expander("📋 Data Preview"):
            st.dataframe(df.head())
        st.subheader("📈 Quick Charts")
        chart_type = st.selectbox("Chart type",
