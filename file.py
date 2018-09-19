import datetime

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

            self.id =                google_api_revision_data.get('id')
            self.mod_time =          google_api_revision_data.get('modifiedTime')

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

            event =                  google_api_change_data['combinedEvent']

            self.user =              event.get('user', None)
            if self.user is None:
                self.user =          ''
            else:
                self.user =          self.user['name']

            self.type =              event['primaryEventType']
            self.time =              datetime.datetime.fromtimestamp(int(event['eventTimeMillis']) / 1000)

    def __init__(self, google_api_file_data, revision_api, change_api):
        """
        Constructor of the File class
        If the name of the last modifying user of the file can not be found, the last_mod_user field is left blank.

        :param google_api_file_data: the File data structure returned from Google API
        :param revision_api: service of the revision api to be used to retrieve the file's revisions
        :param change_api: service of the change api to be used to retrieve the file's changes
        """

        self.id =                google_api_file_data['id']
        self.name =              google_api_file_data['name']
        self.trashed =           google_api_file_data['trashed']
        self.canReadRevisions =  google_api_file_data['capabilities']['canReadRevisions']
        self.revision_api =      revision_api
        self.change_api =        change_api

        try:
            self.last_mod_user = google_api_file_data['lastModifyingUser']['displayName']
        except KeyError:
            self.last_mod_user = ''

        self.revisions =         self.get_revisions()
        self.changes =           self.get_changes()

        self.contribution =      self.get_contribution()
        self.timeline =          self.get_timeline()

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
        results_timeline = []

        for change in self.changes:
            results_timeline.append((change.time, change.user))

        return results_timeline

    def print_basic_info(self):
        """
        Prints the name, ID, last modifying user's name of a file
        If the last modifying user's name is not available, nothing will be printed.

        :param file: the file whose info we want to print
        """

        # prints info of file in format
        print('\t',   '{:21}'.format('Name:'), self.name,
              '\n\t', '{:21}'.format('ID:'), self.id,
              '\n\t', '{:21}'.format('Trashed:'), self.trashed,
              '\n\t', '{:21}'.format('Last Modifying User:'), self.last_mod_user)

    def print_revisions(self):
        """
        Prints the revisions of a file including the revision's id, modified time, last modifying user's name and email
        address.
        If the file does not allow reading of its revisions, nothing will be printed.
        If the last modifying user's name or email address is not available, nothing will be printed.

        :param file: the file whose revisions are going to be printed
        """

        # checks if we can read the revisions of the file
        if not self.canReadRevisions:
            print("\tCan not read revision - NO PERMISSION")
            return

        if not self.revisions:
            print('\tNo revision.')
            return

        # prints the column names
        print('\t', '{:12} {:27} {:29}'.format("Revision ID", "Modified time", "Last Modifying User"))

        # loops through all revisions and prints out their info
        for revision in self.revisions:
            print('\t', '{:12} {:27} {:30}'.format(revision.id, revision.mod_time, revision.last_mod_user))

    def print_changes(self):
        """
        Prints the changes of a file including the time of change, user who made the change and the type of change.

        :param file: the file whose revisions are going to be printed
        """

        if not self.changes:
            print('\tNo activity.')
            return

        # prints the column names
        print('\t', '{:30} {:25} {:10}'.format("Time", "User", "Action"))

        # loops through all changes and prints out their info
        for change in self.changes:
            print('\t', change.time, '    {:25} {:10}'.format(change.user, change.type))

    def print_all_info(self):
        """
        Prints the name, ID, last modifying user's name of a file and its revisions including the revision's id, modified
        time, last modifying user's name and email address

        :param file: the file whose info is going to be printed
        """

        self.print_basic_info()
        print("\t------------------------------------------")
        self.print_revisions()
        print("\t------------------------------------------")
        self.print_changes()
        print()


class Folder:
    def __init__(self, files):
        self.files = files
        self.contribution = self.calculate_contribution()

    def add_file(self, file):
        self.files.append(file)
        self.calculate_contribution_a_file(file)

    def calculate_contribution_a_file(self, file):
        for user in file.contribution:
            try:
                self.contribution[user] = self.contribution[user] + 1
            except KeyError:
                self.contribution[user] = 1

    def calculate_contribution_all_files(self):
        self.contribution = {}

        for file in files:
            self.calculate_contribution_a_file(file)
