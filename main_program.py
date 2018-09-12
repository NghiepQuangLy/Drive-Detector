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

class API:
    def __init__(self, token, scope, name, version, api_name):
        self.token = token
        self.scope = scope
        self.name = name
        self.version = version
        self.api_name = api_name

def main():

    apis = [API('token_REST.json',     SCOPES_REST,     'drive',        'v3', 'rest'),
            API('token_ACTIVITY.json', SCOPES_ACTIVITY, 'appsactivity', 'v1', 'activity')]

    services = {}

    for api in apis:
        store = file.Storage(api.token)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', api.scope)
            creds = tools.run_flow(flow, store)
        services[api.api_name] = build(api.name, api.version, http=creds.authorize(Http()))

    try:
        # Prints all the files in a team drive as well as their revisions
        drive_id = drive_info(services['rest'])

        # Prints all activities in a team drive
        user_activity_info(services['activity'], drive_id)
    except:
        print("An error happened")

if __name__ == '__main__':
    main()


