import requests
import json
import gzip
from io import BytesIO

S3_BUCKET_URL = "https://vcthackathon-data.s3.us-west-2.amazonaws.com"

def get_data(file_name):
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


def condense_data(data: list, important_fields: list) -> list:
    condensed_data = []
    
    for item in data:
        condensed_item = [item[key] for key in important_fields if key in item]  # Extract only the values of important fields
        condensed_data.append(condensed_item)  # Add values as a list
    
    return condensed_data

