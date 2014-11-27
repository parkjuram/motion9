$(document).on("pageshow", function() {
    var popup = setInterval(function(){
        $(".selector").popup("open");
        clearInterval(popup);
    },1);
});

