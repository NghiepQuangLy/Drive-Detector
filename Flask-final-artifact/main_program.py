import google_api
import rest_api
import activity_api
import file
import json
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

# If modifying these scopes, delete the file token_REST.json.
SCOPES_REST = 'https://www.googleapis.com/auth/drive.readonly'

# If modifying these scopes, delete the file token_ACTIVITY.json.
SCOPES_ACTIVITY = 'https://www.googleapis.com/auth/activity'

@app.route("/", methods=['GET', 'POST'])
def main():
    # Prints all the files in a team drive as well as their revisions
    # Prints all activities in a team drive

    # apis = {'rest':     rest_api.REST_API('token_REST.json',     SCOPES_REST,     'drive',        'v3', 'rest'),
    #         'activity': activity_api.ACTIVITY_API('token_ACTIVITY.json', SCOPES_ACTIVITY, 'appsactivity', 'v1', 'activity')}
    #
    # # get all team drives of user
    # team_drives = apis['rest'].get_team_drives()
    #
    # account_contents = []
    #
    # if team_drives:
    #     for team_drive in team_drives:
    #         current_drive = file.Drive(team_drive, apis['rest'], apis['activity'])
    #         account_contents.append(current_drive)
    #
    #
    # json_account = []
    #
    # for team_drive in account_contents:
    #     json_account.append(team_drive.to_json())
    with open("./account-data.json") as f:
        json_account = json.load(f)
    print(type(json_account))
    print(len(json_account))

    return render_template("server.html", account_data=json_account)


if __name__ == '__main__':
    app.run(debug=True)
