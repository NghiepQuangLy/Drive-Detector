import datetime

class File:

    class Revision:
        def __init__(self, google_api_revision_data):
            self.id =                google_api_revision_data.get('id')
            self.mod_time =          google_api_revision_data.get('modifiedTime')

            try:
                self.last_mod_user = google_api_revision_data.get('lastModifyingUser').get('displayName')
            except KeyError:
                self.last_mod_user = ''

    class Change:
        def __init__(self, google_api_change_data):
            event =                  google_api_change_data['combinedEvent']

            self.user =              event.get('user', None)
            if self.user is None:
                self.user =          ''
            else:
                self.user =          self.user['name']

            self.type =              event['primaryEventType']
            self.time =              datetime.datetime.fromtimestamp(int(event['eventTimeMillis']) / 1000)

    def __init__(self, google_api_file_data, revision_api, change_api):

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
        results_revision = []

        revisions = self.revision_api.get_revisions(self.id)

        for revision in revisions:
            results_revision.append(self.Revision(revision))

        return results_revision

    def get_changes(self):
        results_change = []

        changes = self.change_api.get_changes(self.id)

        for change in changes:
            results_change.append(self.Change(change))

        return results_change

    def get_contribution(self):
        results_contribution = {}

        if not self.changes:
            return

        for change in self.changes:
            if change.user is not None:
                try:
                    results_contribution[change.user] = results_contribution[change.user] + 1
                except KeyError:
                    results_contribution[change.user] = 1

        return results_contribution

    def get_timeline(self):
        results_timeline = []

        if not self.changes:
            return

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

    def calculate_contribution(self):
        results_contribution = {}

        for file in files:
            for user in file.contribution:
                try:
                    self.contribution[user] = self.contribution[user] + 1
                except KeyError:
                    self.contribution[user] = 1

        return results_contribution

    def update_contribution(self):

