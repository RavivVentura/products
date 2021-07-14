#from Google import Create_Service
import os
from common.google_drive.Google import Create_Service
from googleapiclient.http import MediaFileUpload #need to be install poetry
from googleapiclient.discovery import build

def connect_google_api():
    CLIENT_SECRET_FILE = './common/client_secret.json'
    #CLIENT_SECRET_FILE = os.environ['CLIENT_SECRET']
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    return service

def save_file_to_google_drive(file_name, folder_id, mime_type='text/csv'):
    service = connect_google_api()
    file_metadate = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload('./CSV_FILES/{0}'.format(file_name), mimetype=mime_type)
    service.files().create(
        body=file_metadate,
        media_body=media,
        fields='id'
    ).execute()





