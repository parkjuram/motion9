$(function (){

    var event_namespace = 'MOBILE:';
    // mixpanel event
    $(document).ready(function ($) {
        mixpanel.track_links("#btn-mypage", event_namespace + "click btn-mypage");
        mixpanel.track_links("#btn-login", event_namespace + "click btn-login");
        mixpanel.track_links("#btn-logout", event_namespace + "click btn-logout");
        mixpanel.track_links("#btn-signup", event_namespace + "click btn-signup");

        mixpanel.track_links("#btn-home", event_namespace + "click btn-home");
        mixpanel.track_links("#btn-home-logo", event_namespace + "click btn-home-logo");

        mixpanel.track_links("#btn-help", event_namespace + "click btn-help");
        mixpanel.track_links("#btn-faq", event_namespace + "click btn-faq");
        mixpanel.track_links("#btn-inquire", event_namespace + "click btn-inquire");

        //mixpanel.track_links("#btn-survey-list", event_namespace + "click btn-survey-report-list");
    });
    
});