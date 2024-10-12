from langchain.agents import create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import query_tool
from localLLama import askllama


def main():
    # Initialize the LLM
    llm = askllama()  

    # Create a prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a very powerful assistant, but don't know current events.",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Create the agent
    agent = create_openai_tools_agent(
        llm=llm,
        tools=[query_tool],
        prompt=prompt
    )

    user_input = input("Enter your question: ")

    # Use the agent to get a response
    response = agent.invoke({"input": user_input,"intermediate_steps": []})  # Changed from run to invoke
    print(response)

if __name__ == "__main__":
    main()
