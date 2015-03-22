$(function (){

    var event_namespace = 'MOBILE:';
    // mixpanel event
    $(document).ready(function ($) {
        mixpanel.track_links("#btn-mypage", event_namespace + "Mypage");
        mixpanel.track_links("#btn-login", event_namespace + "Login");
        mixpanel.track_links("#btn-logout", event_namespace + "Logout");
        mixpanel.track_links("#btn-signup", event_namespace + "Signup");

        mixpanel.track_links("#btn-home", event_namespace + "Home");
        mixpanel.track_links("#btn-home-logo", event_namespace + "Home-by-logo");

        mixpanel.track_links("#btn-help", event_namespace + "Help");
        mixpanel.track_links("#btn-faq", event_namespace + "Faq");
        mixpanel.track_links("#btn-inquire", event_namespace + "QnA");

        mixpanel.track_links("#btn-survey-result", event_namespace + "Report");
        mixpanel.track_links("#btn-survey-result-detail", event_namespace + "Report_detail");

        mixpanel.track_links("#btn-request-survey", event_namespace + "Request_Report");
        mixpanel.track_links("#btn-request-survey-finish", event_namespace + "Finish_Request_Report");

        mixpanel.track_links("#btn-do-interest", event_namespace + "Interest");
        mixpanel.track_links("#btn-undo-interest", event_namespace + "Interest_Cancel");

        mixpanel.track_links("#btn-survey-list", event_namespace + "Report_List");

mixpanel.track_links("#btn-facebook-login-finish", event_namespace + "Login_FB");

        //mixpanel.track_links("#btn-request-survey-again-start", event_namespace + "click btn-request-survey-again-start");
        //mixpanel.track_links("#btn-request-more-info", event_namespace + "click btn-request-more-info");



    });
    
});