from twitter.Google import Create_Service
from googleapiclient.http import MediaFileUpload #need to be install poetry
from googleapiclient.discovery import build

def connect_google_api():
    CLIENT_SECRET_FILE = './twitter/client_secret.json'
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
    media = MediaFileUpload('./Webinars/{0}'.format(file_name), mimetype=mime_type)
    service.files().create(
        body=file_metadate,
        media_body=media,
        fields='id'
    ).execute()








    # drive = build('drive', 'v3', credentials=creds)
    # file_metadata = {
    #     'name': 'sampleName',
    #     'parents': [folder_id],
    #     'mimeType': 'application/vnd.google-apps.spreadsheet',
    #     'driveId': folder_id
    # }
    # res = service.files().create(body=file_metadata,
    #                              media_body=media,
    #                              fields='id',
    #                              supportsAllDrives = True
    #                            ).execute()
    # print(res)

#file_names = ['ArgusSec webinars.csv']
#mime_types = ['text/csv']
# def creats_drive_folder():
#     file_metadata = {
#         'name': 'Invoices',
#         'mimeType': 'application/vnd.google-apps.folder',
#         #'parents' =['1qGa0HU8wdb66pqQBtyELWJctbegY0wrk'],
#     }
#     file = service.files().create(body=file_metadata,
#                                         fields='id').execute()
#     print('Folder ID: %s' % file.get('id'))
#
#
# creats_drive_folder()

# all_csv_files_name = os.listdir('../Webinars')
# for file_name in all_csv_files_name:
#     save_file_to_google_drive(file_name)



