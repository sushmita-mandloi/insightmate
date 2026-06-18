from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

import streamlit as st

def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        return os.getenv("GROQ_API_KEY")

REACT_PROMPT = """You are InsightMate, an AI data analysis agent.

You have access to the following tools:
{tools}

STRICT RULES:
- ALWAYS use Python_REPL tool to execute code and get actual results
- NEVER give theoretical answers without executing code
- Store output in 'result' variable always
- Use EXACTLY this format:

Question: the input question
Thought: I need to use a tool to get actual data
Action: Python_REPL
Action Input: result = df.groupby('Category')['Purchase Amount (USD)'].mean()
Observation: [tool result]
Thought: I now have the actual result
Final Answer: [answer based on actual executed result]

Tool names: {tool_names}

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

def create_agent(tools: list):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
      api_key=get_api_key()
    )

    prompt = PromptTemplate.from_template(REACT_PROMPT)

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=8,
        handle_parsing_errors=True
    )

    return agent_executor