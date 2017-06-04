
   /* attach a submit handler to the form */
    /*this code check the inputs and sent the message to server*/
    $("#monform").submit(function(event) {
        var user = $('#user').val();
        var email = $('#email').val()
        var message = $('#message').val();
        var tel = $('#tel').val();
        var name_error = document.getElementById("name_error");
        var email_error1 = document.getElementById("email_error1");
        var message_error = document.getElementById("message_error");
        var email_error2 = document.getElementById("email_error2");
        var tel_error = document.getElementById("tel_error");
        var succ = document.getElementById("succ");
        var valide = true;
      /* stop form from submitting normally */
      if (user.length == 0) {
       name_error.style.display = "" ;
        valide=false;
    }
    else {
       name_error.style.display = "none" ;
    }
    if (email.length == 0) {
       email_error1.style.display = "" ;
        valide=false;
    }
    else {
        email_error1.style.display = "none" ;
        var i = 0;
        var at = false;

        var len = email.length;
        while (i < len-1 && !at){
            if(email[i] == '@'){
                at = true;
            }
            else{
                i++;
            }
        }
        if(!at){
            email_error2.style.display = "";
            valide=false;
        }
        else{
            var dote = false;
            while (i+1<len && !dote){
                if(email[i] == '.'){
                    dote = true;
                }
                else{
                    i++;
                }
            }
            if(!dote){
                email_error2.style.display = "";
                valide=false;
            }
            else {
                email_error2.style.display = "none";
            }
        }

    }
    if (message.length == 0) {
       message_error.style.display = "" ;
        valide=false;
    }
    else {
       message_error.style.display = "none" ;
    }
    if(tel.length != 0){

        var len = tel.length ;
        var i = 0;
        var notnombre = false;

        while (i<len && !notnombre){
            if(tel[i]>='0'&& tel[i]<='9'){
                i++;
            }
            else{
                notnombre = true;
            }
        }
        if(notnombre){
            tel_error.style.display = "" ;
            valide = false;
        }
        else{
            tel_error.style.display = "none" ;
        }
    }
    if(valide){
        /*send the message to the server*/
        succ.style.display = "" ;
        event.preventDefault();

      /* get the action attribute from the <form action=""> element */
      var $form = $( this ),
          url = "contact";
      /* Send the data using post with element id name and name2*/
      var posting = $.post( url, { name: user,email:email,tel:tel,message:message,validation:valide } );

      /* Alerts the results */
      posting.done();
        $('input[name="nom"]').val("");
        $('input[name="mail"]').val("");
        $('input[name="tel"]').val("");
        $('textarea[name="message"]').val("");
    }
    else {
        succ.style.display = "none" ;
        event.preventDefault();

      /* get the action attribute from the <form action=""> element */
      var $form = $( this ),
          url = "test";

      /* Send the data using post with element id name and name2*/
      var posting = $.post( url, { name: user,email:email,tel:tel,message:message,validation:valide } );

      /* Alerts the results */
      posting.done();
    }

    });
