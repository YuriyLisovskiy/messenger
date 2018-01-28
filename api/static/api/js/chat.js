$(document).ready(function () {
    var chat_room_data;
    var msgs_amount = 0;
    var chat_room_button = $('button[class="user-icon"]');
    var ajax_request_interval;
    chat_room_button.bind("contextmenu", function (event) {
        event.preventDefault();
        $("#popup-chat-room").finish().toggle(100).css({
            top: event.pageY + "px",
            left: event.pageX + "px"
        });
        chat_room_data = this.name;
        $('#delete-dialog').click( function () {
            get_csrf_token();
            console.log(chat_room_data);
            $.ajax({
                method: 'delete',
                url: '/api/chat/manager',
                data: {
                    'delete_chat_room': chat_room_data
                },
                cache: false,
                success: function (response) {
                    console.log(response.success);
                    clearInterval(ajax_request_interval);
                    $('button[name=' + chat_room_data + ']').remove();
                    $('#popup-chat-room').remove();
                    document.getElementById('messages').innerHTML = '<p class="not-found">Chat</p>';
                    $('#message-form').css('visibility', 'hidden');

                },
                error: function () {
                    console.log("Error occurred while deleting chat room.");
                }
            })
        });
    });
    $(document).bind("mousedown", function (e) {
        if (!$(e.target).parents("#popup-chat-room").length > 0) {
            $("#popup-chat-room").hide(100);
        }
    });
    chat_room_button.click( function () {
        $('#message-form').css('visibility', 'visible');
        $('#message').focus();
        msgs_amount = 0;
        chat_room_data = this.name;
        ajax_request_interval = setInterval(check_for_new_msgs, 100);
    });
    function check_for_new_msgs() {
        $.ajax({
            method: 'get',
            url: '/api/chat/manager',
            data: {
                'msgs_amount': msgs_amount,
                'chat_room_data': chat_room_data
            },
            cache: false,
            success: function (response) {
                if (response.amount !== msgs_amount) {
                    refresh_msg_box();
                }
                if (response.amount === 0) {
                    document.getElementById('messages').innerHTML = '<p class="not-found">Chat history is empty</p>';
                }
            },
            error: function () {
                console.log("Error occurred while checking for new messages.");
            }
        });
    }
    function refresh_msg_box() {
        var scroll_chatlogs = $('.chatlogs');
        $.getJSON('/api/chat/manager', {'chat_room_data': chat_room_data}, function (response) {
            msgs_amount = response.data.length;
            var html = "";
            for (var i in response.data) {
                html += js_object_to_html(i, response.data);
            }
            document.getElementById('messages').innerHTML = html;
            scroll_chatlogs.scrollTop(scroll_chatlogs.prop("scrollHeight"));
        })
    }
    function js_object_to_html(i, response) {
        var html;
        var current_user = global_var_current_user;
        if (current_user === response[i].author) {
            html = '<div class="chat self">';
            if (response[i].author_logo) {
                html += '<a href="/account/user/id=' + response[i].author_id + '/"><div class="user-photo" style="background-image: url(' + response[i].author_logo + ')"></div></a>';
            }
            else {
                html += '<a href="/account/user/id=' + response[i].author_id + '/"><div class="user-data"><p>' + response[i].author_fn_ln + '</p></div></a>';
            }
            html += '<div class="chat-message">';
            html += '<p class="msg">' + response[i].msg + '</p>';
            html += '<p class="msg-time">' + response[i].time + '</p>';
            html += '</div>';
            html += '</div>';
        }
        else {
            html = '<div class="chat friend">';
            if (response[i].author_logo) {
                html += '<a href="/account/user/id=' + response[i].author_id + '/"><div class="user-photo" style="background-image: url(' + response[i].author_logo + ')"></div></a>';
            }
            else {
                html += '<a href="/account/user/id=' + response[i].author_id + '/"><div class="user-data"><p>' + response[i].author_fn_ln + '</p></div></a>';
            }
            html += '<div  class="chat-message">';
            html += '<p class="msg">' + response[i].msg + '</p>';
            html += '<p class="msg-time">' + response[i].time + '</p>';
            html += '</div>';
            html += '</div>';
        }
        return html;
    }
    $('#message-form').submit(function (event) {
        get_csrf_token();
        var textarea = $('#message');
        event.preventDefault();
        var message = $.trim(textarea.val());
        if (message.length !== 0) {
            document.getElementById('message').value = "";
            textarea.focus();
            $.ajax({
                method: 'POST',
                url: '/api/chat/manager',
                data: {
                    'msg': message,
                    'friend_id': chat_room_data
                },
                cache: false,
                success: function (response) {
                    console.log(response.status_message);
                },
                error: function () {
                    console.log("Error occurred while sending message.");
                }
            });
        }
    });
    $('#message').keypress(function(event){
      if(event.keyCode === 13) {
          event.preventDefault();
          var textarea = $('#message');
          var message = $.trim(textarea.val());
          if (message.length !== 0) {
              $('#send').click();
          }
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