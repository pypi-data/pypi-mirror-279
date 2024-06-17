import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env'))

PROJECT_ABSOLUTE_PATH = os.getenv('PROJECT_ABSOLUTE_PATH')
CLIENT_SECRET_PATH = PROJECT_ABSOLUTE_PATH + 'client-secret.json'
TOKEN_FILES_DIRNAME = 'token_files'

def create_service(api_name, api_version, *scopes, prefix = ''):
    SCOPES = [scope for scope in scopes[0]]
    
    creds = None
    token_file = f'token_{api_name}_{api_version}{prefix}.json'

    # Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(PROJECT_ABSOLUTE_PATH, TOKEN_FILES_DIRNAME)):
        os.mkdir(os.path.join(PROJECT_ABSOLUTE_PATH, TOKEN_FILES_DIRNAME))

    if os.path.exists(os.path.join(PROJECT_ABSOLUTE_PATH, TOKEN_FILES_DIRNAME, token_file)):
        creds = Credentials.from_authorized_user_file(os.path.join(PROJECT_ABSOLUTE_PATH, TOKEN_FILES_DIRNAME, token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(os.path.join(PROJECT_ABSOLUTE_PATH, TOKEN_FILES_DIRNAME, token_file), 'w') as token:
                token.write(creds.to_json())
        else:
            start_auth_flow(scopes, token_file)

    try:
        service = build(api_name, api_version, credentials=creds, static_discovery = False)
        print(api_name, api_version, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {api_name}')
        os.remove(os.path.join(PROJECT_ABSOLUTE_PATH, TOKEN_FILES_DIRNAME, token_file))
        return None
    
def is_token_valid(api_name, api_version, *scopes, prefix = ''):
    try:
        SCOPES = [scope for scope in scopes[0]]

        creds = None
        token_file = f'token_{api_name}_{api_version}{prefix}.json'

        # Check if token dir exists first, if not, create the folder
        if not os.path.exists(os.path.join(PROJECT_ABSOLUTE_PATH, TOKEN_FILES_DIRNAME)):
            return False

        if os.path.exists(os.path.join(PROJECT_ABSOLUTE_PATH, TOKEN_FILES_DIRNAME, token_file)):
            creds = Credentials.from_authorized_user_file(os.path.join(PROJECT_ABSOLUTE_PATH, TOKEN_FILES_DIRNAME, token_file), SCOPES)
        else:
            return False

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except:
                    return False
            else:
                return False
    except Exception as e:
        return False
    
    return True

def start_auth_flow(api_name, api_version, *scopes, prefix = ''):
    SCOPES = [scope for scope in scopes[0]]
    token_file = f'token_{api_name}_{api_version}{prefix}.json'

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
    creds = flow.run_local_server(port = 0)

    with open(os.path.join(PROJECT_ABSOLUTE_PATH, TOKEN_FILES_DIRNAME, token_file), 'w') as token:
        token.write(creds.to_json())

def convert_to_RFC_datetime(year = 1900, month = 1, day = 1, hour = 0, minute = 0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt
