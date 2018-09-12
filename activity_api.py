import datetime

def main(service, drive_id):
    """
    Prints information about the last 10 events that occurred the user's Drive.
    """

    # Call the Drive Activity API
    results = service.activities().list(source='drive.google.com',
        drive_ancestorId=drive_id, pageSize=10).execute()
    activities = results.get('activities', [])

    if not activities:
        print('No activity.')
    else:
        print('Recent activity:')
        for activity in activities:
            event = activity['combinedEvent']
            user = event.get('user', None)
            target = event.get('target', None)
            if user is None or target is None:
                continue
            time = datetime.datetime.fromtimestamp(
                int(event['eventTimeMillis'])/1000)
            print('{0}: {1}, {2}, {3} ({4})'.format(time, user['name'],
                event['primaryEventType'], target['name'], target['mimeType']))
