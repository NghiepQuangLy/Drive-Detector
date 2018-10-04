import google_api
import json
class REST_API(google_api.GOOGLE_API):
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

    def get_folders(self, parent_id):
        """
        Gets all the folders inside a folder/team drive

        :param parent_id: the id of the file to look for folders inside
        :return: a dictionary containing the folders of the specified folder/team drive
        """

        query = " trashed!=True and mimeType='application/vnd.google-apps.folder'"
        data_to_retrieve = "nextPageToken, files(id, name, mimeType, parents, trashed, capabilities, lastModifyingUser)"

        # get the folders of the folder/team drive
        results_folder = self.service.files().list(pageSize=1000, includeTeamDriveItems=True, corpora='teamDrive',
                                                   supportsTeamDrives=True, teamDriveId=parent_id,
                                                   q=query, fields=data_to_retrieve).execute()

        # convert the result into a dictionary data structure
        folders = results_folder.get('files', [])

        return folders

    def get_files_in_folder(self, folder_id):
        """
        Gets the first 1000 files in a folder

        :param folder_id: the folder id of the drive to look for files
        :return: a dictionary containing the files inside the specified team drive
        """

        query = "trashed!=True and '" + folder_id + "' in parents"
        data_to_retrieve = "nextPageToken, files(id, name, mimeType, parents, trashed, capabilities, lastModifyingUser)"

        # get the files in the folder
        results_file_in_folder = self.service.files().list(pageSize=1000, includeTeamDriveItems=True, supportsTeamDrives=True,
                                                           q=query, fields=data_to_retrieve).execute()

        # convert the result into a dictionary data structure
        files_in_folder = results_file_in_folder.get('files', [])

        return files_in_folder

    def get_files_not_in_folder(self, drive_id):
        """
        Gets the first 1000 files in a drive but are not in any folder of that drive

        :param drive_id: the drive id of the drive to look for files
        :return: a dictionary containing the files inside the specified team drive
        """

        query = "trashed!=True and '" + drive_id + "' in parents and mimeType!='application/vnd.google-apps.folder'"
        data_to_retrieve = "nextPageToken, files(id, name, mimeType, parents, trashed, capabilities, lastModifyingUser)"

        # get the files in the folder
        results_file_not_in_folder = self.service.files().list(pageSize=1000, includeTeamDriveItems=True, corpora='teamDrive',
                                                               supportsTeamDrives=True, teamDriveId=drive_id,
                                                               q=query, fields=data_to_retrieve).execute()

        # convert the result into a dictionary data structure
        files_not_in_folder = results_file_not_in_folder.get('files', [])

        return files_not_in_folder

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
