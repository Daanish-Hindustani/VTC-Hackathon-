import random
import time
import sys
import os
from langchain_community.chat_models import ChatOllama

sys.path.append("..")
import AIAgent

def response_generator(input):
    llm = ChatOllama(model="llama2")  
    agent_executor = AIAgent.agentExecutor.agent(llm)
    response = agent_executor.invoke({"input": input})
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def main():
    print(response_generator("Whos the best valorant player?"))