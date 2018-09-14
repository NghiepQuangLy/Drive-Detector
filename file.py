class File:
    def __init__(self, actions):
        self.contribution = {}
        self.timeline = []
        self.extract_data(actions)

    def calculate_contribution(self, user):
        try:
            self.contribution[user] = self.contribution[user] + 1
        except KeyError:
            self.contribution['user'] = 1

    def calculate_timeline(self, event, user):
        time = datetime.datetime.fromtimestamp(int(event['eventTimeMillis']) / 1000)
        self.timeline.append[(time, user)]

    def extract_data(self, actions):
        for action in actions:
            event = action['combinedEvent']
            user = event.get('user', None)
            if user is not None:
                self.calculate_contribution(user)
            else:
                user = ''
            self.calculate_timeline(event, user)

class Folder:
    def __init__(self, files):
        self.files = files
        self.contribution = {}
        self.calculate_contribution()

    def calculate_contribution(self):
        for file in files:
            for user in file.contribution:
                try:
                    self.contribution[user] = self.contribution[user] + 1
                except KeyError:
                    self.contribution[user] = 1
