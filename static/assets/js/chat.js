function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCookie(key, value) {
    document.cookie = escape(key) + '=' + escape(value);
}

function getNumEnding(iNumber, aEndings) {
    var sEnding, i;
    iNumber = iNumber % 100;
    if (iNumber >= 11 && iNumber <= 19) {
        sEnding = aEndings[2];
    } else {
        i = iNumber % 10;
        switch (i) {
            case (1):
                sEnding = aEndings[0];
                break;
            case (2):
            case (3):
            case (4):
                sEnding = aEndings[1];
                break;
            default:
                sEnding = aEndings[2];
        }
    }
    return sEnding;
}

function activate_chat(team_id, channel_id, thread_id,) {
    $("div.chat-input").focus();

    var ws;

    function start_chat_ws() {
        ws = new WebSocket("ws://127.0.0.1:8888/" + team_id + "/"+ channel_id + "/"+ thread_id + "/");
        ws.onmessage = function (mesege) {
            var message_data = JSON.parse(mesege.data);
            // var date = new Date(message_data.timestamp * 1000);
            // var time = $.map([date.getHours(), date.getMinutes(), date.getSeconds()], function (val, i) {
            //     return (val < 10) ? '0' + val : val;
            // });
            $("div.dialog").append('<div class="sms"><p class="cms" style="margin-bottom: 0; ">'+ message_data.sender +' '+message_data.time+'</p>'+
                    '<p style="margin-bottom: 0; padding-left: 10px; font-size: .875rem;width: 450px;font-family: '+'Noto Sans'+';">'+message_data.text+'</p>'+

                '</div>');
        };


        // scroll_chat_window();
        //     number_of_messages["total"]++;
        //     if (message_data.sender == user_name) {
        //         number_of_messages["sent"]++;
        //     } else {
        //         number_of_messages["received"]++;
        //     }
        //     $("div.chat p.messages").html('<span class="total">' + number_of_messages["total"] + '</span> ' + getNumEnding(number_of_messages["total"], ["сообщение", "сообщения", "сообщений"]) + ' (<span class="received">' + number_of_messages["received"] + '</span> получено, <span class="sent">' + number_of_messages["sent"] + '</span> отправлено)');
        // }
        ws.onclose = function () {
            // Try to reconnect in 5 seconds
            setTimeout(function () {
                start_chat_ws()
            }, 5000);
        };
    }

    if ("WebSocket" in window) {
        start_chat_ws();
        // } else {
        //     $("form.message_form").html('<div class="outdated_browser_message"><p><em>Ой!</em> Вы используете устаревший браузер. Пожалуйста, установите любой из современных:</p><ul><li>Для <em>Android</em>: <a href="http://www.mozilla.org/ru/mobile/">Firefox</a>, <a href="http://www.google.com/intl/en/chrome/browser/mobile/android.html">Google Chrome</a>, <a href="https://play.google.com/store/apps/details?id=com.opera.browser">Opera Mobile</a></li><li>Для <em>Linux</em>, <em>Mac OS X</em> и <em>Windows</em>: <a href="http://www.mozilla.org/ru/firefox/fx/">Firefox</a>, <a href="https://www.google.com/intl/ru/chrome/browser/">Google Chrome</a>, <a href="http://ru.opera.com/browser/download/">Opera</a></li></ul></div>');
        //     return false;
    }

    function send_message() {
        var texts = document.getElementById("text");
        var txt = texts.textContent || texts.innerText;
        // if (textarea.val() == "") {
        //     return false;
        // }
        // if (ws.readyState != WebSocket.OPEN) {
        //     return false;
        // }
        ws.send(txt);
        document.getElementById('text').innerHTML = '';
    }

    $(document).on("click", "#input1", function () {
        send_message();
    });

    $("div#text").keydown(function (e) {``
        // Ctrl + Enter
        if (e.ctrlKey &&e.keyCode == 13) {
            send_message();
        }
    });

}
