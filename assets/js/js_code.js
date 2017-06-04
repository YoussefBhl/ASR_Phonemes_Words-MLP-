
$( document ).ready(function() {
runslide();
function runslide() {
    $('#bienV').fadeIn(1500).delay(1500).fadeOut(1500, function () {
        $('#image').fadeIn(1500).delay(1500).fadeOut(1500, function () {
            $('#appName').fadeIn(1500).delay(1500).fadeOut(1500, function () {
                runslide();
            });
        });
    });
}


});