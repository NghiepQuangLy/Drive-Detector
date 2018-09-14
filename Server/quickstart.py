from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'

def get_team_drives(api_build):
    """
    Gets the first 10 team drives in the user's drive

    :param api_build: the API
    :return: a dictionary containing the team drives
    """

    # get the team drives of the user
    results_drive = api_build.teamdrives().list(pageSize=10).execute()

    # convert the result into a dictionary structure
    team_drives = json.loads(json.dumps(results_drive['teamDrives']))

    return team_drives

def get_files(api_build, drive):
    """
    Gets the first 20 files in a team drive

    :param api_build: the API
    :param drive: the drive to look for files
    :return: a dictionary containing the files inside the specified team drive
    """

    # get the files in the drive
    results_file = api_build.files().list(pageSize=20, includeTeamDriveItems=True, corpora='teamDrive',
                                        supportsTeamDrives=True, teamDriveId=drive['id'],
                                        fields="nextPageToken, files(id, name, capabilities, lastModifyingUser)").execute()

    # convert the result into a dictionary data structure
    files = results_file.get('files', [])

    return files

def get_revisions(api_build, file):
    """
    Gets all the available revisions of a file

    :param api_build: the API
    :param file: the file to look for revisions
    :return: a dictionary containing the revisions of the specified file
    """

    # get the revisions of the file
    revisions_json = api_build.revisions().list(fileId=file['id'],
                                                fields="revisions(id, modifiedTime, lastModifyingUser)").execute()

    # convert the result into a dictionary data structure
    revisions_dict = json.loads(json.dumps(revisions_json['revisions']))

    return revisions_dict

def print_file_basic_info(file):
    """
    Prints the name, ID, last modifying user's name of a file
    If the last modifying user's name is not available, nothing will be printed.

    :param file: the file whose info we want to print
    """

    # prints info of file in format
    print('\t', '{:21}'.format('Name:'), file['name'], '\n\t', '{:21}'.format('ID:'), file['id'], '\n\t',
          '{:22}'.format('Last Modifying User:'), end="")

    # check if the last modifying user name is available
    try:
        print(file['lastModifyingUser']['displayName'])
    except KeyError:
        print()

def print_file_revisions(api_build, file):
    """
    Prints the revisions of a file including the revision's id, modified time, last modifying user's name and email
    address
    If the file does not allow reading of its revisions, nothing will be printed.
    If the last modifying user's name or email address is not available, nothing will be printed.

    :param api_build: the API
    :param file: the file whose revisions are going to be printed
    """

    # checks if we can read the revisions of the file
    if file['capabilities']['canReadRevisions'] is True:

        # get the revisions of the file
        revisions_dict = get_revisions(api_build, file)

        # prints the column names
        print('\t', '{:12} {:27} {:29} {:20}'.format("Revision ID", "Modified time", "Last Modifying User",
                                                     "Email"))

        # loops through all revisions and prints out their info
        for revision in revisions_dict:
            print('\t', '{:12} {:27} '.format(revision.get('id'), revision.get('modifiedTime')), end="")
            try:
                print('{:30}'.format(revision.get('lastModifyingUser').get('displayName')), end="")
                if revision.get('lastModifyingUser').get('emailAddress') is not None:
                    print('{:20}'.format(revision.get('lastModifyingUser').get('emailAddress')))
                else:
                    print()
            except Exception:
                print()
    else:
        print("\tCan not read revision - NO PERMISSION")

def print_file_all_info(api_build, file):
    """
    Prints the name, ID, last modifying user's name of a file and its revisions including the revision's id, modified
    time, last modifying user's name and email address

    :param api_build: the API
    :param file: the file whose info is going to be printed
    """

    print_file_basic_info(file)
    print("\t------------------------------------------")
    print_file_revisions(api_build, file)
    print()

def main():
    """
    Prints all the files in all team drives as well as their revisions
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # get all team drives of user
    team_drives = get_team_drives(service)

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
            return

    print('D R I V E:', drive['name'])

    print('*********************************')
    files = get_files(service, drive)

    if not files:
        print('No files found')
    else:
        print('F I L E S:')
        for a_file in files:
            print_file_all_info(service, a_file)

            """
            results_token = service.changes().getStartPageToken(supportsTeamDrives=True,
                                                                teamDriveId=drive['id']).execute()
            page_token = results_token.get('startPageToken')

            while page_token:
                results_change = service.changes().list(pageToken=page_token, includeTeamDriveItems=True,
                                                        supportsTeamDrives=True, teamDriveId=drive['id']).execute()
                page_token = results_change.get('nextPageToken')
                print(results_change)
            """

    print('*********************************')


if __name__ == '__main__':
    main()
