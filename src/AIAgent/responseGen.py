import random
import time
import sys
import os
from langchain_community.chat_models import ChatOllama
from agentExecutor import agent

def response_generator(input):
    llm = ChatOllama(model="llama2")  
    agent_executor = agent(llm)  
    response = agent_executor.invoke({"input": input})
    for word in response["output"].split():
        yield word + " "
        time.sleep(0.05)

def main():
    # Get the generator object
    generator = response_generator("Who's the best Valorant player?")
    
    # Print each word generated
    for word in generator:
        print(word, end='')  

if __name__ == "__main__":
    main()