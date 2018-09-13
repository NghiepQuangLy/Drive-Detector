import datetime

def get_changes(service, file_id):
    """
    Prints information about the last 10 events that occurred the user's Drive.
    """

    # Call the Drive Activity API
    results = service.activities().list(source='drive.google.com', drive_fileId=file_id, pageSize=20).execute()
    activities = results.get('activities', [])
    return activities

def print_changes(changes):
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
