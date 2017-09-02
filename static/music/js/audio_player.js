$(document).ready(function () {
    var track = document.getElementById('track');
    var play_btn_span = $('#play-span');
    var mute_btn_span = $('#mute-span');
    var play_btn = $('#play-button');
    var mute_btn = $('#mute-button');
    var full_duration = $('#full-duration');
    var current_time = $('#current-time');

    track.addEventListener('durationchange', function () {
        var min = parseInt(track.duration/60);
        var sec = parseInt(track.duration%60);
        full_duration.html(min + ":" + sec);
    });

    play_btn.click(play_pause);
    mute_btn.click(mute_unmute);

    var update_time;

    function play_pause() {
        if (!track.paused && !track.ended) {
            track.pause();
            play_btn_span.attr('class', 'glyphicon glyphicon-play');
            play_btn.attr('title', 'Play');
            window.clearInterval(update_time);
        }
        else {
            track.play();
            play_btn_span.attr('class', 'glyphicon glyphicon-pause');
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
            var playes_minutes = parseInt(track.currentTime / 60);
            var playes_seconds = parseInt(track.currentTime % 60);
            if (playes_seconds > 9) {
                current_time.html(playes_minutes + ":" + playes_seconds);
            }
            else {
                current_time.html(playes_minutes + ":0" + playes_seconds);
            }
        }
        else {
            current_time.html("0:00");
            play_btn_span.attr('class', 'glyphicon glyphicon-play');
            window.clearInterval(update_time);
        }
    }
});
