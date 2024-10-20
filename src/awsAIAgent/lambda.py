import json
from langchain_community.chat_models import BedrockChat

from Agent import Agent

def lambda_handler(event, context):
    print(event)
    user_message = get_user_message(event)
    llm = BedrockChat(model_id="anthropic.claude-3-sonnet-20240229-v1:0")
    langchain_agent = Agent(llm)
    message = langchain_agent.run(input=user_message)
    return http_response(message)

def http_response(message):
        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }

def get_user_message(event):
    body = load_body(event)
    user_message_body = body['message']
    return user_message_body


def load_body(event):
    body = json.loads(event['body'])
    return body