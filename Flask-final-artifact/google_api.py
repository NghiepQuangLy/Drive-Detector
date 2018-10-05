from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class GOOGLE_API:
    """
    GOOGLE_API stores the information of a certain API belonging to GOOGLE API family:
        - token
        - permission scope
        - name
        - version
        - name
        - service

    Permission scopes of GOOGLE APIs: https://developers.google.com/identity/protocols/googlescopes
    """

    def __init__(self, token, scope, name, version, api_name):
        """
        Constructor of the GOOGLE_API class

        :param token:    name of the token established after the user logs in to their Google account
        :param scope:    permission scope of the token
        :param name:     name of the api
        :param version:  version of the api
        :param api_name: name of the api
        """

        self.token =        token
        self.scope =        scope
        self.name =         name
        self.version =      version
        self.api_name =     api_name
        self.service =      self.get_service()

    def get_service(self):
        """
        Gets the service of the api

        :return: service of the api
        """

        store = file.Storage(self.token)
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.scope)
            creds = tools.run_flow(flow, store)

        return build(self.name, self.version, http=creds.authorize(Http()))
