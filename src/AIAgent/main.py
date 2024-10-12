from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import query_tool
from langchain_community.chat_models import ChatOllama
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    llm = ChatOllama(model="llama2")  

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", 
            """
            You are a skilled recruiter for Valorant esports. Based on the input, use the tools to find relevant data and construct a response.
            Leagues: "game-changers", "vct-international", "vct-challengers".
            Categories for query_tool: "leagues", "tournaments", "players", "teams".
            Use snake case for query_key (e.g., first_name). You can query just by query_value without a query_key.
            To condense data, provide important_fields (optional): a list of key fields to summarize. Defaults to None.
            Ask follow-up questions if input is unclear.
            """),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )


    tools = [query_tool]  
    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, output_key="output")
    
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
