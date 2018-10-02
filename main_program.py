import google_api
import rest_api
import activity_api
import file
from piechart import *

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
        drive_name = []
        # prompts the user for a team drive name
        user_input_team_drive = input("Please enter the name of a team drive: ")

        # traverse all the team drives the user has until the one specified by the user is found
        found = False
        for drive in team_drives:
            if drive['name'] == user_input_team_drive:
                drive_name.append(drive['name'])
                found = True
                break

        # if the team drive by the specified by the user does not exist
        if not found:
            print("No such drive")
            return

    

    print('D R I V E:', drive['name'])

    print('*********************************')

    files = apis['rest'].get_files(drive['id'])

    if not files:
        print('No files found')
    else:
        drive_users = []
        drive_contr = []
        print('F I L E S:')
        for a_file in files:
            if a_file.get('mimeType') != 'application/vnd.google-apps.folder':

                current_file = file.File(a_file, apis['rest'], apis['activity'])
                print(current_file.get_all_description())
                print('Contribution:', current_file.contribution)
                print('Timeline:', current_file.timeline)
                
                names = []
                vals = []
                
                for name, val in current_file.contribution.items():
                    if name not in drive_users:
                        drive_users.append(name)
                        drive_contr.append(val)
                    else:
                        for i in range(len(drive_users)):
                            if drive_users[i] == name:
                                drive_contr[i] += val
                                
                    names.append(name)
                    vals.append(val)
                    
                for i in range(len(names)):
                    if names[i] == '':
                        names[i] = 'Unknown'
                        
                #pie chart for % contribution for the current file
                create_pie_chart(drive_name, current_file.name, names, vals)
                
    for i in range(len(drive_users)):
        if drive_users[i] == '':
            drive_users[i] = 'Unknown'
            
    #pie chart for % contribution for the entire drive
    create_pie_chart(drive_name, 'N/A (drive)', drive_users, drive_contr)

    print('*********************************')

if __name__ == '__main__':
    main()
