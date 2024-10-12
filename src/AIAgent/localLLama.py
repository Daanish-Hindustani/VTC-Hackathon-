from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def askllama():
    llm = Ollama(model="llama2:latest", 
             callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    return llm


def main():
    question = input("enter question: ")
    print(askllama().invoke(question))

if __name__ == "__main__":
    main()
