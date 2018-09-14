import google_api
import datetime

class ACTIVITY_API(google_api.API):

    def get_changes(self, file_id):
        """
        Prints information about the last 10 events that occurred the user's Drive.
        """

        # Call the Drive Activity API
        results = self.service.activities().list(source='drive.google.com', drive_fileId=file_id, pageSize=20).execute()
        activities = results.get('activities', [])
        return activities

    def print_changes(self, changes):
        print('\t------------------------------------------')

        if not changes:
            print('\tNo activity.')
        else:
            print('\t Recent activity:')
            print('\t', '{:30} {:25} {:10}'.format("Time", "User", "Action"))
            for change in changes:
                event = change['combinedEvent']
                user = event.get('user', None)
                target = event.get('target', None)
                if user is None or target is None:
                    continue
                time = datetime.datetime.fromtimestamp(
                    int(event['eventTimeMillis'])/1000)
                print('\t', time, '    {:25} {:10}'.format(user['name'], event['primaryEventType']))
