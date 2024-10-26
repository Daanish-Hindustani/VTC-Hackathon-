import json
import boto3

# Define your region and endpoint
REGION = "us-east-1"  # Update if using a different region

# Create the client for Amazon Bedrock runtime API
bedrock_client = boto3.client(
    'bedrock-agent-runtime',
    region_name=REGION,
    endpoint_url=f'https://bedrock-agent-runtime.{REGION}.amazonaws.com'
)

# Define a function to invoke the agent
def invoke_agent(agent_id, agent_alias_id, session_id, input_text, enable_trace=False, end_session=False, session_state={}):
    # Construct the API URL path
    invoke_url = f'/agents/{agent_id}/agentAliases/{agent_alias_id}/sessions/{session_id}/text'
    
    # Create the request payload
    payload = {
        "inputText": input_text,
        "enableTrace": enable_trace,
        "endSession": end_session,
        "sessionState": session_state,
        "agentAliasId":agent_alias_id,
        "agentId": agent_id,
        "sessionId": session_id

    }

    try:
        # Send the POST request to the Bedrock runtime API
        response = bedrock_client.invoke_agent(
            url=invoke_url,  # Path for the specific agent
            body=json.dumps(payload),  # The request payload
            contentType='application/json'  # Specifying JSON content
        )
        
        # Parse the response
        response_data = json.loads(response['body'])
        
        # Print or return the agent's response
        print("Agent Response:", response_data['chunk']['bytes'])
        if enable_trace:
            print("Trace Info:", response_data.get('trace', {}))
        if 'attribution' in response_data:
            print("Attributions:", response_data['attribution'])

    except Exception as e:
        print(f"Error invoking agent: {str(e)}")


