let waveInterval;
let isRecording = false;

window.onload = () => {
    initialConversation();
};

async function initialConversation() {
    const response = await fetch('/start/');
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
        } else {
            showError('Failed to load initial message.');
        }
}

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

const recordBtn = document.getElementById('recordButton');
const submitBtn = document.getElementById('submitButton');
const container = document.getElementById('messageContainer');
const loader = document.getElementById('loader');
const typedText = document.getElementById('typedText');
const cursor = document.getElementById('cursor');
const modal = document.getElementById("errorModal");
const okButton = document.getElementById("okButton");
const closeButton = document.getElementsByClassName("close")[0];

let typingText = 'Loading...';
let typingIndex = 0;
let typingInterval = null;

// List of different loading GIF URLs
const gifList = [
    'https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2hnbHl4ZThreXdyYmhmZGRoNWlyejFzb3JvcWM1anp5ajZqbnJxMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/HRPlCNxx9fprIHgtXu/giphy.gif',
    'https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTFoM2wxMW05YzU3bGk2aWFrYnJrY3gydmFqcDBwdnM5NjdqZmU3MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/0DLrjGAPs3oh4ouLzD/giphy.gif',
    'https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnVka3FueDk0c24zeWMxaHduY29ueGphM3o2MTNtOXFkeTVqc2Y3cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YkMf8py6XfaY9mrzgD/giphy.gif',
    'https://media.giphy.com/media/Ojdmcky6EgFt8yFTkS/giphy.gif?cid=ecf05e47s7h881xgz53tjqldog04ehd9ykz9m22b5baj71ot&ep=v1_gifs_search&rid=giphy.gif&ct=g'
];

function showRandomGif() {
    const randomIndex = Math.floor(Math.random() * gifList.length);
    loaderGif.src = gifList[randomIndex];
}

function startTypingAnimation() {
    typedText.textContent = ''; // clear previous
    typingIndex = 0;
    
    typingInterval = setInterval(() => {
        if (typingIndex < typingText.length) {
            typedText.textContent += typingText[typingIndex];
            typingIndex++;
        } else {
            clearInterval(typingInterval); // Stop typing when done
        }
    }, 150); // typing speed: 150ms per letter
}

function stopTypingAnimation() {
    clearInterval(typingInterval);
    typedText.textContent = '';
}

// Show the modal and update error message
function showError(errorMessage) {
    document.getElementById("errorMessage").textContent = errorMessage;
    modal.style.display = "flex";
}

// Hide the modal
function hideModal() {
    modal.style.display = "none";
}

// When the user clicks on the "OK" button, close the modal
okButton.onclick = function() {
    hideModal();
    // Optional: You can also redirect the user here, e.g., go back to a specific page
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        hideModal();
    }
}

const startRecording = async () => {
    // Send request to start recording
    const response = await fetch('/start-recording/', { method: 'POST' });
    const data = await response.json();
    if (data.status === 'success') {
        isRecording = true;
        // recordButton.textContent = "Stop Recording";
        submitBtn.disabled = true;
        submitBtn.classList.add('processing');
    } else {
        alert("Error starting recording");
    }
};

const stopRecording = async () => {
    // Send request to stop recording
    recordBtn.disabled = true;
    recordBtn.classList.add('processing');
    
    // Blur the container and show loader
    showRandomGif();
    startTypingAnimation();
    container.classList.add('blurred');
    loader.classList.remove('hidden');

    // REQUEST STOP RECORDING
    const stop_record = await fetch('/stop-recording/', { method: 'POST' });
    const data = await stop_record.json();
    if (data.status === 'success') {

        // TRANSCRIPTION
        const transcription = data.transcription;
        console.log('Transcription:', transcription);  // Show transcription or send it to the UI
        const container = document.getElementById('messageContainer');
        const newDiv = document.createElement('div');
        newDiv.className = 'user-text right-anchor';  // for optional styling
        newDiv.textContent = transcription;
        container.appendChild(newDiv);

        // Re-enable Button and Screen
        
        container.classList.remove('blurred');
        loader.classList.add('hidden');
        stopTypingAnimation();

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

            // Re-enable Buttons
            recordBtn.disabled = false;
            recordBtn.classList.remove('processing');
            submitBtn.disabled = false;
            submitBtn.classList.remove('processing');
        } else {
            showError('Failed to record your message. Try again.');
        }
    } else {
        // Re-enable Button and Screen
        recordBtn.disabled = false;
        recordBtn.classList.remove('processing');
        container.classList.remove('blurred');
        loader.classList.add('hidden');
        stopTypingAnimation();
        showError("Error stopping recording");
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

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".chart-item").forEach(item => {
    const pie = item.querySelector(".pie");
    const percent = parseInt(item.getAttribute("data-percent")) || 0;

    // Initialize the percentage text
    const percentageText = pie.querySelector(".percentage");
    percentageText.textContent = percent;
    console.log(percentageText);

    // Animate the pie chart filling
    let current = 0;
    const interval = setInterval(() => {
      if (current > percent) {
        clearInterval(interval); // Stop the animation when it reaches the target
      } else {
        const deg = (current / 100) * 360;
        pie.style.background = `conic-gradient(#5ce85c 0deg ${deg}deg, #383855 ${deg}deg 360deg)`;
        percentageText.textContent = current; // Update the displayed percentage value
        current++;
      }
    }, 10); // Adjust the speed of the animation
  });
});
