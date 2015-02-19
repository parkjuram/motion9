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
                    var i, item, innerHtml="";
//                    innerHtml += '<div class="page-container" style="background-color:#e6e9f2;">';
//                    innerHtml += '<div class="page-content">';
//                    innerHtml += '<div class="row">';
//                    innerHtml += '<div class="col-md-6 col-sm-12">';
//                    innerHtml += '<div class="portlet light">';
//                    innerHtml += '<div class="portlet-title">';
//                    innerHtml += '<div class="caption caption-md">';
//                    innerHtml += '<i class="icon-bar-chart theme-font-color hide"></i>';
//                    innerHtml += '<span class="caption-subject theme-font-color bold uppercase">분석 보고서 목록</span>';
//                    innerHtml += '</div>';
//                    innerHtml += ' <div style="text-align:right;">
//                    innerHtml += '<a href="'+reportFormUrl+'" target="_self" class="btn btn-lg red" style="font-size:11px; color:#FFFFFF !important;">보고서 신청</a>';
//                    innerHtml += '</div>';
//                    innerHtml += '</div>';
//                    innerHtml += '<div class="portlet-body">';
//                    innerHtml += '<div class="scroller" style="height: 305px;" data-always-visible="1" data-rail-visible1="0" data-handle-color="#D7DCE2">';
//                    innerHtml += '<div class="general-item-list">';
                      innerHtml += '<div class="content-title">분석 보고서 목록</div><div class="content-list">';
                    for( i in data.data ) {
                        item = data.data[i];
                        if ( item.is_analysis_finish ) {
                            item.created_display += "(완료)";
                            innerHtml += '<a id="btn-survey-result" onclick="mixpanel.track(\'WEB:click btn-survey-result\');" href="'+ getSurveyResultUrl(item.id) +'" target="_self" is-analysis-finish="'+
                                item.is_analysis_finish+'" >'+item.created_display+'</a>';
                        } else {
                            item.created_display += "(분석중)";
                            innerHtml += '<a target="_self" is-analysis-finish="'+
                                item.is_analysis_finish+'" >'+item.created_display+'</a>';
                        }
                        innerHtml += '<br/>';
                        innerHtml += '<div class="login-box-header"><h4 class="lined-heading-survey"><span></span></h4></div>';
                        innerHtml += '<div class="clearfix"></div>';
                    }
                    innerHtml += '</div><a id="btn-request-survey" onclick="mixpanel.track(\'WEB:click btn-request-survey\');" href="'+ getReportFormUrl() +'" target="_self"><div class="content-title" style="color : white; background-color : black;">보고서 신청</div></a>';

//                    for( i in data.data ) {
//                        item = data.data[i];
//                        innerHtml += '<a href="'+ getSurveyResultUrl(item.id) +'" target="_self" is-analysis-finish="'+
//                            item.is_analysis_finish+'" >'+item.display_name+'</a>';
//                        innerHtml += '<br/>';
//                        innerHtml += '<div class="login-box-header"><h4 class="lined-heading-survey"><span></span></h4></div>';
//                        innerHtml += '<div class="clearfix"></div>';
//                    }
//                    innerHtml += '</div><a href="'+ getReportFormUrl() +'" target="_self"><div class="content-title" style="color : white; background-color : black;">보고서 신청</div></a>';

                    $('#analysis-dialog').html(innerHtml);
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
        if (isUserLogin) {
            $("#analysis-dialog").dialog("open");
        } else {
            window.document.location = getLoginUrl();
        }
    });
});