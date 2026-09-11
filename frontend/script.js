const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");
const typingIndicator = document.getElementById("typingIndicator");
const newChatButton = document.getElementById("newChatButton");


// ============================================================
// API CONFIGURATION
// ============================================================

const API_BASE_URL =
    "https://coit12204-studymate-ai-1.onrender.com/api";

const API_URL =
    `${API_BASE_URL}/chat`;

const NEW_CHAT_URL =
    `${API_BASE_URL}/chat/new`;


// ============================================================
// ADD MESSAGE TO CHAT
// ============================================================

function addMessage(message, sender) {

    const messageElement =
        document.createElement("div");

    messageElement.classList.add(
        "message",
        sender === "user"
            ? "user-message"
            : "assistant-message"
    );


    // Avatar

    const avatar =
        document.createElement("div");

    avatar.classList.add(
        "message-avatar"
    );

    avatar.textContent =
        sender === "user"
            ? "U"
            : "✦";


    // Content container

    const content =
        document.createElement("div");

    content.classList.add(
        "message-content"
    );


    // Name

    const name =
        document.createElement("div");

    name.classList.add(
        "message-name"
    );

    name.textContent =
        sender === "user"
            ? "You"
            : "StudyMate AI";


    // Message bubble

    const bubble =
        document.createElement("div");

    bubble.classList.add(
        "message-bubble"
    );

    bubble.textContent =
        message;


    // Build message

    content.appendChild(name);
    content.appendChild(bubble);

    messageElement.appendChild(avatar);
    messageElement.appendChild(content);

    chatMessages.appendChild(messageElement);


    // Scroll to newest message

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// ============================================================
// SHOW TYPING INDICATOR
// ============================================================

function showTyping() {

    typingIndicator.classList.remove(
        "hidden"
    );

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// ============================================================
// HIDE TYPING INDICATOR
// ============================================================

function hideTyping() {

    typingIndicator.classList.add(
        "hidden"
    );
}


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendMessage() {

    const message =
        messageInput.value.trim();


    // Don't send empty messages

    if (!message) {
        return;
    }


    // Display user's message

    addMessage(
        message,
        "user"
    );


    // Clear input

    messageInput.value = "";

    messageInput.style.height =
        "auto";


    // Disable send button

    sendButton.disabled =
        true;


    // Show typing indicator

    showTyping();


    try {

        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        const data =
            await response.json();


        // Handle API errors

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to contact the AI service."
            );
        }


        // Display AI response

        addMessage(
            data.response,
            "assistant"
        );


    } catch (error) {

        console.error(
            "Chat error:",
            error
        );


        addMessage(
            "Sorry, something went wrong. Please try again.",
            "assistant"
        );


    } finally {

        hideTyping();

        sendButton.disabled =
            false;

        messageInput.focus();
    }
}


// ============================================================
// SEND BUTTON
// ============================================================

sendButton.addEventListener(
    "click",
    sendMessage
);


// ============================================================
// ENTER KEY
// ============================================================

messageInput.addEventListener(
    "keydown",
    function (event) {

        // Enter sends message
        // Shift + Enter creates a new line

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);


// ============================================================
// AUTO-RESIZE MESSAGE INPUT
// ============================================================

messageInput.addEventListener(
    "input",
    function () {

        this.style.height =
            "auto";

        this.style.height =
            Math.min(
                this.scrollHeight,
                120
            ) + "px";
    }
);


// ============================================================
// START NEW CONVERSATION
// ============================================================

newChatButton.addEventListener(
    "click",
    async function () {

        // Prevent multiple clicks

        newChatButton.disabled =
            true;


        try {

            const response =
                await fetch(
                    NEW_CHAT_URL,
                    {
                        method: "POST"
                    }
                );


            const data =
                await response.json();


            // Check API response

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Unable to start a new conversation."
                );
            }


            // Clear messages displayed
            // in the browser

            chatMessages.innerHTML =
                "";


            // Show welcome message

            addMessage(
                "Hello! 👋 I'm StudyMate AI. What would you like to learn today?",
                "assistant"
            );


            // Clear input

            messageInput.value = "";

            messageInput.style.height =
                "auto";


            // Focus input

            messageInput.focus();


            console.log(
                "New conversation started:",
                data
            );


        } catch (error) {

            console.error(
                "New chat error:",
                error
            );


            addMessage(
                "Unable to start a new conversation. Please try again.",
                "assistant"
            );


        } finally {

            newChatButton.disabled =
                false;
        }
    }
);