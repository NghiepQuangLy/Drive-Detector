import google_api
import json

class REST_API(google_api.API):

    def get_team_drives(self):
        """
        Gets the first 10 team drives in the user's drive

        :return: a dictionary containing the team drives
        """

        # get the team drives of the user
        results_drive = self.service.teamdrives().list(pageSize=10).execute()

        # convert the result into a dictionary structure
        team_drives = json.loads(json.dumps(results_drive['teamDrives']))

        return team_drives

    def get_files(self, drive_id):
        """
        Gets the first 20 files in a team drive

        :param drive: the drive to look for files
        :return: a dictionary containing the files inside the specified team drive
        """

        # get the files in the drive
        results_file = self.service.files().list(pageSize=20, includeTeamDriveItems=True, corpora='teamDrive',
                                            supportsTeamDrives=True, teamDriveId=drive_id,
                                            fields="nextPageToken, files(id, name, mimeType, trashed, capabilities, lastModifyingUser)").execute()

        # convert the result into a dictionary data structure
        files = results_file.get('files', [])

        return files

    def get_revisions(self, file_id):
        """
        Gets all the available revisions of a file

        :param file: the file to look for revisions
        :return: a dictionary containing the revisions of the specified file
        """

        # get the revisions of the file
        results_revision = self.service.revisions().list(fileId=file_id,
                                                    fields="revisions(id, modifiedTime, lastModifyingUser)").execute()

        # convert the result into a dictionary data structure
        revisions = json.loads(json.dumps(results_revision['revisions']))

        return revisions
