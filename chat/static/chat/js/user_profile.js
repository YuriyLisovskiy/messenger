$(document).ready(function () {
    $('#btn-save-logo').attr('disabled', true);
    function readURL(input, upload_to) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (event) {
                $(upload_to).attr({
                    'display': 'block',
                    'src': event.target.result,
                    'width': '70%',
                    'height': 'auto'
                });
                $(upload_to).addClass('uploaded-photo');
            };
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#img-input-logo").change(function(){
        readURL(this, '#uploaded-photo-logo');
        $('#btn-save-logo').attr('disabled', false);
    });
    var photo_logo = $('.photo-logo');
    photo_logo.mouseover(function () {
        $('.logo').css('display', 'block');
    });
    photo_logo.mouseout(function () {
        $('.logo').css('display', 'none');
    });
    var msg_area = $('.msg-area');
    $('.send-message').mouseenter(function () {
        msg_area.show(500);
        msg_area.focus();

    });
    msg_area.blur(function () {
        $('.msg-area').hide(500);
    });
    msg_area.keypress(function(event){
      if(event.keyCode === 13) {
          event.preventDefault();
          if ($.trim(msg_area.val()).length !== 0) {
              $('#send-message-btn').click();
          }
      }
    });
});