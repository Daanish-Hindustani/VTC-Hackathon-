from langchain.agents import Tool
import json
from utilities import condense_data, get_data

class Tools():
    def __init__(self) -> None:
        self.tools = [
            Tool(
                name="Query Tool",
                func=self.query_tool,
                description=
                """
                        Retrieves, filters, and condenses data from an S3 bucket based on the given parameters.

                        Args:
                            league (str): The league to query data from ('game-changers', 'vct-international', 'vct-challengers').
                            category (str): The category of data to retrieve ('leagues', 'tournaments', 'players', 'teams').
                            query_key (str, optional): A search term or key to filter data on, in snake_case. Defaults to None.
                            query_value (str, optional): A value to filter data on, within the query_key. Defaults to None.
                            important_fields (list, optional): A list of important fields to include in the summary. Defaults to None.

                        Returns:
                            str: A JSON string of the filtered and condensed results, or an error message if no data is found or inputs are invalid.
                 """
            )
        ]
    
    def query_tool(self, league: str, category: str, query_key: str = None, query_value: str = None, important_fields: list = None) -> str:

        # Validate category
        valid_categories = ["leagues", "tournaments", "players", "teams"]
        if category not in valid_categories:
            return f"Invalid category '{category}'. Valid options: {', '.join(valid_categories)}."
        
        # Validate league
        valid_leagues = ["game-changers", "vct-international", "vct-challengers"]
        if league not in valid_leagues:
            return f"Invalid league '{league}'. Valid options: {', '.join(valid_leagues)}."

        # Fetch data
        data = get_data(f"{league}/esports-data/{category}")
        
        if not data or "error" in data:
            return data.get("error", "Failed to retrieve data.")

        # Filter data
        filtered_results = []
        query_key_lower = query_key.lower() if query_key else None
        query_value_lower = query_value.lower() if query_value else None

        for item in data:
            item_str = json.dumps(item).lower()  # Convert to string for case-insensitive search
            if query_key_lower:
                # If query_key is specified, filter by key and value if provided
                if query_key_lower in item_str:
                    if query_value_lower and query_value_lower in item.get(query_key, "").lower():
                        filtered_results.append(item)
                    elif not query_value_lower:
                        filtered_results.append(item)
            elif query_value_lower:
                # If only query_value is specified, search across the entire item
                if query_value_lower in item_str:
                    filtered_results.append(item)

        if not filtered_results:
            return f"No results found for the given query in '{category}' under '{league}'."

        # Condense data if important fields are specified
        if important_fields:
            condensed_results = condense_data(filtered_results, important_fields)
        else:
            condensed_results = filtered_results

        return json.dumps(condensed_results, indent=4)

    

tools = Tools().tools