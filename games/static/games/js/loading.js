var opts = {
  lines: 13 // The number of lines to draw
, length: 28 // The length of each line
, width: 14 // The line thickness
, radius: 42 // The radius of the inner circle
, scale: 0.25 // Scales overall size of the spinner
, corners: 1 // Corner roundness (0..1)
, color: '#ffffff' // #rgb or #rrggbb or array of colors
, opacity: 0.25 // Opacity of the lines
, rotate: 0 // The rotation offset
, direction: 1 // 1: clockwise, -1: counterclockwise
, speed: 1 // Rounds per second
, trail: 60 // Afterglow percentage
, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
, zIndex: 2e9 // The z-index (defaults to 2000000000)
, className: 'spinner' // The CSS class to assign to the spinner
, top: '100%' // Top position relative to parent
, left: '50%' // Left position relative to parent
, shadow: false // Whether to render a shadow
, hwaccel: false // Whether to use hardware acceleration
, position: 'absolute' // Element positioning
}

var spinner = null;
var spinner_div = 0;

spinner_div = $('#spinner').get(0);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


//exchange form
$('[id=loading-form]').on('submit', function (event) {
    event.preventDefault();
    $('[id=submit-button]').attr('disabled', 'disabled');
    $('[id=results]').hide();
    if (spinner == null) {
        spinner = new Spinner(opts).spin(spinner_div);
    } else {
        spinner.spin(spinner_div);
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        type: "POST",
        url: "",
        data: $(this).serialize(),

        success: function (data) {
            spinner.stop(spinner_div);
            $('[id=submit-button]').removeAttr('disabled');
            $('[id=results]').show();
            var exchange = "/games/exchange/" + data.e + "/"
            $('#results').html("<div class='col-md-6 col-md-offset-3 alert alert-success'>" + data.m + "<a id='exchange-link' href=''> Ver</a>" + "</div>");
            $('#exchange-link').attr({'href': exchange})
        },
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='col-md-6 col-md-offset-3 alert alert-danger'>Error: " + errmsg + "</div>");
        }
    });
});

//contact form
$('#loading-contact-form').on('submit', function (event) {
    event.preventDefault();
    $('#submit-button').attr('disabled', 'disabled');
    $('#results').hide();
    if (spinner == null) {
        spinner = new Spinner(opts).spin(spinner_div);
    } else {
        spinner.spin(spinner_div);
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        type: "POST",
        url: "",
        data: $(this).serialize(),

        success: function (data) {
            spinner.stop(spinner_div);
            $('#submit-button').removeAttr('disabled');
            $('#results').show();
            $('#results').html("<div class='col-md-6 col-md-offset-3 alert alert-success'>" + data.m + "</div>");
        },
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='col-md-6 col-md-offset-3 alert alert-danger'>Error: " + errmsg + "</div>");
        }
    });
});