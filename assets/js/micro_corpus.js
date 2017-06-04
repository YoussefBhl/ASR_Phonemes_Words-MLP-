var minutesLabel = document.getElementById("minutes");
var secondsLabel = document.getElementById("seconds");
var millisecondsLabel = document.getElementById("milliseconds");
var totalmilliSeconds = 0;
var totalSeconds = 0;
var countup = null;
var result = 1 ;
var test = 15;
var phonemes_list = ['أ','ب','ت','ث','ج','ح','خ','د','ذ','ر','ز','س','ش','ص','ض','ط','ع','غ'
               ,'ف','ق','ك','ل','م','ن','ه','و','ي']
var phoneme_indice = 0;
var word_indice = 0;
var repeat = 2;
var words_list = ['أكل','شرب','قام','لعب','نام','الشمس','القمر','أب','أم','قط','كلب','القلم','الكتاب','تونس','أبيض']
var radios = document.getElementsByName('recognition_type');
var active_recorder = false; //
function __log(e, data) {
    log.innerHTML += "\n" + e + " " + (data || '');
  }

  var audio_context;
  var recorder;

  function startUserMedia(stream) {
    var input = audio_context.createMediaStreamSource(stream);

    // Uncomment if you want the audio to feedback directly
    //input.connect(audio_context.destination);
    //__log('Input connected to audio context destination.');

    recorder = new Recorder(input);
  }

  function startRecording(button) {
    recorder.clear();
    recorder && recorder.record();
    button.disabled = true;
    button.nextElementSibling.disabled = false;
    countup = setInterval(setTime, 1);
  }

  function stopRecording(button) {
    recorder && recorder.stop();
    button.disabled = true;
    button.previousElementSibling.disabled = false;
    clearInterval(countup);
     totalmilliSeconds = 0;
     totalSeconds = 0;
    // create WAV download link using audio data blob
    active_recorder = true;
  }



      function recognition(button) {
        if(active_recorder){
       // __log('resultat num '+ result +' : ');
        recorder && recorder.exportWAV(function(blob) {
        var fd = new FormData();
        fd.append('fname', 'test.wav');
        fd.append('data', blob);
            //send the wave file to the server
          $.ajax({type: 'POST',
           data: fd,
           url: 'savecorpus',
           processData: false,
           contentType: false
           }).done(function(data) {
                if(data == 'done'){
                    $('#count').fadeOut(500);
                    $('#msg').fadeOut(500);
                    $('#start').fadeIn(1000);}
           });
        });
        if(phoneme_indice < 27) {
            document.getElementById("phon").innerHTML = "'"+ phonemes_list[phoneme_indice] +"'";
            document.getElementById("iem").innerHTML = repeat.toString();
            if (repeat == 5){
                ++phoneme_indice;
                repeat = 0;
            }

        }
         else {
            document.getElementById("phon").innerHTML = "'"+ words_list[word_indice] +"'";
             document.getElementById("iem").innerHTML = repeat.toString();
            if (repeat == 5 ) {
                ++word_indice;
                repeat = 0;
            }

        }
        if(word_indice ==15 && repeat == 4){
            clearInterval(countup);
            totalmilliSeconds = 0;
            totalSeconds = 0;
            countup = setInterval(setTime, 1);
            $('#out').fadeOut(1);
            $('button').fadeOut(500);
            $('#in').fadeIn(1000);
        }


        recorder.clear();
        ++repeat;
        active_recorder = false;
        }
        else
        alert('Enregistrez votre voix puis cliquez sur le bouton SVP !');
  }

  window.onload = function init() {
    try {
      // webkit shim
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      navigator.getUserMedia = navigator.getUserMedia ||
                       navigator.webkitGetUserMedia ||
                       navigator.mozGetUserMedia ||
                       navigator.msGetUserMedia;
      window.URL = window.URL || window.webkitURL;

      audio_context = new AudioContext;

    } catch (e) {
      alert('No web audio support in this browser!');
    }

    navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
    });
  };
  function setTime()
        {
            ++totalmilliSeconds;
            millisecondsLabel.innerHTML = pad(totalmilliSeconds%1000);
            totalSeconds = parseInt(totalmilliSeconds/1000)
            secondsLabel.innerHTML = pad(totalSeconds%60);
            minutesLabel.innerHTML = pad(parseInt(totalSeconds/60));
        }

        function pad(val)
        {
            var valString = val + "";
            if(valString.length < 2)
            {
                return "0" + valString;
            }
            else
            {
                return valString;
            }
        }