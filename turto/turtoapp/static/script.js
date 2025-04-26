let waveInterval;
let isRecording = false;

const sendTextToSpeech = async (text) => {
    const response = await fetch('/text-to-speech/', {
        method: 'POST',
        body: JSON.stringify({ text: text })
    });

    const data = await response.json();
    if (data.status === 'success') {
        console.log('Text was sent and converted to speech!');
    } else {
        alert('Error: ' + data.message);
    }
}

const startRecording = async () => {
    // Send request to start recording
    const response = await fetch('/start-recording/', { method: 'POST' });
    const data = await response.json();
    if (data.status === 'success') {
        isRecording = true;
        // recordButton.textContent = "Stop Recording";
    } else {
        alert("Error starting recording");
    }
};

const stopRecording = async () => {
    // Send request to stop recording
    const stop_record = await fetch('/stop-recording/', { method: 'POST' });
    const data = await stop_record.json();
    if (data.status === 'success') {
        const transcription = data.transcription;
        console.log('Transcription:', transcription);  // Show transcription or send it to the UI
        const container = document.getElementById('messageContainer');
        const newDiv = document.createElement('div');
        newDiv.className = 'user-text right-anchor';  // for optional styling
        newDiv.textContent = transcription;
        container.appendChild(newDiv);
        
        const response = await fetch('/response/', { method: 'POST', body: JSON.stringify({ user_message: transcription }) });
        const reply = await response.json();
        if (reply.status === 'success') {
            const respond = reply.respond;
            // console.log('Reply', respond);  // Show transcription or send it to the UI
            const container = document.getElementById('messageContainer');
            const newDiv = document.createElement('div');
            newDiv.className = 'bot-text left-anchor';  // for optional styling
            newDiv.textContent = respond;
            container.appendChild(newDiv);
            sendTextToSpeech(respond);
        }
    } else {
        alert("Error stopping recording");
    }
    isRecording = false;
    // recordButton.textContent = "Start Recording";
};

function startWaveAnimation() {
    const bars = document.querySelectorAll('#soundwave span');
    waveInterval = setInterval(() => {
        bars.forEach((bar, index) => {
            const randomHeight = Math.floor(Math.random() * 90) + 10;  // Between 10px and 40px
            const delay = index * 100;  // Stagger the changes between bars

            // Apply random height with a delay for a smoother wave effect
            setTimeout(() => {
                bar.style.height = `${randomHeight}px`;
            }, delay);
        });
    }, 100);  // Update every 500ms for smoothness
}

function stopWaveAnimation() {
    clearInterval(waveInterval);
}

function runRecord() {
    const wave = document.getElementById("soundwave");

    if (wave.classList.contains("show")) {
        wave.classList.remove("show");
        stopWaveAnimation();
        stopRecording();
    } else {
        wave.classList.add("show");
        startWaveAnimation();
        startRecording();
    }
}

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// document.getElementById("recordButton").addEventListener("click", function () {
//     fetch("/record/", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//             "X-CSRFToken": getCookie("csrftoken"),
//         },
//         body: JSON.stringify({ message: "start recording" }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log("Success:", data);
//     })
//     .catch(error => {
//         console.error("Error:", error);
//     });
// });
