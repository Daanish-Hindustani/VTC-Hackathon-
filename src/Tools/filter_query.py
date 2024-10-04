from langchain_core.tools import tool
import json

@tool
def filter_query(league: str, category: str, query_key: str) -> str:
    """
    Retrieves and filters data from an S3 bucket based on the given league, category, and query_key.

    Args:
        league: The esports league to index into. (e.g., "LCS")
        category: The data category ('leagues', 'tournaments', 'players', 'teams').
        query_key: A search term or key to look for within the data.

    Returns:
        A string containing the filtered results matching the query_key, or an error message.
    """
    if category not in ["leagues", "tournaments", "players", "teams"]:
        return f"Invalid category '{category}'. Please use one of: 'leagues', 'tournaments', 'players', 'teams'."

    # Fetch the data
    data = fetch_gzip_and_parse_json(f"{league}/esports-data/{category}")
    
    if "error" in data:
        return data["error"]

    # Filter the data based on the query_key
    filtered_results = []
    for item in data:
        if query_key.lower() in str(item).lower(): 
            filtered_results.append(item)

    if not filtered_results:
        return f"No results found for '{query_key}' in '{category}' for league '{league}'."

    return json.dumps(filtered_results, indent=4)