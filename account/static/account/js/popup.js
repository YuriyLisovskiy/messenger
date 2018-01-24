$(document).ready(function () {
    $(function() {
        // Popup open
        $('[data-popup-open]').on('click', function(e)  {
            $("html").css("overflow-y", "hidden");
            var targeted_popup_class = jQuery(this).attr('data-popup-open');
            $('[data-popup="' + targeted_popup_class + '"]').fadeIn(350);
            e.preventDefault();
        });

        // Popup close
        $('[data-popup-close]').on('click', function(e)  {
            $("html").css("overflow-y", "scroll");
            var targeted_popup_class = jQuery(this).attr('data-popup-close');
            $('[data-popup="' + targeted_popup_class + '"]').fadeOut(350);
            e.preventDefault();
        });
    });
});