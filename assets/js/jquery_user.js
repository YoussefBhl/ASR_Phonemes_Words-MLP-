$( document ).ready(function() {
runslide();
    var clickedbt = 0;
    $('#newcopus').click(function(){
    $('#newcopus').fadeOut(1000);
    $('#oldcorpus').fadeOut(1000);
    $('#monform').fadeIn(1000);
        clickedbt = 1;

});
    $('#oldcorpus').click(function(){
    $('#newcopus').fadeOut(1000);
    $('#oldcorpus').fadeOut(1000);
        $('#monform').fadeIn(1000);
        clickedbt = 2;

});
     $("#monform").submit(function(event) {
         var user = $('#user').val();
         if (user.length == 0) {
       name_error.style.display = "" ;
        valide=false;
    }
    else {
       name_error.style.display = "none" ;
    }
    event.preventDefault();
    if(clickedbt == 2)
          url = "oldUser";
    else
        url = "newUser";
      /* get the action attribute from the <form action=""> element */
      var $form = $( this ),
          url;

      /* Send the data using post with element id name and name2*/
      var posting = $.post( url, { name: user} );

      /* Alerts the results */
      posting.done(function( data ) {
          if(data != "ok")
          alert(data);
          else{
              if(clickedbt==2)
              window.location.replace("recognition");
              else
                 window.location.replace("corpus");
              }
      });
     });
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