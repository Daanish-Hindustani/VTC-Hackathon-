from langchain.agents import create_openai_tools_agent, AgentExecutor
from tools import query_tool
import warnings
from prompt import prompt
warnings.filterwarnings("ignore", category=DeprecationWarning)

def agent(llm):
    tools = [query_tool]  
    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt())
    return AgentExecutor(agent=agent, tools=tools, verbose=True, output_key="output")
    
def main():
    # llm = ChatOllama(model="llama2")  
    # agent_executor = agent(llm)
    # while True:
    #     user_input = input("Enter your question (or type 'exit' to stop): ")
    #     if user_input.lower() == "exit":
    #         print("Exiting...")
    #         break
    #     response = agent_executor.invoke({"input": user_input})
    #     if "output" in response:
    #         print(f"Response: {response['output']}")
    #     else:
    #         print("No valid output received from the agent.")
    pass
