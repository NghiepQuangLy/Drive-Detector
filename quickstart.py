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
        pageSize=10, fields="nextPageToken, files(id, name, capabilities)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print("Name: ", item['name'], "\nID: ", item['id'])
            print("------------------------------------------")
            if item['capabilities']['canReadRevisions'] is True:
                revisions_json = service.revisions().list(fileId=item['id']).execute()
                revisions_str = json.dumps(revisions_json['revisions'])
                #print(revisions_json)
                revisions_dict = json.loads(revisions_str)
                print("Revision ID - Modified time")
                for revision in revisions_dict:
                    print('{0} - {1}'.format(revision.get('id'), revision.get('modifiedTime')))
                    #print("Last modified user: ", revision.get('lastModifyingUser').get('displayName'), revision.get('lastModifyingUser').get('emailAddress'), "\n")
            else:
                print("Can not read revision - NO PERMISSION")
            print()

if __name__ == '__main__':
    main()
