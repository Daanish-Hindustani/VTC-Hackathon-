
import json
from query_tool import query_tool

def lambda_handler(event, context):
    print(event)
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])

    #Extract parameters
    param_dict = {param["name"].lower(): str(param["value"]) for param in parameters if param['type'] == 'string'}
    
    if function == "query_tool":
        league = param_dict.get("league")
        category = param_dict.get("category")
        query_key = param_dict.get("query_key")
        query_value = param_dict.get("query_value")
        important_fields = param_dict.get("important_fields")
        
        res = query_tool(league, category, query_key, query_value, important_fields)
        
        res_text = "The json data returned for the following league: {}, category: {}, query_key: {}, query_value: {}, important_fields: {}, json: {}".format(league, category, query_key, query_value, important_fields, res)
        
        responseBody = {
                "TEXT": {
                    "body": res_text
                }
        }
    
    
    
    
    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }

    }

    dummy_function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(dummy_function_response))

    return dummy_function_response
