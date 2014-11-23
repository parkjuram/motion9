$(function () {

    function wireDataWithForm(){
        var name  = $('#name'), email  = $('#email');

        FB.api('/me', function(response) {

            rr = response;

            console.log(response);
            console.log(response.email);

            email.val(response.email);
            emailCheck(email);
            name.val(response.last_name + response.first_name);

            if(response.gender == 'male'){
                $('#sex_m').attr('checked', 'checked');
            }else{
                $('#sex_f').attr('checked', 'checked');
            }
        });
    }

    function registerPageInit(response) {
        if (response.status === 'connected') {
            wireDataWithForm();
        } else if (response.status !== 'not_authorized') {

        }
    }

    var rr;

    console.log('ttt');

    $.ajaxSetup({ cache: true });
      $.getScript('//connect.facebook.net/ko_kr/all.js', function(){
        FB.init({
          appId: '1450591788523941',
          cookie: true,  // enable cookies to allow the server to access
          // the session
          xfbml: true,  // parse social plugins on this page
          version: 'v2.0' // use version 2.0
        });

         FB.getLoginStatus(registerPageInit);
      });



    $('.fb-join-btn').click(function(e){
        e.preventDefault();
        window.location = encodeURI("https://www.facebook.com/dialog/oauth?client_id=1450591788523941&redirect_uri=http://"+location.host+'/user/registration_page/?next='+next+"&response_type=token&scope=public_profile,email,user_friends");
    });

    function emailCheck(el){
       var email = el.val();
       if(email.length > 5 && email != '') {
           $.ajax({
               url: '/user/check/email/',
               dataType: 'json',
               async: true,
               type: 'POST',
               data: {email: email},
               success: function (data) {
                   if (data.exist == false && data.isValid == true && data.success == true) {
                       $('#joinBtn').attr('data-enable', true);
                       $('span.warning-message').hide();
                   } else {
                       $('#joinBtn').attr('data-enable', false);
                       $('span.warning-message').show();
                   }
               },
               error: function (jqXHR, textStatus, errorThrown) {
                   console.log(textStatus);
               }
           });
       }
    }

    $('#email').focusout(function(e){
       emailCheck($(this));
    });


});