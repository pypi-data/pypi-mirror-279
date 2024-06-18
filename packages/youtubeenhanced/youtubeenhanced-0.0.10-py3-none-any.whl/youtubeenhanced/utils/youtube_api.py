from .google_api import create_service as create_google_service, is_token_valid as is_google_token_valid, start_auth_flow as start_google_auth_flow

import os

PROJECT_ABSOLUTE_PATH = os.getenv('PROJECT_ABSOLUTE_PATH')
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']

def is_token_valid():
    """
    Checks if the current Youtube Data v3 API token is valid.

    This method returns True if yes, or False if not.
    """
    return is_google_token_valid(API_NAME, API_VERSION, SCOPES)

def start_auth_flow():
    """
    Starts the Google auth flow for Youtube Data v3 API.
    """
    return start_google_auth_flow(API_NAME, API_VERSION, SCOPES)

def create_service():
    """
    Creates a Youtube Data v3 API service and returns it.
    """
    return create_google_service(API_NAME, API_VERSION, SCOPES)
