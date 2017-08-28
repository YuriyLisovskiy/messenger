$(document).ready(function () {
    $('#parameters').find('input').attr('disabled', true);
    var search_field = $('#search-field');
    search_field.focus();
    $('#search-btn').click(function search() {
        var search = $.trim(search_field.val());
        search_field.focus();
        if (search.length !== 0) {
            get_csrf_token();
            document.getElementById('result-block').innerHTML = waiting_for_response();
            search_field.val(search);
            if (!$('#check-parameters').prop('checked')) {
                $.ajax({
                    method: 'post',
                    url: '/search/',
                    data: {'search': search},
                    cache: false,
                    success: function (response) {
                        console.log("Search request '" + search + "' was sent to server.");
                        var html = "";
                        for (var key in response) {
                            html += js_object_to_html(key, response);
                        }
                        if (html.length === 0) {
                            html = '<p class="not-found">No users found</p>';
                        }
                        document.getElementById('result-block').innerHTML = html;
                        search_field.focus();
                    },
                    error: function () {
                        console.log("Error occurred!");
                        $.ajax(this);
                    }
                })
            }
            else {
                var city = $('#city').val();
                var country = $('#country').val();
                var birthday = $('#birthday').val();
                var gender = $('#gender').val();
                if (city && country && birthday && gender) {
                    $.ajax({
                        method: 'post',
                        url: '/search/',
                        data: {
                            'search': search,
                            'city': city,
                            'country': country,
                            'birthday': birthday,
                            'gender': gender
                        },
                        cache: false,
                        success: function (response) {
                            console.log("Search request '" + search + "' was sent to server.");
                            var html = "";
                            for (var key in response) {
                                html += js_object_to_html(key, response);
                            }
                            if (html.length === 0) {
                                html = '<p class="not-found">No users found</p>';
                            }
                            document.getElementById('result-block').innerHTML = html;
                            search_field.focus();
                        },
                        error: function () {
                            console.log("Error occurred!");
                            $.ajax(this);
                        }
                    })
                }
                else {
                    document.getElementById('result-block').innerHTML = '<p class="not-found">Incorrect input</p>';
                }
            }
        }
    });
    function js_object_to_html(key, response) {
        var user_id_current = user_id_global;
        if (response[key].id === user_id_current) {
            return "";
        }
        var html = '<div class="user-found">';
        html += '<a href="/user/' + response[key].id + '">';
        if (response[key].user_logo) {
            html += '<div class="user-img" style="background-image: url(' + response[key].user_logo + ')"></div>';
        }
        else {
            html += '<div class="user-img user-img-none">';
            html += '<span class="glyphicon glyphicon-user"></span>';
            html += '</div>';
        }
        html += '<p>'+ response[key].first_name + " " + response[key].last_name + '</p>';
        html += '</a>';
        html += '</div>';
        return html;
    }
    search_field.keypress(function(event){
      if(event.keyCode === 13) {
          event.preventDefault();
          if ($.trim(search_field.val()).length !== 0) {
              $('#search-btn').click();
          }
      }
    });
    function waiting_for_response() {
        var html = '<div class="waiting">';
        html += '<ul class="ul-list">';
        html += '<li></li>';
        html += '<li></li>';
        html += '<li></li>';
        html += '<li></li>';
        html += '<li></li>';
        html += '<li></li>';
        html += '</ul>';
        html += '</div>';
        return html;
    }
    $('#check-parameters').change(function(){
        if(this.checked) {
            $('#parameters').find('input').attr('disabled', false);
            $('#info').slideDown();
        }
        else {
            $('#parameters').find('input').attr('disabled', true);
            $('#info').slideUp();
            $('#city').val("");
            $('#country').val("");
            $('#birthday').val("");
            $('#gender').val("");
        }
    });
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