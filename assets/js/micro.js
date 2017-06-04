var minutesLabel = document.getElementById("minutes");
var secondsLabel = document.getElementById("seconds");
var millisecondsLabel = document.getElementById("milliseconds");
var totalmilliSeconds = 0;
var totalSeconds = 0;
var countup = null;
var result = 1 ;
var test = 15;
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
        __log('resultat num '+ result +' : ');
        recorder && recorder.exportWAV(function(blob) {
        var fd = new FormData();
        fd.append('fname', 'test.wav');
        fd.append('data', blob);
        if(radios[0].checked){
            link = 'analyze_phoneme'
        }
        else if (radios[1].checked){
            link = 'analyze_mot'}
        else{
            link = 'analyze_paragraphe'}
            //send the wave file to the server
          $.ajax({type: 'POST',
           data: fd,
           url: link,
           processData: false,
           contentType: false
           }).done(function(data) {
                __log(data);
           });
        });
        recorder.clear();
        ++result;
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