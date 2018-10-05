import google_api

class ACTIVITY_API(google_api.GOOGLE_API):
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
        results_activity = self.service.activities().list(source='drive.google.com', drive_fileId=file_id, pageSize=20).execute()

        # convert the result into a dictionary data structure
        activities = results_activity.get('activities', [])

        return activities
