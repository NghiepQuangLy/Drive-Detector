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

    files = apis['rest'].get_files(drive['id'])

    if not files:
        print('No files found')
    else:
        print('F I L E S:')

        folders = {}
        folder_id_name = []
        files_not_in_folder = []

        for a_file in files:

            # getting all the folder names and ids
            if a_file.get('mimeType') == 'application/vnd.google-apps.folder' and not a_file.get('trashed'):
                folder_id_name.append((a_file.get('id'), a_file.get('name')))

            if a_file.get('mimeType') != 'application/vnd.google-apps.folder' and not a_file.get('trashed'):

                current_file = file.File(a_file, apis['rest'], apis['activity'])

                # get all the parents of a file
                for parent in a_file.get('parents'):
                    if parent == drive['id']:
                        files_not_in_folder.append(current_file)
                    else:
                        if parent not in folders:
                            folders[parent] = []

                        folders[parent].append(current_file)

        for folder in folder_id_name:
            folders[folder[1]] = folders.pop(folder[0])

        drive_contents = []

        for folder in folders:
            current_folder = file.Folder(folder, folders[folder])
            drive_contents.append(current_folder)

        for file_not_in_folder in files_not_in_folder:
            drive_contents.append(file_not_in_folder)

        print(drive_contents)


if __name__ == '__main__':
    main()
