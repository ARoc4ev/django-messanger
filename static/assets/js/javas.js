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




$(document).ready(function () {

    $(".mymagicoverbox").click(function () {
        $('#myfond_gris').fadeIn(300);
        var iddiv = $(this).attr("iddiv");
        $('#' + iddiv).fadeIn(300);
        $('#myfond_gris').attr('opendiv', iddiv);



        return false;
    });

    $('#myfond_gris, .mymagicoverbox_fermer').click(function () {
        var iddiv = $("#myfond_gris").attr('opendiv');
        $('#myfond_gris').fadeOut();
        $('#' + iddiv).fadeOut();


    });

});


function checkParams() {
    let text = $('#newtread').val();
    let treadname = $('#treadsms').val();

    if (text.length != 0 && treadname.length != 0) {
        $('#tread').removeAttr('disabled');
    } else {
        $('#tread').attr('disabled', 'disabled');
    }
}


$(document).ready(function () {


    $("#btn").click(
        function () {
            sendAjaxForm();
            return false;
        }
    );
    $("#tread").click(
        function () {
            sendAjaxForm2();
            return false;
        }
    );

});


function sendAjaxForm(csrftoken) {
    $.ajax({
        url: 'http://127.0.0.1:8000/ch/',
        type: "POST", //метод отправки
        dataType: "html", //форbtnмат данных
        data: {
            text: $('#newchanel').val(),
            csrfmiddlewaretoken: getCookie('csrftoken'),
            action: 'post'
        },
        // Сеарилизуем объект

        success: function (response) { //Данные отправлены успешно
            result = $.parseJSON(response);
            $('#channel_res').html('<div id=' + result.id + '>' +
                '<a href="/u/1/' + result.id + '/" class="boxx"><p class="m_b  size">' + result.name + '</p></a>' + '</div>')

            var iddiv = $("#myfond_gris").attr('opendiv');
            $('#myfond_gris').fadeOut();
            $('#' + iddiv).fadeOut();


        },
        error: function (response) { // Данные не отправлены
            $('#result_form').html('Ошибка. Данные не отправлены.');
        }
    });
}


function sendAjaxForm2(csrftoken) {
    $.ajax({
        url: 'http://127.0.0.1:8000/tr/', //url страницы (action_ajax_form.php)
        type: "POST", //метод отправки
        dataType: "html", //форbtnмат данных
        data: {
            name: $('#newtread').val(),
            text: $('#treadsms').val(),
            channel_id:$('#channel_id').val(),
            csrfmiddlewaretoken: getCookie('csrftoken'),
            action: 'post'
        },
        // Сеарилизуем объект

        success: function (response) { //Данные отправлены успешно
            result = $.parseJSON(response);
            $('#restread').html('<a href="/u/1/'+result.channel_id + '/'+ result.tread_id + '/" style="color: black">'+
                    '<div class="traid">'+
                        '<div class="traid_text">'+
                            '<div class="test44"><p style="margin-bottom: 0">'+ result.tread_name + '</p>'+
                                '<p class="size"'+
                                   'style="margin: 0; font-size: 12px ; color: rgba(25,25,26,0.6)">' + result.partner + ': '+ result.text + ' </p>'+
                            '</div>'+


                        '</div>'+
                    '</div>'+
                '</a>')

            var iddiv = $("#myfond_gris").attr('opendiv');
            $('#myfond_gris').fadeOut();
            $('#' + iddiv).fadeOut();


        },
        error: function (response) { // Данные не отправлены
            $('#result_form').html('Ошибка. Данные не отправлены.');
        }
    });
}