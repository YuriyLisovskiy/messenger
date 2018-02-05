$(document).ready(function () {
    var panel_search_field = $('#panel-search-field');
    var panel_search_result = $('#panel-search-result');
    panel_search_field.keyup(send_request);
    $('#panel-search-btn').click(send_request);
    $('body').click(function () {
        panel_search_result.hide();
    });
    $('#panel-search').click(function(event){
        event.stopPropagation();
    });
    panel_search_field.keypress(function(event){
        if(event.keyCode === 13) {
            event.preventDefault();
            send_request();
        }
    });
    function send_request() {
        var search = $.trim(panel_search_field.val());
        if (search.length !== 0) {
            get_csrf_token();
            $.ajax({
                method: 'post',
                url: '/search/people',
                data: {'search': search},
                cache: false,
                success: function (response) {
                    panel_search_result.show();
                    var html = "";
                    for (var i in response.data) {
                        html += js_object_to_html(i, response.data);
                    }
                    if (html.length === 0) {
                        html = '<p class="not-found">No users found</p>';
                    }
                    document.getElementById('panel-search-result').innerHTML = html;
                },
                error: function () {
                    console.log("Error occurred!");
                    $.ajax(this);
                }
            });
        }
        else {
            panel_search_result.hide();
        }
    }
    function js_object_to_html(i, response) {
        var user_id_current = user_id_global;
        if (response[i].id === user_id_current) {
            return "";
        }
        var html = '<div class="panel-user-found">';
        html += '<a href="/user/' + response[i].id + '">';
        if (response[i].logo) {
            html += '<div class="panel-user-img" style="background-image: url(' + response[i].logo + ')"></div>';
        }
        else {
            html += '<div class="panel-user-img user-img-none">';
            html += '<span class="glyphicon glyphicon-user"></span>';
            html += '</div>';
        }
        html += '<p>'+ response[i].first_name + " " + response[i].last_name + '</p>';
        html += '</a>';
        html += '</div>';
        return html;
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