from langchain_community.chat_models import ChatOllama
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from AIAgent.agentExecutor import agent

def main():
    llm = ChatOllama(model="llama2")  
    agent_executor = agent(llm)
    
    while True:
        user_input = input("Enter your question (or type 'exit' to stop): ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        response = agent_executor.invoke({"input": user_input})
        if "output" in response:
            print(f"Response: {response['output']}")
        else:
            print("No valid output received from the agent.")

if __name__ == "__main__":
    main()
