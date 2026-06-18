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

st.title("InsightMate")
st.caption("AI-powered Data Analysis + Placement Assistant")
st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("Data Analyst Mode", use_container_width=True):
        st.session_state.mode = "Data Analyst"
        st.session_state.messages = []
        st.session_state.agent = None
        st.rerun()
with col2:
    if st.button("Placement Assistant Mode", use_container_width=True):
        st.session_state.mode = "Placement"
        st.session_state.messages = []
        st.session_state.agent = None
        st.rerun()

st.write("Current mode: " + st.session_state.mode)
st.divider()

if st.session_state.mode == "Data Analyst":
    st.subheader("Data Analyst Mode")
    uploaded_file = st.file_uploader("CSV file upload karo", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        set_repl_df(df)
        set_chart_df(df)
        os.makedirs("data", exist_ok=True)
        temp_path = "data/temp.csv"
        df.to_csv(temp_path, index=False)
        set_csv_path(temp_path, df)
        st.success("Loaded: " + str(df.shape[0]) + " rows, " + str(df.shape[1]) + " columns")
        st.dataframe(df.head())
        chart_type = st.selectbox("Chart type", ["bar", "pie", "line", "scatter"])
        cat_cols = [c for c in df.columns if df[c].dtype == 'object']
        num_cols = [c for c in df.columns if df[c].dtype in ['int64', 'float64']]
        col_x = st.selectbox("X axis", cat_cols if cat_cols else df.columns.tolist())
        col_y = st.selectbox("Y axis", num_cols if num_cols else df.columns.tolist())
        if st.button("Generate Chart"):
            result = generate_chart(chart_type + " chart of " + col_y + " by " + col_x)
            chart = get_last_chart()
            if chart:
                st.plotly_chart(chart, use_container_width=True)
        if st.session_state.agent is None:
            tools = [python_repl_tool, sql_tool]
            st.session_state.agent = create_agent(tools)

elif st.session_state.mode == "Placement":
    st.subheader("Placement Assistant Mode")
    resume_file = st.file_uploader("Resume PDF upload karo", type=["pdf"])
    if resume_file:
        os.makedirs("data", exist_ok=True)
        temp_path = "data/temp_resume.pdf"
        with open(temp_path, "wb") as f:
            f.write(resume_file.read())
        st.success("Resume loaded: " + resume_file.name)
        if st.button("Parse Resume"):
            with st.spinner("Analyzing..."):
                result = parse_resume(temp_path)
                st.write(result)
                st.session_state.messages.append({"role": "assistant", "content": result})
        if st.session_state.agent is None:
            tools = [resume_parser_tool]
            st.session_state.agent = create_agent(tools)

st.divider()
st.subheader("Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Kuch bhi poochho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    if st.session_state.agent:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.agent.invoke({"input": prompt})
                    answer = response["output"]
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error("Error: " + str(e))
    else:
        with st.chat_message("assistant"):
            st.write("Pehle file upload karo!")
Commit karo. Batao! 🚀
