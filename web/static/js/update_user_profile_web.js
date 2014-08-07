/**
 * Created by Juram-Park on 14. 8. 7.
 */
$(function(){
    $('#btn-update').click( function(e) {
        e.preventDefault();
        var update_form = document.update
        update_form.submit()
    })

    $('#btn-cancel').click( function(e) {
        e.preventDefault();
        location.href = url_mypage;
    })
});