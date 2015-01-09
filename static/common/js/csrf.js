(function ($) {
 
    var cookieName = 'csrftoken';
    var xHeaderName = 'X-CSRFToken';
 
    var csrfSafeMethod = function (method) {
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    };
 
    var getCookie = function (cookie) {
        var cookieValue = null;
 
        try {
            cookieValue = document.cookie.split(';')
                .map(function (x) {
                    return x.trim().split('=');
                })
                .filter(function (x) {
                    return x[0] == cookie;
                })
                .map(function (x) {
                    return x[1];
                })[0];
        } catch (e) {
            console.error(e);
        }
        return cookieValue;
    };
 
    $.csrfAjaxSupport = function () {
        $.ajaxSetup({
            crossDomain: false,
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader(xHeaderName, getCookie(cookieName));
                }
            }
        });
    };
 
}(jQuery));