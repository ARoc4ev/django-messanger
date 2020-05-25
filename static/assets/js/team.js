
$(document).ready(function () {

    $("#teams_s").click(
        function () {
            sendAjax();
            return false;
        }
    );
    $("#im").click(
        function () {
            ert();
            return false;
        }
    );


});

function ert() {
    let sendData = data = $('#myForm').serializeArray();
    // alert(sendData)
    if (sendData.length != 0) {
        $.ajax({
            url: 'http://127.0.0.1:8000/ims/',
            type: 'POST',
            data: {
                'sendData': JSON.stringify(sendData),
                'csrfmiddlewaretoken': getCookie('csrftoken'),

            },
            success: function (data) {


                try {
                       document.location.href = "http://127.0.0.1:8000/im/" + data.id_threadim + "/";

                } catch (err) {
                     $('#teams').append('<a href="/im/'+'/" style="color: black">'+
                        '<div class="traid">'+
                           ' <div class="traid_text">'+
                                '<div class="test44"><p style="margin-bottom: 0">{{ i.name }}</p>'+
                                    '<p class="size"'+
                                      ' style="margin: 0; font-size: 12px ; color: rgba(25,25,26,0.6)">Алексей'+
                                       ' Рочев: {{ i.text }} </p>'+
                             '   </div>'+


                    '        </div>'+
                      '  </div>'+
                    '</a>')


                }
            }
        })
    }
};


function sendAjax() {
    $.ajax({
        url: 'http://127.0.0.1:8000/tm/?format=json', //url страницы (action_ajax_form.php)
        type: "get", //метод отправки
        dataType: "html", //форbtnмат данных
        data: {},
        // Сеарилизуем объект

        success: function (response) { //Данные отправлены успешно
            result = JSON.parse(response);
            $("#teams").html("");


            for (index = 0, len = result.length; index < len; ++index) {
                $('#teams').append('<label><div class="" style=" width: 450px" align="left" >' +
                    ' <div class="team_blok" style="">' +
                    '<div style="display: flex">' +
                    '<p style="margin: 0; margin-left: 40px" ; class="cms">' + result[index].first_name + ' ' + result[index].last_name + '</p>' +
                    '<input  name="teams" value="' + result[index].id + '" style="margin-left: auto; margin-right: 20px; margin-top: 9px" type="checkbox"></input>' +
                    '</div>' +
                    '</div>' +
                    '</div>' +
                    '</label>'
                )
            }


        },
        error: function (response) { // Данные не отправлены
            $('#result_form').html('Ошибка. Данные не отправлены.');
        }
    });
}

document.querySelector('#search').oninput = function () {
    let val = this.value.trim();
    let elementicItems = document.querySelectorAll("#teams div div p")
    if (val != '') {
        elementicItems.forEach(function (elem) {
            if (elem.innerText.search(val) == -1) {
                $(elem).closest('label').hide();
            } else {
                $(elem).closest('label').show();
            }


        })


    } else {
        elementicItems.forEach(function (elem) {
            $(elem).closest('label').show();
        })
    }
}

