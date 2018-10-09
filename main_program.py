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

account_contents = []
json_account = []
content_id = 0

@app.before_first_request
def startup():

    global account_contents
    global json_account

    # Prints all the files in a team drive as well as their revisions
    # Prints all activities in a team drive

    apis = {'rest':     rest_api.REST_API('token_REST.json', SCOPES_REST, 'drive', 'v3', 'rest'),
            'activity': activity_api.ACTIVITY_API('token_ACTIVITY.json', SCOPES_ACTIVITY, 'appsactivity', 'v1', 'activity')}

    # get all team drives of user
    team_drives = apis['rest'].get_team_drives()

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
        content_id = list(request.form.keys())[0].strip()
        return redirect(url_for('inside_drive'))

    return render_template("user_account.html", account_data=json_account)


@app.route("/inside_drive/", methods=["GET", "POST"])
def inside_drive():

    global account_contents
    global content_id

    if request.method == "POST":

        type = None

        if list(request.form.keys())[0].strip() == "Back":
            return redirect(url_for('user_account'))

        # have to check whether a file or a folder inside the drive was clicked
        for drive in account_contents:
            for object_in_drive in drive.contents:
                if object_in_drive.id == content_id:
                    type = object_in_drive.type
                    break
            if type is not None:
                break

        content_id = list(request.form.keys())[0].strip()

        # if a file was clicked
        if type == "file":
            return redirect(url_for('inside_file'))
        # if a folder was clicked
        elif type == "folder":
            return redirect(url_for('inside_folder'))

    json_drive = None
    for drive in account_contents:
        if drive.id == content_id:
            json_drive = drive.to_json()
            break

    return render_template("inside_drive.html", drive_data=json_drive)


if __name__ == '__main__':
    startup()
    app.run(debug=True)
