/**
 * Created by kunbae_park on 2014. 7. 14..
 */

$(function(){
    var registerPageInit = function(response) {
        console.log(response);
        if (response.status === 'connected') {
            wireDataWithForm();
        } else if (response.status === 'not_authorized') {

        } else {

        }
    }


    function wireDataWithForm(){
        var name  = $('#name');
        var email  = $('#email');

        FB.api('/me', function(response) {

          email.val(response.email);
          name.val(response.last_name + response.first_name);

          if(response.gender == 'male'){
              $('#sex_m').attr('selected', 'selected');
          }else{
              $('#sex_f').attr('selected', 'selected');
          }

        });
    }

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
        window.location = encodeURI("https://www.facebook.com/dialog/oauth?client_id=1450591788523941&redirect_uri=http://"+location.host+'/user/mobile/registration_page'+"&response_type=token&scope=public_profile,email,user_friends");
    });

});

