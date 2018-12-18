gAnswers = []

$('#group-google-get').click(function(e) {
    handleClientLoad(e);
});

var CLIENT_ID = '8372100595-q7sv932tbof1ome2td9ktt0q4c02hvjd.apps.googleusercontent.com';
var API_KEY = 'AIzaSyAD4qydu6OTwsstN7LhbHCnJjcvF2Fjovs';
var DISCOVERY_DOCS = ["https://sheets.googleapis.com/$discovery/rest?version=v4"];
var SCOPES = "https://www.googleapis.com/auth/spreadsheets.readonly";

/**
*  On load, called to load the auth2 library and API client library.
*/

function handleClientLoad(e) {
    gapi.load('client:auth2', function() {
        gapi.client.init({
            apiKey: API_KEY,
            clientId: CLIENT_ID,
            discoveryDocs: DISCOVERY_DOCS,
            scope: SCOPES
        }).then(function () {
            // Listen for sign-in state changes.
            gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);
            
            // Handle the initial sign-in state.
            updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
        }, function(error) {
            alert(JSON.stringify(error.error.message));
        });
    });
}

/**
*  Called when the signed in status changes, to update the UI
*  appropriately. After a sign-in, the API is called.
*/
function updateSigninStatus(isSignedIn) {
    if (isSignedIn) {
        getSheets();
    } 
    else {
        gapi.auth2.getAuthInstance().signIn().catch( function(err) {
            var msg = err.error;
            console.log(msg);
            if( msg=="popup_closed_by_user" ) {
                alert("關屁關，趕快登入")
            }
            else if( msg=="popup_blocked_by_browser") {
                alert("請允許彈出式視窗歐，不會有垃圾廣告的您放心")
            }
        });
    }
}

/**
* Print the names and majors of students in a sample spreadsheet:
* https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
*/
function getSheets() {

    var link = $('#input-googlelink').val() || "https://docs.google.com/spreadsheets/d/1cInDMhG2fRZxVCBWC1UDrYxUsf6hGniKjvx6Yg90Y8U/";
    var table = $('#input-googletable').val() || "表單回應 1";
    console.log(link, table)
    gapi.client.sheets.spreadsheets.values.get({
        spreadsheetId: getSheetId(link),
        range: table,
    }).then(function(response) {
        alert("爬取完畢，請選擇對應欄位");
        var rows = response.result.values;
        var title = rows[0];
        gAnswers = rows.slice(1);                 
        ele = "<option selected disabled>---請選擇---</option>";
        for( var i=0; i<title.length; i++ ) {
            ele += '<option value="'+i+'">'+title[i]+'</option>'
        }
        $('#select-colname').html(ele);
        
    }, function(res) {
        console.log(res);
        if( res.result.error.status == "NOT_FOUND" ) {
            alert("表單連結錯誤");
        }
        else if( res.result.error.status == "INVALID_ARGUMENT" ) {
            alert("工作表名稱錯誤")
        }
        else if( res.result.error.status == "PERMISSION_DENIED") {
            alert("沒有開啟權限")
        }
        else {
            alert(JSON.stringify(res.result))
        }
    });
}

function getSheetId(url) {
    start = url.indexOf("spreadsheets/d/");
    path = url.substring(start+15);
    end = path.indexOf("/");
    id = path.substring(0, end)
    console.log(id);
    return id;
}

function getSheetColData() {
    var i = $('#select-colname').val();
    var colData = gAnswers.map( function(d) {
        return d[i]
    });
    return colData;
}