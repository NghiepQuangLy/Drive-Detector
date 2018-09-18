import google_api

class ACTIVITY_API(google_api.API):

    def get_changes(self, file_id):
        """
        Prints information about the last 10 events that occurred the user's Drive.
        """

        # Call the Drive Activity API
        results = self.service.activities().list(source='drive.google.com', drive_fileId=file_id, pageSize=20).execute()
        activities = results.get('activities', [])
        return activities
