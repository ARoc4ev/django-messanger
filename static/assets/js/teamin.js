




$(document).ready(function () {

    $("#inv").click(
        function () {
            invitation();
            return false;
        }
    );

  $(".mymagicoverbox").click(function () {
        document.getElementById('dwedf').innerHTML = '';
          document.getElementById('in').value = "";




  })
});

function invitation() {
    $.ajax({
        url: 'http://127.0.0.1:8000/in/', //url страницы (action_ajax_form.php)
        type: "post", //метод отправки
        data: {
                'email': $('#in').val(),
                'csrfmiddlewaretoken': getCookie('csrftoken'),

            },
        // Сеарилизуем объект

        success: function (response) {
            $('#dwedf').html(response.result);


        },
        error: function (response) { // Данные не отправлены
            $('#result_form').html('Ошибка. Данные не отправлены.');
        }
    });
}