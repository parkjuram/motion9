/**
 * Created by Park-Kunbae on 14. 3. 31.
 */

$(function () {

    function openWithoutReferrer(url) {
        var site = window.open("", "_blank");
        site.location.href = "javascript:location.replace('" + url + "')";
    }

    // Open links with "hide-referrer" class without sending the referrer
    $(document).on('click', 'a.hide-referrer', function (e) {
        e.preventDefault();
        openWithoutReferrer($(this).attr('href'));
    });

    $('.right-tooltip').tooltip({position: {
        my: "left",
        at: "right",
        track: false,
        using: function (position, feedback) {
            $(this).css(position);
        }
    }, tooltipClass: "ui-right-tooltip"});

    $('.left-tooltip').tooltip({position: {
        my: "right",
        at: "left",
        track: false,
        using: function (position, feedback) {
            $(this).css(position);
        }
    }, tooltipClass: "ui-left-tooltip"});

    $(document).ready(function ($) {
        var options = {
            $FillMode: 2,                                       //[Optional] The way to fill image in slide, 0 stretch, 1 contain (keep aspect ratio and put all inside slide), 2 cover (keep aspect ratio and cover whole slide), 4 actual size, 5 contain for large image, actual size for small image, default value is 0
            $AutoPlay: true,                                    //[Optional] Whether to auto play, to enable slideshow, this option must be set to true, default value is false
            $AutoPlayInterval: 4000,                            //[Optional] Interval (in milliseconds) to go for next slide since the previous stopped if the slider is auto playing, default value is 3000
            $PauseOnHover: 1,                                   //[Optional] Whether to pause when mouse over if a slider is auto playing, 0 no pause, 1 pause for desktop, 2 pause for touch device, 3 pause for desktop and touch device, default value is 1

            $ArrowKeyNavigation: true,   			            //[Optional] Allows keyboard (arrow key) navigation or not, default value is false
            //$SlideEasing: $JssorEasing$.$EaseOutQuint,          //[Optional] Specifies easing for right to left animation, default value is $JssorEasing$.$EaseOutQuad
            $SlideDuration: 800,                               //[Optional] Specifies default duration (swipe) for slide in milliseconds, default value is 500
            $MinDragOffsetToSlide: 20,                          //[Optional] Minimum drag offset to trigger slide , default value is 20
            //$SlideWidth: 600,                                 //[Optional] Width of every slide in pixels, default value is width of 'slides' container
            //$SlideHeight: 300,                                //[Optional] Height of every slide in pixels, default value is height of 'slides' container
            $SlideSpacing: 0, 					                //[Optional] Space between each slide in pixels, default value is 0
            $DisplayPieces: 1,                                  //[Optional] Number of pieces to display (the slideshow would be disabled if the value is set to greater than 1), the default value is 1
            $ParkingPosition: 0,                                //[Optional] The offset position to park slide (this options applys only when slideshow disabled), default value is 0.
            $UISearchMode: 1,                                   //[Optional] The way (0 parellel, 1 recursive, default value is 1) to search UI components (slides container, loading screen, navigator container, arrow navigator container, thumbnail navigator container etc).
            $PlayOrientation: 1,                                //[Optional] Orientation to play slide (for auto play, navigation), 1 horizental, 2 vertical, 5 horizental reverse, 6 vertical reverse, default value is 1
            $DragOrientation: 1,                                //[Optional] Orientation to drag slide, 0 no drag, 1 horizental, 2 vertical, 3 either, default value is 1 (Note that the $DragOrientation should be the same as $PlayOrientation when $DisplayPieces is greater than 1, or parking position is not 0)

            $BulletNavigatorOptions: {                          //[Optional] Options to specify and enable navigator or not
                $Class: $JssorBulletNavigator$,                 //[Required] Class to create navigator instance
                $ChanceToShow: 2,                               //[Required] 0 Never, 1 Mouse Over, 2 Always
                $AutoCenter: 1,                                 //[Optional] Auto center navigator in parent container, 0 None, 1 Horizontal, 2 Vertical, 3 Both, default value is 0
                $Steps: 1,                                      //[Optional] Steps to go for each navigation request, default value is 1
                $Lanes: 1,                                      //[Optional] Specify lanes to arrange items, default value is 1
                $SpacingX: 8,                                   //[Optional] Horizontal space between each item in pixel, default value is 0
                $SpacingY: 8,                                   //[Optional] Vertical space between each item in pixel, default value is 0
                $Orientation: 1                                 //[Optional] The orientation of the navigator, 1 horizontal, 2 vertical, default value is 1
            },

            $ArrowNavigatorOptions: {                           //[Optional] Options to specify and enable arrow navigator or not
                $Class: $JssorArrowNavigator$,                  //[Requried] Class to create arrow navigator instance
                $ChanceToShow: 1,                               //[Required] 0 Never, 1 Mouse Over, 2 Always
                $AutoCenter: 2,                                 //[Optional] Auto center arrows in parent container, 0 No, 1 Horizontal, 2 Vertical, 3 Both, default value is 0
                $Steps: 1                                       //[Optional] Steps to go for each navigation request, default value is 1
            }
        };
        var jssor_slider1 = new $JssorSlider$('slider1_container', options);

        function ScaleSlider() {
            var bodyWidth = document.body.clientWidth;
            if (bodyWidth)
                jssor_slider1.$SetScaleWidth(Math.min(bodyWidth, 1920));
            else
                window.setTimeout(ScaleSlider, 30);
        }

        ScaleSlider();

        if (!navigator.userAgent.match(/(iPhone|iPod|iPad|BlackBerry|IEMobile)/)) {
            $(window).bind('resize', ScaleSlider);
        }
    });


    var fixDiv = function () {
        var b = $(window).scrollTop();
        var d = $("#header").offset().top + 80;
        var c = $("#nav-top-btn");
        if (b > d) {
            c.css({position: "fixed", top: "90%", display: "block"});
        } else {
            c.css({position: "absolute", top: "0px", display: 'none'});
        }
    };

    $(window).scroll(fixDiv);

    $('.login-box, .login-form').keypress(function (e) {
        if (e.keyCode == 13) {
            $(this).find('form').submit();
        }
    });


    $('.login-submit-btn').click(function (e) {
        e.preventDefault();

        var isEnable = $(this).attr('data-enable');

        if (isEnable && isEnable == 'false') {
            alert('이메일을 확인하세요.');
        } else {
            var formType = $(this).attr('data-form');
            var form = $('form').filter(function () {
                return $(this).attr('data-form') == formType;
            });

            var formType = $(this).attr('data-form');
            var form = $('form').filter(function () {
                return $(this).attr('data-form') == formType;
            });

            form.submit();
        }


    });

    $('#loginBox').jqm({modal: false});
    $('.login-btn').click(function (e) {
        e.preventDefault();
        $('#loginBox').jqmShow();


    });

    function loginCheck(email) {
        $.ajax({
            url: "/user/logincheck/",
            dataType: 'json',
            async: true,
            type: 'POST',
            data: {email: email},
            success: function (data) {
                if (data == 'valid')
                    location.href = 'login success url';
                else
                    location.href = '/user/registration_page';
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(textStatus);
            }
        });
    }


    function fbLoginCallback(response) {
        if (response.status === 'connected') {
            FB.api('/me', function (user_info) {
                $('#fbEmail').val(user_info.email);
                $('#fbToken').val(response.authResponse.accessToken);
                $('#facebookLoginForm').submit();
            });
        } else if (response.status === 'not_authorized') {
            window.location = encodeURI("https://www.facebook.com/dialog/oauth?client_id=1450591788523941&redirect_uri=http://" + location.host + '/user/registration_page/?next=' + next + "&response_type=token&scope=public_profile,email,user_friends");

            /*
             FB.login(function(response) {
             if (response.status === 'connected') {
             // Logged into your app and Facebook.
             console.log('logged in');
             } else if (response.status === 'not_authorized') {
             // The person is logged into Facebook, but not your app.
             console.log('facebook logged in but not the app');
             } else {
             // The person is not logged into Facebook, so we're not sure if
             // they are logged into this app or not.
             console.log('wtff');
             }
             }, {scope: 'public_profile,email,user_friends'});
             */
        } else {
            FB.login(function (response) {
                if (response.authResponse) {
                    FB.api('/me', function (user_info) {
                        $('#fbEmail').val(user_info.email);
                        $('#fbToken').val(response.authResponse.accessToken);
                        $('#facebookLoginForm').submit();
                    });
//                    console.log('Welcome!  Fetching your information.... ');
//                    FB.api('/me', function(response) {
//                        console.log('Good to see you, ' + response.name + '.');
//                    });
                } else {
//                    console.log('User cancelled login or did not fully authorize.');
                }
            }, {scope: 'public_profile,email,user_friends' });
//            alert('페이스북에 로그인을 먼저 해주세요.');
            // The person is not logged into Facebook, so we're not sure if
            // they are logged into this app or not.
        }
    }


    $('.fb-login-btn').click(function (e) {
        e.preventDefault();

        FB.getLoginStatus(fbLoginCallback);
    });


    var subMenuInitialize = function () {

        $('.header-sub-menu').removeClass('header-sub-menu-selected');

        var selectedMainMenu = $('#header-main-menu-list a').filter(function () {
            return $(this).hasClass('selected');
        }).attr('data-attr');

        $('#' + selectedMainMenu).addClass('header-sub-menu-selected');
    };

    var mainMenuSelection = function () {
        var menuLinks = $('#header-main-menu-list a');
        menuLinks.click(function (e) {
            e.preventDefault();

            if ($(this).attr('data-directly') == 'true')
                location.href = $(this).attr('href');

            // before 2014-07-30 front
//            menuLinks.removeClass('selected');
//            $(this).addClass('selected');
//            subMenuInitialize();
            // before 2014-07-30 end

            // after 2014-07-30 front

            if ($('#header-main-menu-list a.selected').attr('data-attr') == $(this).attr('data-attr')) {
                menuLinks.removeClass('selected');
                subMenuInitialize();
            } else {
                menuLinks.removeClass('selected');
                $(this).addClass('selected');
                subMenuInitialize();
            }
            // after 2014-07-30 end
        });

        $('#headerSearchBtn').click(function (e) {
            e.preventDefault();
            menuLinks.removeClass('selected');
            subMenuInitialize();
            $('#headerSearch').addClass('header-sub-menu-selected');
        });
    };

    subMenuInitialize();
    mainMenuSelection();
});


$(document).ready(function () {
    $("#analysis-dialog").dialog({
        dialogClass: 'notitle-dialog',
        autoOpen: false,
        modal: true,
        height: 800,
        width: 500,
        open: function (ev, ui) {
            $.ajax({
                url: surveyListInJsonUrl,
                dataType: 'json',
                data: {
                    csrfmiddlewaretoken: csrfToken
                },
                async: true,
                type: 'post',
                success: function (data, textStatus, jqXHR) {
                    for( i in data.data ) {
                        console.log(data.data[i]);
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                },
                complete: function (jqXHR, textStatus) {
                }
            });
            jQuery('.ui-widget-overlay').bind('click', function () {
                jQuery('#analysis-dialog').dialog('close');
            });
        }
    });

    $("#btn-survey-list").click(function () {
        $("#analysis-dialog").dialog("open");
    });
});