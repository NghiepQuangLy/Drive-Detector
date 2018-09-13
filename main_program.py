import google_api
import rest_api
import activity_api

# If modifying these scopes, delete the file token_REST.json.
SCOPES_REST = 'https://www.googleapis.com/auth/drive.readonly'

# If modifying these scopes, delete the file token_ACTIVITY.json.
SCOPES_ACTIVITY = 'https://www.googleapis.com/auth/activity'

def main():
    # Prints all the files in a team drive as well as their revisions
    # Prints all activities in a team drive

    apis = {'rest':     google_api.API('token_REST.json',     SCOPES_REST,     'drive',        'v3', 'rest'),
            'activity': google_api.API('token_ACTIVITY.json', SCOPES_ACTIVITY, 'appsactivity', 'v1', 'activity')}

    for api in apis:
        apis[api].get_service()

    drive_id = None

    # get all team drives of user
    team_drives = rest_api.get_team_drives(apis['rest'].service)

    # if the user has no team drives
    if not team_drives:
        print('No drives found')
        return
    else:

        # prompts the user for a team drive name
        user_input_team_drive = input("Please enter the name of a team drive: ")

        # traverse all the team drives the user has until the one specified by the user is found
        found = False
        for drive in team_drives:
            if drive['name'] == user_input_team_drive:
                found = True
                break

        # if the team drive by the specified by the user does not exist
        if not found:
            print("No such drive")
            return

    print('D R I V E:', drive['name'])

    print('*********************************')

    files = rest_api.get_files(apis['rest'].service, drive)

    if not files:
        print('No files found')
    else:
        print('F I L E S:')
        for a_file in files:
            rest_api.print_file_all_info(apis['rest'].service, a_file)

            file_changes = activity_api.get_changes(apis['activity'].service, a_file['id'])
            activity_api.print_changes(file_changes)

            print()

    print('*********************************')

if __name__ == '__main__':
    main()
