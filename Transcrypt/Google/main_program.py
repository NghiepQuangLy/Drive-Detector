from __future__ import print_function
import datetime
from itertools import chain
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class Trial:
    class GOOGLE_API:
        """
        GOOGLE_API stores the information of a certain API belonging to GOOGLE API family:
            - token
            - permission scope
            - name
            - version
            - name
            - service

        Permission scopes of GOOGLE APIs: https://developers.google.com/identity/protocols/googlescopes
        """

        def __init__(self, token, scope, name, version, api_name):
            """
            Constructor of the GOOGLE_API class

            :param token:    name of the token established after the user logs in to their Google account
            :param scope:    permission scope of the token
            :param name:     name of the api
            :param version:  version of the api
            :param api_name: name of the api
            """

            self.token = token
            self.scope = scope
            self.name = name
            self.version = version
            self.api_name = api_name
            self.service = self.get_service()

        def get_service(self):
            """
            Gets the service of the api

            :return: service of the api
            """

            store = file.Storage(self.token)
            creds = store.get()

            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('credentials.json', self.scope)
                creds = tools.run_flow(flow, store)

            return build(self.name, self.version, http=creds.authorize(Http()))

    class File:
        """
        File stores the information of a file:
            - id of file
            - name of file
            - if the file has been deleted
            - if the user has the permission to read the revisions of the file
            - service of the revision api to be used to retrieve the file's revisions
            - service of the change api to be used to retrieve the file's changes
            - revisions of file
            - changes of file
            - contributors of file and their contribution in the file
            - changes represented in a timeline
        """

        class Revision:
            """
            Revision stores the information of a revision:
                - id of revision
                - time of revision
                - last modifying user of revision
            """

            def __init__(self, google_api_revision_data):
                """
                Constructor of the Revision class
                If the name of the last modifying user of the revision can not be found, the last_mod_user field is left blank.

                :param google_api_revision_data: the Revision data structure returned from Google API
                """

                self.id = google_api_revision_data.get('id')
                self.mod_time = google_api_revision_data.get('modifiedTime')

                try:
                    self.last_mod_user = google_api_revision_data.get('lastModifyingUser').get('displayName')
                except KeyError:
                    self.last_mod_user = ''

        class Change:
            """
            Change stores the information of a change:
                - name of user who made the change
                - type of change:
                    1.  comment
                    2.  create
                    3.  edit
                    4.  emptyTrash
                    5.  move
                    6.  permissionChange
                    7.  rename
                    8.  trash
                    9.  unknown
                    10. untrash
                    11. upload
                - time of change
            """

            def __init__(self, google_api_change_data):
                """
                Constructor of the Change class
                If the name of the user who made the change can not be found, the user field is left blank.

                :param google_api_change_data: the Change data structure returned from Google API
                """

                event = google_api_change_data['combinedEvent']

                self.user = event.get('user', None)
                if self.user is None:
                    self.user = ''
                else:
                    self.user = self.user['name']

                self.type = event['primaryEventType']
                self.time = datetime.datetime.fromtimestamp(int(event['eventTimeMillis']) / 1000).strftime(
                    '%Y-%m-%d %H:%M:%S')

        def __init__(self, google_api_file_data, revision_api, change_api):
            """
            Constructor of the File class
            If the name of the last modifying user of the file can not be found, the last_mod_user field is left blank.

            :param google_api_file_data: the File data structure returned from Google API
            :param revision_api: service of the revision api to be used to retrieve the file's revisions
            :param change_api: service of the change api to be used to retrieve the file's changes
            """

            self.id = google_api_file_data['id']
            self.name = google_api_file_data['name']
            self.trashed = google_api_file_data['trashed']
            self.canReadRevisions = google_api_file_data['capabilities']['canReadRevisions']
            self.revision_api = revision_api
            self.change_api = change_api

            try:
                self.last_mod_user = google_api_file_data['lastModifyingUser']['displayName']
            except KeyError:
                self.last_mod_user = ''

            self.revisions = self.get_revisions()
            self.changes = self.get_changes()

            self.contribution = self.get_contribution()
            self.timeline = self.get_timeline()

        def get_revisions(self):
            """
            Gets the revisions of the file
            If the file has no revisions, an empty array will be returned.

            :return: an array containing the revisions of the file
            """

            results_revision = []

            # use the service of the revision api to retrieve the revisions
            revisions = self.revision_api.get_revisions(self.id)

            # put all the revisions into the returned array
            for revision in revisions:
                results_revision.append(self.Revision(revision))

            return results_revision

        def get_changes(self):
            """
            Gets the changes of the file
            If the file has no changes, an empty array will be returned.

            :return: an array containing the changes of the file
            """

            results_change = []

            # use the service of the change api to retrieve the changes
            changes = self.change_api.get_changes(self.id)

            # put all the changes into the returned array
            for change in changes:
                results_change.append(self.Change(change))

            return results_change

        def get_contribution(self):
            """
            Gets the name of the contributors of the file and their contribution in the file

            :return: a dictionary containing the name of the contributors as keys and the data stored at the keys are how
                     many actions the corresponding contributor performed towards the file
            """

            results_contribution = {}

            for change in self.changes:
                if change.user is not None:
                    try:
                        results_contribution[change.user] = results_contribution[change.user] + 1
                    except KeyError:
                        results_contribution[change.user] = 1

            return results_contribution

        def get_timeline(self):
            """
            Gets the changes that occurred to the file in a chronological order

            :return: an array containing the time of the change and the user responsible for that change
            """

            results_timeline = []

            for change in self.changes:
                results_timeline.append((change.time, change.user))

            return results_timeline

        def get_basic_description(self):
            """
            Prints the name, ID, last modifying user's name of a file
            If the last modifying user's name is not available, nothing will be printed.
            """
            uniform_format = '{:21} {:10}'

            separator = '\n'

            tags = ['Name:', 'ID:', 'Trashed:', 'Last Modifying User:']
            values = [self.name, self.id, str(self.trashed), self.last_mod_user]

            data = []

            for tag, value in zip(tags, values):
                data.append(uniform_format.format(tag, value))

            return separator.join(data)

        def get_revisions_description(self):
            """
            Prints the revisions of a file including the revision's id, modified time, last modifying user's name and email
            address.
            If the file does not allow reading of its revisions, nothing will be printed.
            If the last modifying user's name or email address is not available, nothing will be printed.
            """

            # checks if we can read the revisions of the file
            if not self.canReadRevisions:
                return 'Can not read revision - NO PERMISSION'

            if not self.revisions:
                return 'No revision'

            uniform_format = '{:12} {:27} {:29}'

            separator = '\n'

            data = [''] * (len(self.revisions) + 1)

            # prints the column names
            data[0] = uniform_format.format('Revision ID', 'Modified time', 'Last Modifying User')

            i = 1
            # loops through all revisions and prints out their info
            for revision in self.revisions:
                data[i] = uniform_format.format(revision.id, revision.mod_time, revision.last_mod_user)
                i += 1

            return separator.join(data)

        def get_changes_description(self):
            """
            Prints the changes of a file including the time of change, user who made the change and the type of change.
            """

            if not self.changes:
                return 'No activity'

            uniform_format = '{:30} {:25} {:10}'

            separator = '\n'

            data = [''] * (len(self.changes) + 1)

            # prints the column names
            data[0] = uniform_format.format("Time", "User", "Action")

            i = 1
            # loops through all changes and prints out their info
            for change in self.changes:
                data[i] = uniform_format.format(change.time, change.user, change.type)
                i += 1

            return separator.join(data)

        def get_all_description(self):
            """
            Prints the name, ID, last modifying user's name of a file and its revisions including the revision's id, modified
            time, last modifying user's name and email address
            """

            separator = '\n------------------------------------------\n'

            all_description = [self.get_basic_description(), self.get_revisions_description(),
                               self.get_changes_description()]

            return separator.join(all_description)

    class Folder:
        def __init__(self, files):
            self.files = files
            self.contribution = {}
            self.calculate_contribution()

        def add_file(self, file):
            self.files.append(file)
            self.calculate_contribution_a_file(file)

        def calculate_contribution_a_file(self, file):
            for user in file.contribution:
                try:
                    self.contribution[user] = self.contribution[user] + 1
                except KeyError:
                    self.contribution[user] = 1

        # I made a change here
        def calculate_contribution_all_files(self):
            if self.files:
                self.contribution = {}

                for file in self.files:
                    self.calculate_contribution_a_file(file)

    #############################################

    class ACTIVITY_API(GOOGLE_API):
        """
        ACTIVITY_API provides 1 service offered by Google Drive DRIVE ACTIVITY API:
            - get changes of a file

        Permission scopes of ACTIVITY_API: https://developers.google.com/identity/protocols/googlescopes#appsactivityv1
        """

        def get_changes(self, file_id):
            """
            Gets the first 20 changes of a file

            :param file_id: the file id of the file to look for changes
            :return: a dictionary containing the changes inside the specified file
            """

            # get the changes in the file
            results_activity = self.service.activities().list(source='drive.google.com', drive_fileId=file_id,
                                                              pageSize=20).execute()

            # convert the result into a dictionary data structure
            activities = results_activity.get('activities', [])

            return activities

    #####################################################

    class REST_API(GOOGLE_API):
        """
        REST_API provides 3 services offered by Google Drive REST API:
            - get team drives of a user
            - get files of a drive
            - get revisions of a file

        Permission scopes of REST_API: https://developers.google.com/identity/protocols/googlescopes#drivev3
        """

        def get_team_drives(self):
            """
            Gets the first 10 team drives in the user's drive

            :return: a dictionary containing the team drives
            """

            # get the team drives of the user
            results_drive = self.service.teamdrives().list(pageSize=10).execute()

            # convert the result into a dictionary structure
            team_drives = results_drive.get('teamDrives', [])

            return team_drives

        def get_files(self, drive_id):
            """
            Gets the first 20 files in a team drive

            :param drive_id: the drive id of the drive to look for files
            :return: a dictionary containing the files inside the specified team drive
            """

            # get the files in the drive
            results_file = self.service.files().list(pageSize=20, includeTeamDriveItems=True, corpora='teamDrive',
                                                     supportsTeamDrives=True, teamDriveId=drive_id,
                                                     fields="nextPageToken, files(id, name, mimeType, parents, trashed, capabilities, lastModifyingUser)").execute()

            # convert the result into a dictionary data structure
            files = results_file.get('files', [])

            return files

        def get_revisions(self, file_id):
            """
            Gets all the available revisions of a file

            :param file_id: the file id of the file to look for revisions
            :return: a dictionary containing the revisions of the specified file
            """

            # get the revisions of the file
            results_revision = self.service.revisions().list(fileId=file_id,
                                                             fields="revisions(id, modifiedTime, lastModifyingUser)").execute()

            # convert the result into a dictionary data structure
            revisions = results_revision.get('revisions', [])

            return revisions

    #################################################

    # If modifying these scopes, delete the file token_REST.json.
    SCOPES_REST = 'https://www.googleapis.com/auth/drive.readonly'

    # If modifying these scopes, delete the file token_ACTIVITY.json.
    SCOPES_ACTIVITY = 'https://www.googleapis.com/auth/activity'
    def main():
        # Prints all the files in a team drive as well as their revisions
        # Prints all activities in a team drive

        apis = {'rest':     REST_API('token_REST.json',     SCOPES_REST,     'drive',        'v3', 'rest'),
                'activity': ACTIVITY_API('token_ACTIVITY.json', SCOPES_ACTIVITY, 'appsactivity', 'v1', 'activity')}

        # get all team drives of user
        team_drives = apis['rest'].get_team_drives()

        # if the user has no team drives
        if not team_drives:
            document.getElementById('main_area').innerHTML = ''.format('No drives found')
            # return
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
                document.getElementById('main_area').innerHTML = ''.format("No such drive")
                # return

            document.getElementById('main_area').innerHTML = ''.format('D R I V E:', drive['name'])

            document.getElementById('main_area').innerHTML = ''.format('*********************************')

        files = apis['rest'].get_files(drive['id'])

        if not files:
            document.getElementById('main_area').innerHTML = ''.format('No files found')
        else:
            document.getElementById('main_area').innerHTML = ''.format('F I L E S:')
            for a_file in files:
                if a_file.get('mimeType') != 'application/vnd.google-apps.folder':

                    current_file = file.File(a_file, apis['rest'], apis['activity'])
                    document.getElementById('main_area').innerHTML = ''.format(current_file.get_all_description())
                    document.getElementById('main_area').innerHTML = ''.format('Contribution:', current_file.contribution)
                    document.getElementById('main_area').innerHTML = ''.format('Timeline:', current_file.timeline)

                    document.getElementById('main_area').innerHTML = ''.format()

            document.getElementById('main_area').innerHTML = ''.format('*********************************')

    # if __name__ == '__main__':
        # main()

main_function = Trial()
print(main_function)
