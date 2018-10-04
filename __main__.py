import google_api
import rest_api
import activity_api
import file

# If modifying these scopes, delete the file token_REST.json.
SCOPES_REST = 'https://www.googleapis.com/auth/drive.readonly'

# If modifying these scopes, delete the file token_ACTIVITY.json.
SCOPES_ACTIVITY = 'https://www.googleapis.com/auth/activity'

def main():
    # Prints all the files in a team drive as well as their revisions
    # Prints all activities in a team drive

    apis = {'rest':     rest_api.REST_API('token_REST.json',     SCOPES_REST,     'drive',        'v3', 'rest'),
            'activity': activity_api.ACTIVITY_API('token_ACTIVITY.json', SCOPES_ACTIVITY, 'appsactivity', 'v1', 'activity')}

    # get all team drives of user
    team_drives = apis['rest'].get_team_drives()

    if team_drives:
        for team_drive in team_drives:
            if team_drive['name'] == 'FIT2101':
                folders = apis['rest'].get_folders(team_drive['id'])
                for folder in folders:
                    print('******************\n',folder['name'], folder['id'])
                    files_in_folder = apis['rest'].get_files_in_folder(folder['id'])
                    for file_in_folder in files_in_folder:
                        print(file_in_folder['name'])
                files_not_in_folder = apis['rest'].get_files_not_in_folder(team_drive['id'])
                for file_not_in_folder in files_not_in_folder:
                    print('(((((((((((((((((\n',file_not_in_folder['name'])
                    print('***********************')

    """
    account_contents = []

    # if the user has no team drives
    if team_drives:
        for team_drive in team_drives:
            current_drive = file.Drive(team_drive, apis['rest'], apis['activity'])
            account_contents.append(current_drive)

    for drive in account_contents:
        print(drive.name)
    """

if __name__ == '__main__':
    main()
