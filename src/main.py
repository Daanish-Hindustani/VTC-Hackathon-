import streamlit as st
import time
import boto3


def response_generator(input):
   
    response = "K"
    for word in response["output"].split():
        yield word + " "
        time.sleep(0.05)

def main(): 
    st.title("Valorant AI Agent")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask Me A Question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Replace with api
            response = st.write_stream(response_generator(prompt))
        st.session_state.messages.append({"role": "assistant", "content": response})

# if "__main__" == __name__:
#     main()

