$(document).ready(function () {
    var generated_code;
    $('#register').click(function register() {
        var received_code = document.getElementById('received-code');
        if (!received_code.value) {
            $('#received-code-content').show(400);
            document.getElementById('content-register').style.height = "850px";
            generated_code = Math.random().toString(36).slice(2);
            send_code(
                generated_code,
                document.getElementById('email').value,
                document.getElementById('password').value,
                document.getElementById('username').value);
        }
    });
    function send_code(code, email, password, username) {
        get_csrf_token();
        $.ajax({
                method: 'GET',
                url: '/api/send/email',
                dataType: 'json',
                data: {
                    generated_code: code,
                    user_email: email,
                    password: password,
                    username: username
                },
                cache: false,
                success: function (response) {
                    if (response.error_code === "222") {
                        alert("Error message: " + response.name);
                        $('#received-code-content').hide();
                    }
                    else {
                        console.log("Code for verification has been sent successfully!");
                    }
                },
                error: function () {
                    alert("Error occurred while sending code for verification!");
                }
        });
    }
    function get_csrf_token() {
        function getCookie(name)
            {
                var cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });
    }
});