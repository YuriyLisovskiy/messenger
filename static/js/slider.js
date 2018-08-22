$(document).ready(function () {
    var slideIndexLogo = 1;
    var slideIndexBackground = 1;
    showDivs(slideIndexLogo, "slide-item-logo");
    showDivs(slideIndexBackground, "slide-item-bg");
    $('#prev-logo').click(function () {
        showDivs(slideIndexLogo += -1, "slide-item-logo");
    });
    $('#next-logo').click(function () {
        showDivs(slideIndexLogo += 1, "slide-item-logo");
    });
    $('#prev-bg').click(function () {
        showDivs(slideIndexBackground += -1, "slide-item-bg");
    });
    $('#next-bg').click(function () {
        showDivs(slideIndexBackground += 1, "slide-item-bg");
    });

    function showDivs(n, show_div) {
        var i;
        var x = document.getElementsByClassName(show_div);
        if (x.length !== 0) {
            if (show_div === "slide-item-logo") {
                if (n > x.length) {
                    slideIndexLogo = 1;
                }
                if (n < 1) {
                    slideIndexLogo = x.length;
                }
                for (i = 0; i < x.length; i++) {
                    x[i].style.display = "none";
                }
                x[slideIndexLogo - 1].style.display = "block";
            }
            else if (show_div === "slide-item-bg") {
                if (n > x.length) {
                    slideIndexBackground = 1;
                }
                if (n < 1) {
                    slideIndexBackground = x.length;
                }
                for (i = 0; i < x.length; i++) {
                    x[i].style.display = "none";
                }
                x[slideIndexBackground - 1].style.display = "block";
            }
        }
    }
});