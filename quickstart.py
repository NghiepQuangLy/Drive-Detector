from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # get all team drives of user
    results_drive = service.teamdrives().list(pageSize=10).execute()
    team_drives = json.loads(json.dumps(results_drive['teamDrives']))

    print('D R I V E S:')
    if len(team_drives) == 0:
        print('No drives found')
    else:
        # goes through all the drive on the user's account
        for drive in team_drives:
            print('*********************************\n', drive['name'])
            results_file = service.files().list(pageSize=20, includeTeamDriveItems=True, corpora='teamDrive',
                                                supportsTeamDrives=True, teamDriveId=drive['id'],
                                                fields="nextPageToken, files(id, name, capabilities, lastModifyingUser)").execute()
            files = results_file.get('files', [])

            if not files:
                print('\t', drive['name'], ': No files found')
            else:
                print('\tF I L E S:')
                for a_file in files:
                    print('\t', '{:21}'.format('Name:'), a_file['name'], '\n\t', '{:21}'.format('ID:'), a_file['id'], '\n\t', '{:22}'.format('Last Modifying User:'), end="")
                    try:
                        print(a_file['lastModifyingUser']['displayName'])
                    except KeyError:
                        print()
                    print("\t------------------------------------------")
                    if a_file['capabilities']['canReadRevisions'] is True:

                        revisions_json = service.revisions().list(fileId=a_file['id'],
                                                                  fields="revisions(id, modifiedTime, lastModifyingUser)").execute()
                        revisions_str = json.dumps(revisions_json['revisions'])
                        revisions_dict = json.loads(revisions_str)

                        print('\t', '{:12} {:27} {:29} {:20} {:30}'.format("Revision ID", "Modified time", "Last Modifying User",
                                                               "Email", "Hello"))
                        for revision in revisions_dict:
                            print('\t', '{:12} {:27} '.format(revision.get('id'), revision.get('modifiedTime')), end="")
                            try:
                                print('{:30}'.format(revision.get('lastModifyingUser').get('displayName')), end="")
                                if revision.get('lastModifyingUser').get('emailAddress') is not None:
                                    print('{:20}'.format(revision.get('lastModifyingUser').get('emailAddress')))
                                    print('{:40}'.format(revision.lists(a_file).revisions()))
                                    """trying to work on revisions"""
                                else:
                                    print()
                            except Exception:
                                print()
                    else:
                        print("\tCan not read revision - NO PERMISSION")
                    print()
            print('*********************************')

            response = drive_service.changes().getStartPageToken().execute()
            print('Start token: %s' % response.get('startPageToken'))

            page_token = saved_start_page_token
            while page_token is not None:
                response = drive_service.changes().list(pageToken=page_token,
                                                        spaces='drive').execute()
                for change in response.get('changes'):
                    # Process change
                    print('Change found for file: %s' % change.get('fileId'))
                if 'newStartPageToken' in response:
                    # Last page, save this token for the next polling interval
                    saved_start_page_token = response.get('newStartPageToken')
                page_token = response.get('nextPageToken')


"""
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, capabilities, lastModifyingUser)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print("Name: ", item['name'], "\nID: ", item['id'], "\nLast Modifying User: ", end="")
            try:
                print(item['lastModifyingUser']['displayName'], " - ", item['lastModifyingUser']['emailAddress'])
            except KeyError:
                print("Can not get last modifying user information")
            print("------------------------------------------")
            if item['capabilities']['canReadRevisions'] is True:
                revisions_json = service.revisions().list(fileId=item['id'], fields="revisions(id, modifiedTime, lastModifyingUser)").execute()
                revisions_str = json.dumps(revisions_json['revisions'])
                revisions_dict = json.loads(revisions_str)
                print('{:12} {:27} {:29} {:20}'.format("Revision ID", "Modified time", "Last Modifying User", "Email"))
                for revision in revisions_dict:
                    print('{:12} {:27} '.format(revision.get('id'), revision.get('modifiedTime')), end="")
                    try:
                        print('{:30}'.format(revision.get('lastModifyingUser').get('displayName')), end="")
                        if revision.get('lastModifyingUser').get('emailAddress') is not None:
                            print('{:20}'.format(revision.get('lastModifyingUser').get('emailAddress')))
                        else:
                            print()
                    except Exception:
                        print()
                    #print("Last modified user: ", revision.get('lastModifyingUser').get('displayName'), revision.get('lastModifyingUser').get('emailAddress'), "\n")
            else:
                print("Can not read revision - NO PERMISSION")
            print()
"""
if __name__ == '__main__':
    main()
