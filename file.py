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
            self.time =              datetime.datetime.fromtimestamp(int(event['eventTimeMillis']) / 1000).strftime('%Y-%m-%d %H:%M:%S')

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

        tags   = ['Name:',   'ID:',   'Trashed:',        'Last Modifying User:']
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

        all_description = [self.get_basic_description(), self.get_revisions_description(), self.get_changes_description()]

        return separator.join(all_description)


class Folder:
    def __init__(self, name, files):
        self.name = name
        self.files = files
        self.contribution = {}
        self.calculate_contribution_all_files()

    def add_file(self, file):
        self.files.append(file)
        self.calculate_contribution_a_file(file)

    def calculate_contribution_a_file(self, file):
        for user in file.contribution:
            number_of_actions = file.contribution[user]
            while number_of_actions > 0:
                try:
                    self.contribution[user] = self.contribution[user] + 1
                except KeyError:
                    self.contribution[user] = 1
                number_of_actions -= 1

    def calculate_contribution_all_files(self):
        if self.files:
            self.contribution = {}

            for file in self.files:
                self.calculate_contribution_a_file(file)

class Drive:
    def __init__(self, google_api_drive_data, revision_api, change_api):
        self.name =             google_api_drive_data['name']
        self.id =               google_api_drive_data['id']
        self.revision_api =     revision_api
        self.change_api =       change_api
        self.contents =         self.get_contents()
        self.contribution =     {}
        #self.calculate_contribution_all_files()

    def get_contents(self):

        def is_folder(file):
            return file.get('mimeType') == 'application/vnd.google-apps.folder'

        def in_folder(parent_id):
            return parent_id != self.id

        def get_files_not_in_folder():

            files_not_in_folder = []

            for file in files:
                for parent in file.get('parents'):
                    if not in_folder(parent):
                        files_not_in_folder.append(file)

            return files_not_in_folder

        def get_folders():

            folders_id_name = []

            for file in files:
                if is_folder(file) and not file.get('trashed'):
                    folders_id_name.append((file.get('id'), file.get('name')))

            return folders_id_name

        def get_drive_contents_excluding_files_not_in_folder():

            folders_and_their_contents = {}

            for file in files:
                if not is_folder(file) and not file.get('trashed'):
                    current_file = File(file, self.revision_api, self.change_api)

                    for parent in file.get('parents'):
                        if in_folder(parent):
                            if parent not in folders_and_their_contents:
                                folders_and_their_contents[parent] = []

                            folders_and_their_contents[parent].append(current_file)

            return folders_and_their_contents

        files = self.revision_api.get_files(self.id)

        if not files:
            return []
        else:

            folders_and_their_contents = get_drive_contents_excluding_files_not_in_folder()
            files_not_in_folder = get_files_not_in_folder()
            folders_id_name = get_folders()

            for folder in folders_id_name:
                folders_and_their_contents[folder[1]] = folders_and_their_contents.pop(folder[0])

            drive_contents = []

            for folder_name in folders_and_their_contents:
                current_folder = Folder(folder_name, folders_and_their_contents[folder_name])
                drive_contents.append(current_folder)

            for file_not_in_folder in files_not_in_folder:
                drive_contents.append(file_not_in_folder)

            return drive_contents

