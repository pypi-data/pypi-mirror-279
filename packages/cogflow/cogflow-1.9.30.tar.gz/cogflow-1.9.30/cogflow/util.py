"""
    Utility functions
"""

import requests
from datetime import datetime


def make_post_request(url, data=None, params=None, files=None):
    """
        utility function to make POST requests
    :param url: url of the API endpoint
    :param data: JSON payload
    :param params: request params
    :param files : file
    :return: response for the POST request in json format
    """
    try:
        if data:
            response = requests.post(url, json=data, params=params)
        elif files:
            with open(files, "rb") as f:
                file = {"file": f}
                response = requests.post(url, params=params, files=file)
                f.close()
        else:
            response = requests.post(url, params=params)

        if response.status_code == 201:
            print("POST request successful")
            return response.json()
        # if not the success response
        print(f"POST request failed with status code {response.status_code}")
        raise Exception("request failed")
    except requests.exceptions.RequestException as e:
        print(f"Error making POST request: {e}")
        raise Exception(f"Error making POST request: {e}")

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def is_valid_s3_uri(uri):
    """
        method to check if the url is valid S3 url
    :param uri: url to check
    :return:
    """
    # Regular expression for S3 URI
    s3_uri_regex = re.compile(r"^s3://([a-z0-9.-]+)/(.*)$")

    # Check against the regex pattern
    match = s3_uri_regex.match(uri)

    if match:
        bucket_name = match.group(1)
        object_key = match.group(2)

        # Additional checks for bucket name and object key can be added here
        if bucket_name and object_key:
            return True

    return False
