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

        mixpanel.track_links("#btn-survey-result", event_namespace + "click btn-survey-result");
        mixpanel.track_links("#btn-survey-result-detail", event_namespace + "click btn-survey-result-detail");

        mixpanel.track_links("#btn-request-survey", event_namespace + "btn-request-survey");
        mixpanel.track_links("#btn-request-survey-finish", event_namespace + "click btn-request-survey-finish");

        mixpanel.track_links("#btn-product-detail", event_namespace + "click btn-product-detail");
        mixpanel.track_links("#btn-do-interest", event_namespace + "click btn-do-interest");
        mixpanel.track_links("#btn-undo-interest", event_namespace + "click btn-undo-interest");

        mixpanel.track_links("#btn-request-survey-again-start", event_namespace + "click btn-request-survey-again-start");
        mixpanel.track_links("#btn-request-more-info", event_namespace + "click btn-request-more-info");



    });
    
});