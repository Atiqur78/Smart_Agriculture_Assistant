$(document).ready(function() {
    $('#send-btn').on('click', function() {
        sendMessage();
    });

    $('#user-input').on('keypress', function(e) {
        if (e.which === 13) {
            sendMessage();
        }
    });

    $('#record-btn').on('click', function() {
        toggleRecording();
    });

    var recording = false;
    var recorder;

    function toggleRecording() {
        if (recording) {
            stopRecording();
            $('#record-btn').text('Record');
        } else {
            startRecording();
            $('#record-btn').text('Stop Recording');
        }
        recording = !recording;
    }

    
    function startRecording() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(function(stream) {
                    recorder = new MediaRecorder(stream);
                    var chunks = [];
    
                    recorder.addEventListener('dataavailable', function(e) {
                        chunks.push(e.data);
                    });
    
                    recorder.addEventListener('stop', function() {
                        var audioBlob = new Blob(chunks, { type: 'audio/webm' });
                        var formData = new FormData();
                        formData.append('audio', audioBlob, 'audio.webm');
                        sendAudio(formData);
                    });
    
                    recorder.start();
                })
                .catch(function(err) {
                    console.error('Error accessing microphone:', err);
                });
        } else {
            console.error('getUserMedia is not supported in this browser.');
        }
    }


    function stopRecording() {
        if (recorder) {
            recorder.stop();
        }
    }

    function sendAudio(formData) {
        $('#chat-container').append('<div class="col-xs-12"><p class="loading-message">Uploading audio...</p></div>');
        scrollToBottom();

        $.ajax({
            url: '/chat',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                $('#chat-container .loading-message:last').remove();

                var transcription = response.text;
                $('#user-input').val(transcription);
                sendMessage();
            },
            error: function(xhr, status, error) {
                console.error('Error uploading audio:', error);
            }
        });
    }

    function sendMessage() {
        var userInput = $('#user-input').val();
        if (userInput.trim() !== '') {
            $('#user-input').val('');
            $('#chat-container').append('<div class="col-xs-12 text-right"><p class="alert alert-info">' + userInput + '</p></div>');
            scrollToBottom();

            $('#chat-container').append('<div class="col-xs-12"><p class="loading-message">Bot is typing...</p></div>');
            scrollToBottom();

            $.post('/chat', {text: userInput}, function(response) {
                $('#chat-container .loading-message:last').remove();

                $('#chat-container').append('<div class="col-xs-12 text-left"><p class="alert alert-success">' + response.text + '</p></div>');
                scrollToBottom();

                setVoice(response.voice);
                playNotificationSound();
                showNotification(response.text);
            });
        }
    }

    function setVoice(voiceFile) {
        var audio = document.getElementById('audio');
        audio.pause();
        audio.src = voiceFile;
        audio.load();
        audio.play();
    }

    function playNotificationSound() {
        var audio = new Audio("{{ url_for('static', filename='audio/sound.mp3') }}");
        audio.play();
    }

    function showNotification(message) {
        if (Notification.permission === "granted") {
            var notification = new Notification("New Message", {
                body: message,
                icon: "{{ url_for('static', filename='img/notification-icon.png') }}"
            });
        } else if (Notification.permission !== "denied") {
            Notification.requestPermission().then(function(permission) {
                if (permission === "granted") {
                    var notification = new Notification("New Message", {
                        body: message,
                        icon: "{{ url_for('static', filename='img/notification-icon.png') }}"
                    });
                }
            });
        }
    }

    function scrollToBottom() {
        $('#chat-container').scrollTop($('#chat-container')[0].scrollHeight);
    }
});