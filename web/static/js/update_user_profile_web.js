/**
 * Created by Juram-Park on 14. 8. 7.
 */
$(function(){
    var element = document.getElementById('addressLayer');
    $(element).jqm({modal:false});

    function closeDaumPostcode() {
        // iframe을 넣은 element를 안보이게 한다.
        element.style.display = 'none';
    }

    function showDaumPostcode() {
        new daum.Postcode({
            oncomplete: function(data) {
                // 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.
                // 우편번호와 주소 및 영문주소 정보를 해당 필드에 넣는다.
                $('#postalcode').val(data.postcode);
                $('#basicAddress').val(data.address);
                // iframe을 넣은 element를 안보이게 한다.
                $(element).jqmHide();
            },
            width : '100%',
            height : '100%'
        }).embed(element);



        $(element).jqmShow();
    }

    function closeDaumPostcode(){
        $(element).jqmHide();
    }

    $('#searchAddressBtn').click(function(e){
        showDaumPostcode();
    });

    $('#btn-update').click( function(e) {
        e.preventDefault();
        var update_form = document.update;
        update_form.submit();
    })

    $('#btn-cancel').click( function(e) {
        e.preventDefault();
        location.href = url_mypage;
    })
});