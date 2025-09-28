document.addEventListener('DOMContentLoaded', function () {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const voiceButton = document.getElementById('voice-btn');
    const voiceStatus = document.getElementById('voice-status');

    // ---- Speech Recognition Setup ----
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isListening = false;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            sendMessage(transcript);
        };

        recognition.onerror = function (event) {
            console.error('Speech recognition error:', event.error);
            updateVoiceUI(false);
            addMessage('Microphone error: ' + event.error, false);
        };

        recognition.onend = function () {
            if (isListening) {
                try { recognition.start(); } catch (e) { /* ignore if already started */ }
            } else {
                updateVoiceUI(false);
            }
        };
    } else {
        if (voiceButton) voiceButton.style.display = 'none';
        console.warn('SpeechRecognition not supported in this browser.');
    }

    if (voiceButton) {
        voiceButton.addEventListener('click', function () {
            if (!recognition) {
                addMessage('Speech recognition not supported in this browser.', false);
                return;
            }
            isListening = !isListening;
            if (isListening) {
                try {
                    recognition.start();
                    updateVoiceUI(true);
                } catch (err) {
                    console.error('Error starting recognition:', err);
                    isListening = false;
                    updateVoiceUI(false);
                    addMessage('Unable to access microphone. Please allow mic permission.', false);
                }
            } else {
                recognition.stop();
                updateVoiceUI(false);
            }
        });
    }

    function updateVoiceUI(listening) {
        if (!voiceButton || !voiceStatus) return;
        voiceButton.classList.toggle('listening', listening);
        voiceStatus.classList.toggle('active', listening);
    }

    // ---- Chat Helpers ----
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator-container';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
        return typingDiv;
    }

    function removeTypingIndicator(typingIndicator) {
        if (typingIndicator && typingIndicator.parentNode) {
            typingIndicator.remove();
        }
    }

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        if (isUser) {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="message-text"><p>${escapeHtml(message)}</p></div>
                    <div class="message-time">${time}</div>
                </div>
                <div class="message-avatar"><i class="fas fa-user"></i></div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-avatar"><i class="fas fa-robot"></i></div>
                <div class="message-content">
                    <div class="message-text"><p>${escapeHtml(message)}</p></div>
                    <div class="message-time">${time}</div>
                </div>
            `;
        }
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    // ---- Messaging ----
    async function sendMessage(message) {
        const clean = message.trim();
        if (!clean) return;

        addMessage(clean, true);
        userInput.value = '';

        const typing = showTypingIndicator();
        try {
            const response = await fetch('/get_response', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: clean })
            });
            const data = await response.json();
            removeTypingIndicator(typing);
            addMessage(data && data.response ? data.response : "I'm sorry, I didn't catch that. Could you rephrase?", false);
        } catch (err) {
            console.error('Request error:', err);
            removeTypingIndicator(typing);
            addMessage("I'm having trouble reaching the server. Please try again later.", false);
        }
    }

    // ---- Events ----
    if (sendButton) {
        sendButton.addEventListener('click', () => {
            const message = userInput.value.trim();
            if (message) sendMessage(message);
        });
    }

    if (userInput) {
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const message = userInput.value.trim();
                if (message) sendMessage(message);
            }
        });
    }

    // Initial state
    scrollToBottom();
});
