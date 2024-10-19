from langchain.agents import create_openai_tools_agent, AgentExecutor
from tools import query_tool
import warnings
from prompt import prompt
warnings.filterwarnings("ignore", category=DeprecationWarning)

def agent(llm):
    tools = [query_tool]  
    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt())
    return AgentExecutor(agent=agent, tools=tools, verbose=True, output_key="output")
    