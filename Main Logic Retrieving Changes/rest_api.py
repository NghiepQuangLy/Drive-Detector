import google_api

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
