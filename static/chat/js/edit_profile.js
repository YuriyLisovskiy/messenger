$(document).ready(function () {
    var user_first_name = first_name;
    var user_last_name = last_name;
    var user_status = status;
    var user_city = city;
    var user_country = country;
    var user_birthday = b_year + "-" + b_month + "-" + b_day;
    var user_gender = gender;
    var user_education = education;
    var user_mobile = mobile;
    var user_about = about;

    $('#first_name').val(user_first_name);
    $('#last_name').val(user_last_name);
    $('#status').val(user_status);
    $('#city').val(user_city);
    $('#country').val(user_country);
    $('#birthday').val(user_birthday);
    if (user_gender === "Male") {
        $('#gender').prop("selectedIndex", 1);
    }
    else if (user_gender === "Female") {
        $('#gender').prop("selectedIndex", 2);
    }
    else {
        $('#gender').prop("selectedIndex", 3);
    }
    $('#education').val(user_education);
    $('#mobile_number').val(user_mobile);
    $('#about_me').text(user_about);
});