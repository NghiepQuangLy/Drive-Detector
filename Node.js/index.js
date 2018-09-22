const fs = require('fs');
const readline = require('readline');
const {google} = require('googleapis');

// If modifying these scopes, delete token.json.
const SCOPES = ['https://www.googleapis.com/auth/activity',
                'https://www.googleapis.com/auth/drive.metadata.readonly'];
const TOKEN_PATH = 'token.json';

// Load client secrets from a local file.
fs.readFile('credentials.json', (err, content) => {
  if (err) return console.log('Error loading client secret file:', err);
  // Authorize a client with credentials, then call the Google Drive Activity
  // API.
  authorize(JSON.parse(content), listActivity);
});

/**
 * Create an OAuth2 client with the given credentials, and then execute the
 * given callback function.
 * @param {Object} credentials The authorization client credentials.
 * @param {function} callback The callback to call with the authorized client.
 */
function authorize(credentials, callback) {
  const {client_secret, client_id, redirect_uris} = credentials.installed;
  const oAuth2Client = new google.auth.OAuth2(
      client_id, client_secret, redirect_uris[0]);

  // Check if we have previously stored a token.
  fs.readFile(TOKEN_PATH, (err, token) => {
    if (err) return getNewToken(oAuth2Client, callback);
    oAuth2Client.setCredentials(JSON.parse(token));
    callback(oAuth2Client);
  });
}

/**
 * Get and store new token after prompting for user authorization, and then
 * execute the given callback with the authorized OAuth2 client.
 * @param {google.auth.OAuth2} oAuth2Client The OAuth2 client to get token for.
 * @param {getEventsCallback} callback The callback for the authorized client.
 */
function getNewToken(oAuth2Client, callback) {
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
  });
  console.log('Authorize this app by visiting this url:', authUrl);
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  rl.question('Enter the code from that page here: ', (code) => {
    rl.close();
    oAuth2Client.getToken(code, (err, token) => {
      if (err) return console.error('Error retrieving access token', err);
      oAuth2Client.setCredentials(token);
      // Store the token to disk for later program executions
      fs.writeFile(TOKEN_PATH, JSON.stringify(token), (err) => {
        if (err) console.error(err);
        console.log('Token stored to', TOKEN_PATH);
      });
      callback(oAuth2Client);
    });
  });
}

/**
 * Lists the recent activity in your Google Drive.
 *
 * @param {google.auth.OAuth2} auth An authorized OAuth2 client.
 */
function listActivity(auth) {
  const service = google.appsactivity({version: 'v1', auth});
  service.activities.list({
    'source': 'drive.google.com',
    'drive.ancestorId': 'root',
    'pageSize': 10,
  }, (err, res) => {
    if (err) return console.error('The API returned an error: ' + err);
    const activities = res.data.activities;
    if (activities) {
      console.log('Recent activity:');
      activities.forEach((activity) => {
        const event = activity.combinedEvent;
        const user = event.user;
        const target = event.target;
        if (user && target) {
          const time = new Date(Number(event.eventTimeMillis));
          //console.log(`${time}: ${user.name}, ${event.primaryEventType}, ` +
          console.log(`${user.name},                ${event.primaryEventType},   ` +
              `${target.name}   `);
        }
      });
    }
  });
}
