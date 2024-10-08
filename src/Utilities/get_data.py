import requests
import json
import gzip
from io import BytesIO

S3_BUCKET_URL = "https://vcthackathon-data.s3.us-west-2.amazonaws.com"

def fetch_gzip_and_parse_json(file_name):
    """
    Fetch gzip data from the S3 bucket and return parsed JSON.

    Args:
        file_name: A string formatted as {league}/esports-data/{category}.json.gz
                   where the category can be 'leagues', 'tournaments', 'players', 'teams'.

    Returns:
        Parsed JSON data, or None if the file is not found or an error occurs.
    """
    remote_file = f"{S3_BUCKET_URL}/{file_name}.json.gz"
    response = requests.get(remote_file, stream=True)

    if response.status_code == 200:
        gzip_bytes = BytesIO(response.content)
        with gzip.GzipFile(fileobj=gzip_bytes, mode="rb") as gzipped_file:
            json_bytes = gzipped_file.read()
            json_data = json.loads(json_bytes.decode('utf-8'))
            return json_data
    elif response.status_code == 404:
        return {"error": f"File '{file_name}' not found. Please check the league or category."}
    else:
        return {"error": f"Failed to download '{file_name}'. Status code: {response.status_code}"}
