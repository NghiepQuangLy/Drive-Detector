from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class API:

    def __init__(self, token, scope, name, version, api_name):
        self.token = token
        self.scope = scope
        self.name = name
        self.version = version
        self.api_name = api_name
        self.service = None

    def get_service(self):
        if self.service is None:
            store = file.Storage(self.token)
            creds = store.get()

            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets('credentials.json', self.scope)
                creds = tools.run_flow(flow, store)

            self.service = build(self.name, self.version, http=creds.authorize(Http()))

        return (self.service) # defensive programming
