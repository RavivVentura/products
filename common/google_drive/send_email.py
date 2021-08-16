from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from twittersite import settings
from django.core.mail import EmailMessage
import os

# email = EmailMessage(
#     'Hello',
#     'Body goes here',
#     'from@example.com',
#     ['to1@example.com', 'to2@example.com'],
#     ['bcc@example.com'],
#     reply_to=['another@example.com'],
#     headers={'Message-ID': 'foo'},
# )

def send_email(file_name):
    # subject = request.POST.get('subject', '')
    # message = request.POST.get('message', '')
    # # from_email = request.POST.get('from_email', '')
    # if subject and message and from_email:
    print('dir',os.path.isdir('./CSV_FILES'))
    print('file', os.path.isfile('./CSV_FILES/opencomp_webinars.csv'))
    try:
        print("im here")
        message = EmailMessage("stav", file_name, settings.EMAIL_HOST_USER, ["stav@getbrew.com"])
        print("creat message2")
        #message.attach(file_name, img_data, 'text/csv')
        try:
            file = open("./CSV_FILES/{0}".format(file_name))
        except Exception as e:
            print("exception", e)
        # message.attach(file)
        message.attach_file("./CSV_FILES/{0}".format(file_name))
        print("create file")
        message.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return HttpResponseRedirect('/contact/thanks/')
    # else:
    #     # In reality we'd use a form class
    #     # to get proper validation errors.
    #     return HttpResponse('Make sure all fields are entered and valid.')






























# import smtplib, ssl
# import getpass
#
# port = 465  # For SSL
# smtp_server = "smtp.gmail.com"
# sender_email = "stavforwork@gmail.com"  # Enter your address
# receiver_email = "stav@everthere.co"  # Enter receiver address
#
#
# password = getpass.getpass(prompt='Type your password and press enter: ')
# # password = input("Type your password and press enter: ")
# message = """\
# Subject: Hi there
#
# This message is sent from Python."""
#
# context = ssl.create_default_context()
# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, message)

#
# from __future__ import print_function
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
#
# # If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
#
# def main():
#     """Shows basic usage of the Gmail API.
#     Lists the user's Gmail labels.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 '../client_secret.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#
#     service = build('gmail', 'v1', credentials=creds)
#
#     # Call the Gmail API
#     results = service.users().labels().list(userId='me').execute()
#     labels = results.get('labels', [])
#
#     if not labels:
#         print('No labels found.')
#     else:
#         print('Labels:')
#         for label in labels:
#             print(label['name'])
#
# if __name__ == '__main__':
#     main()