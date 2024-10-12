from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import query_tool
from langchain_community.chat_models import ChatOllama


# Assuming all necessary imports and tools are set up
def main():
    # Initialize the LLM
    llm = ChatOllama(model="llama2")  

    # Create a prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", 
             """
             You are a powerful recruiter for Valorant Game. Based on the input, use the tools to find related data and construct a response. 
             Here are the leagues: "game-changers", "vct-international", "vct-challengers".
             Here are the categories for query_tool: "leagues", "tournaments", "players", "teams".
             The query_key input needs to be in snake case, like first_name.
             If input is vague, ask follow-up questions.
             """),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    tools = [query_tool]  
    # Create the agent
    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)

    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, output_key="output")
    
    while True:
        # Ask the user for a question
        user_input = input("Enter your question (or type 'exit' to stop): ")
        
        # Exit loop if the user types "exit"
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        
        # Use `invoke` to handle the input
        response = agent_executor.invoke({"input": user_input})

        # Output the result
        if "output" in response:
            print(f"Response: {response['output']}")
        else:
            print("No valid output received from the agent.")

if __name__ == "__main__":
    main()
