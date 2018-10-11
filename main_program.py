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
content_ids = []

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
        global content_ids
        content_ids.append(list(request.form.keys())[0].strip())
        return redirect(url_for('inside_drive_pie'))

    return render_template("user_account.html", account_data=json_account)


@app.route("/inside_drive_pie/", methods=["GET", "POST"])
def inside_drive_pie():

    global account_contents
    global content_ids

    if request.method == "POST":

        type = None

        if list(request.form.keys())[0].strip() == "Back":
            content_ids.pop()
            return redirect(url_for('user_account'))
        elif list(request.form.keys())[0].strip() == "Histogram":
            return redirect(url_for("inside_drive_histogram"))

        content_ids.append(list(request.form.keys())[0].strip())

        # have to check whether a file or a folder inside the drive was clicked
        for drive in account_contents:
            for object_in_drive in drive.contents:
                if object_in_drive.id == content_ids[len(content_ids) - 1]:
                    type = object_in_drive.type
                    break
            if type is not None:
                break

        # if a file was clicked
        if type == "file":
            return redirect(url_for('inside_file'))
        # if a folder was clicked
        elif type == "folder":
            return redirect(url_for('inside_folder'))

    json_drive = None
    for drive in account_contents:
        if drive.id == content_ids[len(content_ids) - 1]:
            json_drive = drive.to_json()
            break

    return render_template("inside_drive_pie.html", drive_data=json_drive)

@app.route("/inside_drive_histogram/", methods=["GET", "POST"])
def inside_drive_histogram():

    global account_contents
    global content_ids

    if request.method == "POST":

        type = None

        if list(request.form.keys())[0].strip() == "Back":
            content_ids.pop()
            return redirect(url_for('user_account'))
        elif list(request.form.keys())[0].strip() == "Pie":
            return redirect(url_for("inside_drive_pie"))

        content_ids.append(list(request.form.keys())[0].strip())

        # have to check whether a file or a folder inside the drive was clicked
        for drive in account_contents:
            for object_in_drive in drive.contents:
                if object_in_drive.id == content_ids[len(content_ids) - 1]:
                    type = object_in_drive.type
                    break
            if type is not None:
                break

        # if a file was clicked
        if type == "file":
            return redirect(url_for('inside_file'))
        # if a folder was clicked
        elif type == "folder":
            return redirect(url_for('inside_folder'))

    json_drive = None
    for drive in account_contents:
        if drive.id == content_ids[len(content_ids) - 1]:
            json_drive = drive.to_json()
            break

    return render_template("inside_drive_histogram.html", drive_data=json_drive)

@app.route("/inside_folder/", methods=["GET", "POST"])
def inside_folder():

    global account_contents
    global content_ids

    if request.method == "POST":

        if list(request.form.keys())[0].strip() == "Back":
            content_ids.pop()
            return redirect(url_for('inside_drive_pie'))

        content_ids.append(list(request.form.keys())[0].strip())

        return redirect(url_for('inside_file'))

    json_folder = None
    for drive in account_contents:
        for object_in_drive in drive.contents:
            if object_in_drive.id == content_ids[len(content_ids) - 1]:
                json_folder = object_in_drive.to_json()
                break
        if json_folder is not None:
            break

    return render_template("inside_folder.html", folder_data=json_folder)

@app.route("/inside_file", methods=["GET", "POST"])
def inside_file():

    global account_contents
    global content_ids

    if request.method == "POST":

        if list(request.form.keys())[0].strip() == "Back":
            content_ids.pop()
            parent = content_ids[len(content_ids) - 1]

            for drive in account_contents:
                if drive.id == parent:
                    return redirect(url_for('inside_drive_pie'))
                else:
                    for object_in_drive in drive.contents:
                        if object_in_drive.id == parent:
                            if object_in_drive.type == "folder":
                                return redirect(url_for('inside_folder'))
    else:
        file_json = None
        for drive in account_contents:
            for object_in_drive in drive.contents:
                if object_in_drive.type == "folder":
                    for files in object_in_drive.files:
                        if files.id == content_ids[len(content_ids) - 1]:
                            file_json = files.to_json()
                            break
                elif object_in_drive.type == "file":
                    if object_in_drive.id == content_ids[len(content_ids) - 1]:
                        file_json = object_in_drive.to_json()
                        break
            if file_json is not None:
                break

        return render_template("inside_file.html", file_data=file_json)

if __name__ == '__main__':
    startup()
    app.run(debug=True)
