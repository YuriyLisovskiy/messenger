$(document).ready(function () {
    var track = document.getElementById('track');
    var source = document.getElementById('source');
    var play_btn_span = $('#play-span');
    var mute_btn_span = $('#mute-span');
    var play_btn = $('#play-button');
    var mute_btn = $('#mute-button');
    var full_duration = $('#full-duration');
    var current_time = $('#current-time');
    var bar_size = 600;
    var bar = document.getElementById('default-bar');
    var progress_bar = document.getElementById('progress-bar');
    var playlist = $('#playlist');
    var update_time;
    var song_title = $('#song-title');
    var play_btn_span_current_song;

    track.addEventListener('durationchange', function () {
       var minutes = parseInt(track.duration / 60);
       var seconds = pad(parseInt(track.duration % 60));
       full_duration.html(minutes + ":" + seconds);
    });
    play_btn.click(play_pause);
    mute_btn.click(mute_unmute);
    bar.addEventListener('click', clicked_bar, false);

    function play_pause() {
        if (!track.paused && !track.ended) {
            track.pause();
            play_btn_span.attr('class', 'glyphicon glyphicon-play');
            play_btn_span_current_song.attr('class', 'glyphicon glyphicon-play');
            play_btn.attr('title', 'Play');
            window.clearInterval(update_time);
        }
        else {
            track.play();
            play_btn_span.attr('class', 'glyphicon glyphicon-pause');
            play_btn_span_current_song.attr('class', 'glyphicon glyphicon-pause');
            play_btn.attr('title', 'Pause');
            update_time = setInterval(update, 500);
        }
    }
    function mute_unmute() {
        if (track.muted) {
            track.muted = false;
            mute_btn_span.attr('class', 'glyphicon glyphicon-volume-up');
            mute_btn.attr('title', 'Mute');
        }
        else {
            track.muted = true;
            mute_btn_span.attr('class', 'glyphicon glyphicon-volume-off');
            mute_btn.attr('title', 'Unmute');
        }
    }
    function update() {
        if (!track.ended) {
            var played_minutes = parseInt(track.currentTime / 60);
            var played_seconds = pad(parseInt(track.currentTime % 60));
            current_time.html(played_minutes + ":" + played_seconds);
            var size = parseInt(track.currentTime * bar_size / track.duration);
            progress_bar.style.width = size + "px";
        }
        else {
            current_time.html("0:00");
            play_btn_span.attr('class', 'glyphicon glyphicon-play');
            progress_bar.style.width = 0;
            window.clearInterval(update_time);
        }
    }
    function pad(arg) {
        return (arg < 10) ? "0" + arg.toString() : arg;
    }
    function clicked_bar(event) {
        if (!track.ended) {
            var mouse_x = event.pageX - bar.offsetLeft;
            track.currentTime = mouse_x * track.duration / bar_size;
            progress_bar.style.width = mouse_x + "px";
        }
    }
    $(document).on('click', "#song-href", function (event) {
        event.preventDefault();
        source.src = this;
        song_title.html($(this).attr('data-song-name'));
        play_btn_span.attr('class', 'glyphicon glyphicon-pause');
        play_btn.attr('title', 'Pause');
        track.load();
        update_time = setInterval(update, 500);
        track.play();
        $('li[id="song"]').removeClass();
        $('li[id="song"]').find('span').attr('class', 'glyphicon glyphicon-play');
        $(this).parent().addClass('song-active');
        play_btn_span_current_song = $(this).parent().find('span');
        play_btn_span_current_song.attr('class', 'glyphicon glyphicon-pause');
    });
});
