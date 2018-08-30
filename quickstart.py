from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

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

if __name__ == '__main__':
    main()
