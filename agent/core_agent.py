from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

def get_api_key():
    try:
        import streamlit as st
        return st.secrets["GROQ_API_KEY"]
    except:
        return os.getenv("GROQ_API_KEY")

REACT_PROMPT = """You are InsightMate, an AI data analysis agent.

You have access to the following tools:
{tools}

STRICT RULES:
- ALWAYS use tools to get actual results
- NEVER give theoretical answers
- Store output in 'result' variable always
- Use EXACTLY this format:

Question: the input question
Thought: I need to use a tool
Action: tool_name
Action Input: code or query here
Observation: tool result
Thought: I have the result
Final Answer: answer here

Available tool names: {tool_names}

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