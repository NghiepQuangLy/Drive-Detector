import google_api
import rest_api
import activity_api
import file
import json
from flask import Flask, jsonify, render_template, request, redirect, url_for
app = Flask(__name__)

# If modifying these scopes, delete the file token_REST.json.
SCOPES_REST = 'https://www.googleapis.com/auth/drive.readonly'

# If modifying these scopes, delete the file token_ACTIVITY.json.
SCOPES_ACTIVITY = 'https://www.googleapis.com/auth/activity'

json_account = []

@app.before_first_request
def startup():

    global json_account

    # Prints all the files in a team drive as well as their revisions
    # Prints all activities in a team drive

    apis = {'rest':     rest_api.REST_API('token_REST.json', SCOPES_REST, 'drive', 'v3', 'rest'),
            'activity': activity_api.ACTIVITY_API('token_ACTIVITY.json', SCOPES_ACTIVITY, 'appsactivity', 'v1', 'activity')}

    # get all team drives of user
    team_drives = apis['rest'].get_team_drives()

    account_contents = []

    if team_drives:
        for team_drive in team_drives:
            current_drive = file.Drive(team_drive, apis['rest'], apis['activity'])
            account_contents.append(current_drive)

    for team_drive in account_contents:
        json_account.append(team_drive.to_json())


@app.route("/", methods=["GET", "POST"])
def user_account():
    global json_account

    if request.method == "POST":
        global content_id
        content_id = list(request.form.keys())[0]
        return redirect(url_for('inside_drive'))

    return render_template("server.html", account_data=json_account)


@app.route("/inside_drive/")
def inside_drive():
    return content_id

content_id = 0
if __name__ == '__main__':
    startup()
    app.run(debug=True)
