import google_api
import rest_api
import activity_api
import file
import json
from flask import Flask
app = Flask(__name__)


@app.route("/")
def main():
    output = ""
    # If modifying these scopes, delete the file token_REST.json.
    SCOPES_REST = 'https://www.googleapis.com/auth/drive.readonly'

    # If modifying these scopes, delete the file token_ACTIVITY.json.
    SCOPES_ACTIVITY = 'https://www.googleapis.com/auth/activity'
    ##########################################################

    # Prints all the files in a team drive as well as their revisions
    # Prints all activities in a team drive

    apis = {'rest':     rest_api.REST_API('token_REST.json',     SCOPES_REST,     'drive',        'v3', 'rest'),
            'activity': activity_api.ACTIVITY_API('token_ACTIVITY.json', SCOPES_ACTIVITY, 'appsactivity', 'v1', 'activity')}

    # get all team drives of user
    team_drives = apis['rest'].get_team_drives()

    # if the user has no team drives
    if not team_drives:
        output += 'No drives found'
        return
    else:

        # prompts the user for a team drive name
        # user_input_team_drive = input("Please enter the name of a team drive: ")
        user_input_team_drive = "FIT2101"

        # traverse all the team drives the user has until the one specified by the user is found
        found = False
        for drive in team_drives:
            if drive['name'] == user_input_team_drive:
                found = True
                break

        # if the team drive by the specified by the user does not exist
        if not found:
            output += "No such drive"
            return

    output += 'D R I V E:' + str(drive['name'])

    files = apis['rest'].get_files(drive['id'])

    if not files:
        output += 'No files found'
    else:
        output += 'F I L E S:'
        folders = {}
        for a_file in files:
            if a_file.get('mimeType') != 'application/vnd.google-apps.folder' and not a_file.get('trashed'):

                current_file = file.File(a_file, apis['rest'], apis['activity'])

                # get all the parents of a file
                for parent in a_file.get('parents'):
                    if parent not in folders:
                        folders[parent] = []

                    folders[parent].append(current_file)

    for folder in folders:
        output += str(folder) + str(folders[folder])
    output += drive['id']

    # print(output)
    return output


if __name__ == '__main__':
    main()
