import json
import logging
import os

import requests

# Get the API key from the environment variable
_api_key = os.getenv('RUNLOOP_API_KEY')

if _api_key is None:
    raise ValueError("API key not found in environment variables.")

# Define the API endpoint
_base_url = 'https://api.runloop.ai'


def api_get(path: str) -> json:
    # Set up the headers with the Bearer token
    headers = {
        'Authorization': f'Bearer {_api_key}'
    }

    resolved_url = _base_url + path

    logging.debug(f"invoking GET request to {resolved_url}")

    # Perform the GET request
    response = requests.get(resolved_url, headers=headers, timeout=30)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON data from the response
        data = response.json()

        logging.debug(f"response=\n{json.dumps(data, indent=4)}")

        return data
    else:
        logging.debug(f'GET failed status={response.status_code} message={response.content}')
        raise ValueError(f'Failed to retrieve data: {response.status_code}')


def api_post(path: str, body: dict) -> json:
    # Set up the headers with the Bearer token
    headers = {
        'Authorization': f'Bearer {_api_key}'
    }

    resolved_url = _base_url + path

    logging.debug(f"invoking POST request to {resolved_url}")

    # Perform the POST request
    response = requests.post(resolved_url, headers=headers, json=body, timeout=30)

    if response.status_code == 200:
        # Load the JSON data from the response
        body = response.json()

        logging.debug(f"response=\n{json.dumps(body, indent=4)}")

        return body
    else:
        logging.debug(f'POST failed status={response.status_code} message={response.content}')
        raise ValueError(f'Failed to retrieve data: {response.status_code}')

