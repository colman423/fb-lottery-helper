var legalList;
$('#check-google').change( function() {
    $('#options-google').toggle(100);
})

$('#form-grouptab').submit( function(e) {
    e.preventDefault();
    $('#submit-grouptab').addClass('disabled').text("爬取中，請至webdriver操作");
    
    var data  = {
        post_link: $('#input-postlink').val(),
        need_like: $('#check-like').prop('checked'),
        need_comment: $('#check-comment').prop('checked'),
        need_csv: $('#check-google').prop('checked'),
    }
    if( data.need_comment ) {
        data.comment_options = {
            text: $('#input-commenttext').val(),
            tag: $('#input-tagcount').val()
        }
    }
    if( data.need_csv ) {
        data.csv_options = {
            data: getSheetColData(),
            type: $('#select-colusage').val()
        }
    }

    console.log(data)
    $.ajax({
        url: '/scrapy',
        method: 'POST',
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function(data) {
            $('#submit-grouptab').text("爬取完畢！");
            console.log(data);
            legalList = data;
            ele = "";
            for( var i=0; i<data.length; i++ ) {
                d = data[i];
                url = "https://www.facebook.com"+d.url;
                ele += '<tr><th scope="row">'+(i+1)+'</th><td><a href="'+url+'" target="_blank">'+d.name+'</a></td>><td>'+d.comment+'</td><td>'+d.time+'</td></tr>'
            }
            $('#legal-list-content').html(ele);
            $('#legal-count').text(data.length);

        },
        error: function(a, b, c) {
            console.log(a, b, c)
            var msg = a.responseText;
            if( msg=="INVALID_FACEBOOK_URL" ) {
                alert("url放錯囉87")
            }
            if( msg.indexOf("needs to be in PATH")!=-1 ) {
                alert("Chrome Driver位置錯誤")
            }
        },
        complete: function() {    
            setTimeout(function() {
                $('#submit-grouptab').text("開始爬取抽獎名單").removeClass('disabled');
            }, 1000)
        }
    })
})

$('#btn-add-lottery').click( function() {
    var tmp = $('#lottery-input-hidden');
    lotteryInput = tmp.clone().removeClass('d-none').addClass('lottery-input').removeAttr('id')
    lotteryInput.appendTo('#lottery-input-wrapper');
});

$(document).on('click', '.btn-delete-lottery', function() {
    var lotteryInput = $(this).parents('.lottery-input');
    lotteryInput.remove();
})

$('#lottery-btn').click( function() {
    var prize = $.map( $('.lottery-input'), function(d) {
        var name = $(d).find('.input-lottery-name').val()
        var count = $(d).find('.input-lottery-count').val()
        return {'name': name, 'count': count};
    });
    data =  {
        'prize': prize,
        'legal_list': legalList
    }
    $.ajax({
        'url': '/lottery',
        'method': 'POST',
        'contentType': "application/json",
        'data': JSON.stringify(data),
        'success': function(res) {
            var ele = "";
            for( var i=0; i<res.length; i++ ) {
                console.log(res[i]);
                d = res[i];
                url = "https://www.facebook.com"+d.url;
                ele += '<tr><td>'+(i+1)+'</td><td><a href="'+url+'" target="_blank">'+d.name+'</a></td><td>'+d.comment+'</td><td>'+d.prize+'</td></tr>';
            }
            $('#winner-list-content').html(ele);
        },
        'error': function(err) {
            alert(err.responseText)
        } 
    })
})

$(document).ready( function() {
    $('#btn-add-lottery').click()
    // $('#check-google').trigger('change')
});