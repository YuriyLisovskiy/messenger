$(document).ready(function () {
    var album_id = 0;
    $('a[name="album"]').click(function (event) {
        event.preventDefault();
        var current_album = this.id;
        if (current_album !== album_id) {
            album_id = current_album;
            $('div[data-target]').slideUp();
            $('div[data-target="' + current_album + '"]').slideDown();
            get_songs(current_album);
        }
        else {
            $('div[data-target="' + current_album + '"]').slideUp();
            album_id = 0;
        }
    });
    function get_songs(album_id) {
        $.ajax({
            method: 'get',
            url: '/music_manager/',
            data: {
                'album_id': album_id
            },
            cache: false,
            success: function (response) {
                if (!response.error) {
                    var html = '<ul id="playlist">';
                    for (var key in response) {
                        html += js_object_to_html(response[key]);
                    }
                    html += '</ul>';
                    document.getElementById('playlist-area').innerHTML = html;
                }
                else {
                    document.getElementById('playlist-area').innerHTML = '<h4>Your playlist is empty</h4>';
                }
            },
            error: function () {
                console.log("Error occurred while getting songs of requested album.");
            }
        });
    }
    function js_object_to_html(song) {
        var html = '<li id="song">';
        html += '<button type="button" class="play-button" id="play-button" title="Play" disabled>';
        html += '<span id="play-span" class="glyphicon glyphicon-play" aria-hidden="true"></span>';
        html += '</button>';
        html += '<a name="song" href="' + song.source + '" data-song-name="' + song.artist + '-' + song.title + '">' + song.artist + ' - ' + song.title + '</a>';
        html += '</li>';
        return html;
    }
    $('#add-album').click(function (event) {
        event.stopPropagation();
        $('#all-form').slideDown();
        $('#submit').prop('disabled', false);
        $('.album-list').css('height', '180px');
    });
    $(document).click(function () {
        $('#all-form').slideUp(function () {
            $('.album-list').css('height', '350px');
        });
        $('#submit').prop('disabled', true);
    });
});