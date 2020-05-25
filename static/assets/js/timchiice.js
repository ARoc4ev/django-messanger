$(document).ready(function () {

    $("#inv").click(
        function () {
            invitation2();
            return false;
        }
    );

    $(".mymagicoverbox").click(function () {
        document.getElementById('dwedf').innerHTML = '';
        document.getElementById('in').value = "";


    })
});

function invitation2() {
    $.ajax({
        url: 'http://127.0.0.1:8000/int/', //url страницы (action_ajax_form.php)
        type: "post", //метод отправки
        data: {
            'id': $('#efer').val(),
            'csrfmiddlewaretoken': getCookie('csrftoken'),

        },
        // Сеарилизуем объект

        success: function (response) {
            try {
                rrr = response.ok
                document.location.href = "http://127.0.0.1:8000/";
            } catch (err) {
                $('#dwedf').html(response.result);
            }


        },
        error: function (response) { // Данные не отправлены
            $('#result_form').html('Ошибка. Данные не отправлены.');
        }
    });
}