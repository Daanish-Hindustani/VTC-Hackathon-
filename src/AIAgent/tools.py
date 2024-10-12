import json
from utilities import get_data
from langchain.agents import tool


@tool
def query_tool(league: str, category: str, query_key: str, query_value: str = None) -> str:
    """
    Retrieves and filters data from an S3 bucket based on the given league, category, and query_key.
    Please ask follow-up questions if you are unable to find specific arguments from the user input,
    or need additional info for the query_key.
    
    Args:
        league: game-changers, vct-international, vct-challengers
        category: 'leagues', 'tournaments', 'players', 'teams'.
        query_key: A search term or key to look for within the data, keys are in snake case.
        query_value: A value to look for within the data and query_key, this is optional.
    Returns:
        A string containing the filtered results matching the query_key, or an error message.
    """
    
    # Validate category
    valid_categories = ["leagues", "tournaments", "players", "teams"]
    if category not in valid_categories:
        return f"Invalid category '{category}'. Please use one of: {', '.join(valid_categories)}."
    
    # Validate league
    valid_leagues = ["game-changers", "vct-international", "vct-challengers"]
    if league not in valid_leagues:
        return f"Invalid league '{league}'. Please use one of: {', '.join(valid_leagues)}."

    # Fetch the data
    data = get_data(f"{league}/esports-data/{category}")

    if "error" in data:
        return data["error"]

    # Filter the data based on query_key and query_value (if provided)
    filtered_results = []
    query_key_lower = query_key.lower()
    
    for item in data:
        # Check if the query_key is in the item (case-insensitive)
        if query_key_lower in str(item).lower():
            # If query_value is provided, filter based on its value
            if query_value:
                query_value_lower = query_value.lower()
                # Check if query_key exists in item and if its value matches query_value
                if query_key in item and query_value_lower in str(item[query_key]).lower():
                    filtered_results.append(item)
            else:
                filtered_results.append(item)

    # Return results or a message if none found
    print(filtered_results)
    if not filtered_results:
        return f"No results found for '{query_key}' in '{category}' for league '{league}'."
    
    return json.dumps(filtered_results, indent=4)
    


def main():
    res = query_tool.invoke({
        "league": "game-changers",
        "category": "players",
        "query_key": "first_name",
        "query_value": "Vanessa"
    })
    print(res)

if __name__ == "__main__":
    main()
