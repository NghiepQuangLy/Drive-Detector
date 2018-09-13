from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import rest_api
import activity_api

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

def get_service(api):

    store = file.Storage(api.token)
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', api.scope)
        creds = tools.run_flow(flow, store)

    return build(api.name, api.version, http=creds.authorize(Http()))

def main():
    # Prints all the files in a team drive as well as their revisions
    # Prints all activities in a team drive

    apis = [API('token_REST.json',     SCOPES_REST,     'drive',        'v3', 'rest'),
            API('token_ACTIVITY.json', SCOPES_ACTIVITY, 'appsactivity', 'v1', 'activity')]

    services = {}

    for api in apis:
        services[api.api_name] = get_service(api)

    drive_id = None

    # get all team drives of user
    team_drives = rest_api.get_team_drives(services['rest'])

    # prompts the user for a team drive name
    user_input_team_drive = input("Please enter the name of a team drive: ")

    # if the user has no team drives
    if not team_drives:
        print('No drives found')
        return
    else:

        # traverse all the team drives the user has until the one specified by the user is found
        found = False
        for drive in team_drives:
            if drive['name'] == user_input_team_drive:
                found = True
                break

        # if the team drive by the specified by the user does not exist
        if not found:
            print("No such drive")
            return drive_id

    print('D R I V E:', drive['name'])

    print('*********************************')

    files = rest_api.get_files(services['rest'], drive)

    if not files:
        print('No files found')
    else:
        print('F I L E S:')
        for a_file in files:
            rest_api.print_file_all_info(services['rest'], a_file)
            file_changes = activity_api.get_changes(services['activity'], a_file['id'])
            activity_api.print_changes(file_changes)

    print('*********************************')

if __name__ == '__main__':
    main()
