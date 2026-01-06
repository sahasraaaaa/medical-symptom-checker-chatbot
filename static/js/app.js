// Medical Symptom Checker Chatbot - Frontend JavaScript

class ChatbotUI {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.symptomsList = document.getElementById('symptomsList');
        this.resetBtn = document.getElementById('resetBtn');
        this.disclaimerModal = document.getElementById('disclaimerModal');
        this.acceptDisclaimerBtn = document.getElementById('acceptDisclaimer');

        this.init();
    }

    init() {
        // Load disclaimer
        this.loadDisclaimer();

        // Event listeners
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        this.resetBtn.addEventListener('click', () => this.resetConversation());
        this.acceptDisclaimerBtn.addEventListener('click', () => this.acceptDisclaimer());

        // Add welcome message
        this.addBotMessage("Hello! I'm a medical symptom checker chatbot.\n\nI can help identify possible conditions based on your symptoms, but please remember that I cannot replace a real doctor's diagnosis.\n\nCould you please describe the symptoms you're experiencing?\nFor example: \"I have a headache and fever\" or \"I'm experiencing chest pain\"");
    }

    async loadDisclaimer() {
        try {
            const response = await fetch('/api/disclaimer');
            const data = await response.json();
            document.getElementById('disclaimerText').textContent = data.disclaimer;
        } catch (error) {
            console.error('Error loading disclaimer:', error);
        }
    }

    acceptDisclaimer() {
        this.disclaimerModal.classList.add('hidden');
        this.messageInput.focus();
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();

        if (!message) {
            return;
        }

        // Add user message to chat
        this.addUserMessage(message);

        // Clear input
        this.messageInput.value = '';

        // Disable send button
        this.sendBtn.disabled = true;
        this.sendBtn.textContent = 'Thinking...';

        try {
            // Send message to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            const data = await response.json();

            if (data.error) {
                this.addBotMessage('Sorry, an error occurred: ' + data.error);
            } else {
                // Add bot response
                this.addBotMessage(data.response);

                // Update symptoms list
                this.updateSymptomsList(data.symptoms);
            }
        } catch (error) {
            console.error('Error:', error);
            this.addBotMessage('Sorry, I encountered an error. Please try again.');
        } finally {
            // Re-enable send button
            this.sendBtn.disabled = false;
            this.sendBtn.textContent = 'Send';
            this.messageInput.focus();
        }
    }

    addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';

        const label = document.createElement('div');
        label.className = 'message-label';
        label.textContent = 'You';

        const content = document.createElement('div');
        content.className = 'message-content';
        content.textContent = message;

        messageDiv.appendChild(label);
        messageDiv.appendChild(content);
        this.chatMessages.appendChild(messageDiv);

        this.scrollToBottom();
    }

    addBotMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';

        const label = document.createElement('div');
        label.className = 'message-label';
        label.textContent = 'Medical Assistant';

        const content = document.createElement('div');
        content.className = 'message-content';
        content.textContent = message;

        messageDiv.appendChild(label);
        messageDiv.appendChild(content);
        this.chatMessages.appendChild(messageDiv);

        this.scrollToBottom();
    }

    updateSymptomsList(symptoms) {
        if (!symptoms || symptoms.length === 0) {
            this.symptomsList.innerHTML = '<p class="no-symptoms">No symptoms detected yet</p>';
            return;
        }

        this.symptomsList.innerHTML = '';
        symptoms.forEach(symptom => {
            const symptomDiv = document.createElement('div');
            symptomDiv.className = 'symptom-item';
            symptomDiv.textContent = symptom.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            this.symptomsList.appendChild(symptomDiv);
        });
    }

    async resetConversation() {
        if (!confirm('Are you sure you want to reset the conversation?')) {
            return;
        }

        try {
            const response = await fetch('/api/reset', {
                method: 'POST',
            });

            if (response.ok) {
                // Clear chat messages
                this.chatMessages.innerHTML = '';

                // Clear symptoms list
                this.updateSymptomsList([]);

                // Add welcome message
                this.addBotMessage("Conversation reset. Let's start fresh!\n\nPlease describe the symptoms you're experiencing.");
            }
        } catch (error) {
            console.error('Error resetting conversation:', error);
            alert('Failed to reset conversation. Please try again.');
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// Initialize chatbot UI when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatbotUI();
});
