gAnswers = []

$('#group-google-get').click(function(e) {
    if ( gapi.auth2.getAuthInstance().isSignedIn.get() ) {
        getSheets();
    }
    else {
        gapi.auth2.getAuthInstance().signIn().then( function() {
            getSheets();
        }).catch( function(err) {
            var msg = err.error;
            console.log(msg);
            if( msg=="popup_closed_by_user" ) {
                alert("關屁關，趕快登入");
            }
            else if( msg=="popup_blocked_by_browser") {
                alert("請允許彈出式視窗歐，不會有垃圾廣告的您放心");
            }
        });
    }
});

function getSheets() {

    var link = $('#input-googlelink').val();
    var table = $('#input-googletable').val();
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
        if( res.result.error.status == "NOT_FOUND" ) alert("表單連結錯誤");
        else if( res.result.error.status == "INVALID_ARGUMENT" ) alert("工作表名稱錯誤");
        else if( res.result.error.status == "PERMISSION_DENIED") alert("沒有開啟權限");
        else alert(JSON.stringify(res.result));
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
        return d[i];
    });
    return colData;
}