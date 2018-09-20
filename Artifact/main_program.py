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

    apis = {'rest':     rest_api.REST_API('token_REST.json',     SCOPES_REST,     'drive',        'v3', 'rest'),
            'activity': activity_api.ACTIVITY_API('token_ACTIVITY.json', SCOPES_ACTIVITY, 'appsactivity', 'v1', 'activity')}

    # get all team drives of user
    team_drives = apis['rest'].get_team_drives()

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

    files = apis['rest'].get_files(drive)

    if not files:
        print('No files found')
    else:
        print('F I L E S:')
        for a_file in files:

            # If found folder file, prompt user, and ask if the user wants the folder retrieved.

            if a_file.get('mimeType') == 'application/vnd.google-apps.folder':
                print('Folder : ' + a_file.get('name') + ' found')
                print('\n')
                user_input_retrieve = input("Would you like to retrieve the files in the folder? (y/n): ")

                while (user_input_retrieve != "n") and (user_input_retrieve != "y"):
                    print('\n')
                    print("Invalid input, please insert valid input.")
                    user_input_retrieve = input("Would you like to retrieve the files in the folder? (y/n): ")

                if user_input_retrieve == "n":
                    return
                else:
                    print('\n')

            else:

                apis['rest'].print_file_all_info(a_file)
                file_changes = apis['activity'].get_changes(a_file['id'])
                apis['activity'].print_changes(file_changes)

                print()

    print('*********************************')

if __name__ == '__main__':
    main()
