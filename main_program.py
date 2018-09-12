from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from rest_api import main as drive_info
from activity_api import main as user_activity_info

# If modifying these scopes, delete the file token_REST.json.
SCOPES_REST = 'https://www.googleapis.com/auth/drive.readonly'

# If modifying these scopes, delete the file token_ACTIVITY.json.
SCOPES_ACTIVITY = 'https://www.googleapis.com/auth/activity'

def main():

    store = file.Storage('token_REST.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES_REST)
        creds = tools.run_flow(flow, store)
    service_REST = build('drive', 'v3', http=creds.authorize(Http()))

    store = file.Storage('token_ACTIVITY.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES_ACTIVITY)
        creds = tools.run_flow(flow, store)
    service_ACTIVITY = build('appsactivity', 'v1', http=creds.authorize(Http()))

    # Prints all the files in a team drive as well as their revisions
    drive_id = drive_info(service_REST)

    # Prints all activities in a team drive
    user_activity_info(service_ACTIVITY, drive_id)

if __name__ == '__main__':
    main()


