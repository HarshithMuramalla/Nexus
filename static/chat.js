document.addEventListener('DOMContentLoaded', () => {
  const chatHistory = document.getElementById('chatHistory');
  const promptInput = document.getElementById('prompt');
  const sendButton = document.getElementById('sendButton');
  const clearButton = document.getElementById('clearButton');
  const micButton = document.getElementById('micButton');
  const toggleSoundButton = document.getElementById('toggleSound');
  const recordingIndicator = document.getElementById('recordingIndicator');
  const loadingOverlay = document.getElementById('loadingOverlay');

  let isSoundEnabled = true;
  let isRecording = false;
  let isWaitingForResponse = false;

  function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = '<span></span><span></span><span></span>';
    chatHistory.appendChild(typingDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }

  function removeTypingIndicator() {
    const typingDiv = document.getElementById('typingIndicator');
    if (typingDiv) typingDiv.remove();
  }

  function addMessage(role, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role} fade-in`;

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = role === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';

    const content = document.createElement('div');
    content.className = 'content';
    content.textContent = text;

    messageDiv.appendChild(role === 'user' ? content : avatar);
    messageDiv.appendChild(role === 'user' ? avatar : content);

    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    if (role === 'bot' && isSoundEnabled) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-US';
      speechSynthesis.speak(utterance);
    }
  }

  async function sendMessage() {
    const prompt = promptInput.value.trim();
    if (!prompt || isWaitingForResponse) return;

    addMessage('user', prompt);
    promptInput.value = '';
    isWaitingForResponse = true;
    loadingOverlay.classList.remove('d-none');
    showTypingIndicator();

    try {
      const baseURL = window.location.hostname.includes('vercel.app')
        ? 'https://13f3-174-93-238-64.ngrok-free.app'  // Replace with current ngrok if it changes
        : '';

      const response = await fetch(`${baseURL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });

      const data = await response.json();
      removeTypingIndicator();

      if (data.response) {
        addMessage('bot', data.response);
      } else {
        addMessage('bot', 'Unexpected response from server.');
      }
    } catch (err) {
      removeTypingIndicator();
      addMessage('bot', 'Error connecting to server.');
    } finally {
      isWaitingForResponse = false;
      loadingOverlay.classList.add('d-none');
    }
  }

  sendButton.addEventListener('click', sendMessage);
  promptInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
  clearButton.addEventListener('click', () => {
    chatHistory.innerHTML = '';
  });

  micButton.addEventListener('click', () => {
    if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
      alert('Speech recognition is not supported in this browser.');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      isRecording = true;
      micButton.classList.add('btn-mic-recording');
      recordingIndicator.style.display = 'block';
    };

    recognition.onend = () => {
      isRecording = false;
      micButton.classList.remove('btn-mic-recording');
      recordingIndicator.style.display = 'none';
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      promptInput.value = transcript;
      sendMessage();
    };

    recognition.start();
  });

  toggleSoundButton.addEventListener('click', () => {
    isSoundEnabled = !isSoundEnabled;
    toggleSoundButton.innerHTML = `<i class="fa-solid fa-volume-${isSoundEnabled ? 'high' : 'xmark'}"></i>`;
    if (!isSoundEnabled && speechSynthesis.speaking) {
      speechSynthesis.cancel();
    }
  });
});

