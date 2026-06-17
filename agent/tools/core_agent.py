# agent/core_agent.py
# InsightMate ka brain — LangChain ReAct Agent

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain import hub
from dotenv import load_dotenv
import os

# .env file se API key load karo
load_dotenv()

def create_agent(tools: list):
    """
    InsightMate agent banata hai.
    
    tools: list of tools jo agent use kar sakta hai
    returns: AgentExecutor (ready to run agent)
    """
    
    # Step 1: LLM (brain) banao
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Step 2: ReAct prompt load karo (LangChain ka default)
    prompt = hub.pull("hwchase17/react")
    
    # Step 3: Memory banao (conversation yaad rakhne ke liye)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Step 4: Agent banao
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Step 5: AgentExecutor banao (jo actually run karta hai)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,        # terminal mein thinking process dikhata hai
        max_iterations=10,   # infinite loop se bachao
        handle_parsing_errors=True
    )
    
    return agent_executor