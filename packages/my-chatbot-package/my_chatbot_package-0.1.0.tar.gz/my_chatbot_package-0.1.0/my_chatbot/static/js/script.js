document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.querySelector('.chat-input textarea');
    const sendChatBtn = document.querySelector('.chat-input span');
    const chatbox = document.querySelector('.chatbox');
    const inputInitHeight = chatInput.scrollHeight;
    let isTyping = false; 
    let suggestionButtonsShown = false;
    const closeButtonButton = document.getElementById('closeButton');

    closeButtonButton.addEventListener('click', ()=> {
        toggleChatbot();
    })
    
    window.onbeforeunload = function() {
        fetch('/reset_chatbot', {method: 'GET'});
      };

    // Event listener for the Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            toggleChatbot(); // Close the chatbot interface
        }
    });

    // Event listener for changes in the input value
    chatInput.addEventListener('input', handleInput);
    
    // Event listener for sending a chat message
    sendChatBtn.addEventListener('click', handleChat);

    // Chatbot toggler button event listener
    const chatbotToggler = document.querySelector('.chatbot-togglers');
    chatbotToggler.addEventListener('click', toggleChatbot);

    // Function to handle input changes
    function handleInput() {
        
        const inputValue = chatInput.value.trim().toLowerCase();
        isTyping = '';

        if (isTyping == '') {
            toggleKeywordButtons(isTyping);
        }else{
            toggleKeywordButtons(isTyping);
        }

        // Check if the keyword "borrow" is included in the input value
        if (inputValue.includes('borrow') || inputValue.includes('borro')
        ) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['How to borrow book personally?', 
                                      'How to borrow article online?',
                                      'How to borrow thesis physically?',
                                      'How to borrow newspaper virtually?']);
                suggestionButtonsShown = true; // Update the flag
            }

        } else if (inputValue.includes('get')) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['How to get book personally?',
                                      'How to get thesis online?',
                                      'How to get newspaper physically?',
                                      'How to get magazine virtually?'])
                suggestionButtonsShown = true; // Update the flag
            }

        } else if (inputValue.includes('time') || inputValue.includes('closing') || inputValue.includes('open') || inputValue.includes('schedule')) {
            // Only show suggestion buttons if they haven't been shown before
            removekeywordButton();
            if (!suggestionButtonsShown) {
                showSuggestionButton(["What time does the library opens?", 
                                      "What is the available time of the library?", 
                                      "What is the closing time of library?", 
                                      "What is the library schedule?"])
                suggestionButtonsShown = true; // Update the flag
            }
        } else if (inputValue.includes('return') || inputValue.includes('retur')) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['How to return book on the Circulation section?',
                                      'How to return thesis on the Thesis section?',
                                      'How to return item on the third floor?',
                                      'How to return material on Reference section?'])
                                      
                suggestionButtonsShown = true; // Update the flag
            }
        
        } else if (inputValue.includes('reserve')  || inputValue.includes('reserv')) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['How to reserve room in the library?',
                                      'How to do room reservation?',
                                      'How to schedule room in library?',
                                      'How to set room reservation?'])
                suggestionButtonsShown = true; // Update the flag
            }
        
        } else if (inputValue.includes('print') || inputValue.includes('prin')) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['How to avail printing service?',
                                      'How to print inside the library?',
                                      'What floor can students avail printing?',
                                      'How to print in the library for free?'])
                suggestionButtonsShown = true; // Update the flag
            }

        } else if (inputValue.includes('penalty') || inputValue.includes('pena')) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['What if I returned the book late?',
                                      'What if I return the item after the due date?',
                                      'What is the fee for returning an item late?',
                                      'What is the penalty fee for returning an item late?'])
                suggestionButtonsShown = true; // Update the flag
            }
        } else if (inputValue.includes('duration') || inputValue.includes('durat') || inputValue.includes('long') || inputValue.includes('lon')) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['How long can I borrow a reading materials?',
                                      'How many days I can borrow reading materials?',
                                      'What is the maximum duration for borrowing books?'])
                suggestionButtonsShown = true; // Update the flag
            }

        } else if (inputValue.includes('limit') || inputValue.includes('lim') || inputValue.includes('many') || inputValue.includes('man')) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['How many books can I check out?',
                                      'How many books can I borrow at the library?',
                                      "How many books am I permitted to borrow?"])
                suggestionButtonsShown = true; // Update the flag
            }

        } else if (inputValue.includes('late') || inputValue.includes('lat')) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['What if I did not return the book on time?',
                                      'What is the penalty fee for late book returns?',
                                      'What if I returned the book after due date?'])
                suggestionButtonsShown = true; // Update the flag
            }

        } else if (inputValue.includes('submit') || inputValue.includes('pass') || inputValue.includes('submi')) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['How to submit accomplished thesis?',
                                      'How to pass thesis in library?',
                                      'How to do online submission of manuscript?',
                                      'How to submit thesis online at library?'])
                suggestionButtonsShown = true; // Update the flag
            }
        } else if (inputValue.includes('penalty') || inputValue.includes('pena')) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['What if I returned the book late?',
                                      'What if I return the item after the due date?',
                                      'What is the fee for returning an item late?',
                                      'What is the penalty fee for returning an item late?'])
                suggestionButtonsShown = true; // Update the flag
            }
        } else if (inputValue === '') {
            removeSuggestionButtons();
            suggestionButtonsShown = false; // Update the flag
            
        
        } else if (inputValue.includes('requirement') || inputValue.includes('requireme') || inputValue.includes('requir')) {
            removekeywordButton();
            // Only show suggestion buttons if they haven't been shown before
            if (!suggestionButtonsShown) {
                showSuggestionButton(['What are the requirements on the library?',
                                      'What are the requirements for outsiders?',
                                      'What is the requirement for visitors?'])
                suggestionButtonsShown = true; // Update the flag
            }

        } else {
            removeSuggestionButton();
            // Reset the flag if the keyword is not present
            suggestionButtonsShown = false; 
        }
        
    }


    // Function to toggle keyword buttons visibility
    function toggleKeywordButtons(visible) {
        const keywordButtons = document.querySelectorAll('.keyword-button');
        const keywordButton = document.querySelectorAll('.suggestionfix-button');
        keywordButtons.forEach(btn => {
            btn.style.display = visible ? 'none' : 'inline-block';
        
        });
        keywordButton.forEach(btn => {
            btn.style.display = visible ? 'none' : 'inline-block';
        
        });
        
    }

    // Function to show the suggestion button
    function showSuggestionButton(suggestionTexts) {
        removeSuggestionButton();

        suggestionTexts.forEach(text => {
            const suggestionButton = createSuggestionButton(text);
            chatbox.appendChild(suggestionButton);
        });
        
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }

    // Function to create the suggestion button
    function createSuggestionButton(text) {
        const suggestionButton = document.createElement('button');
        suggestionButton.innerText = text;
        suggestionButton.classList.add('suggestion-button');
        suggestionButton.addEventListener('click', handleSuggestionButtonClick)
        return suggestionButton;
    }

    // Function to remove the suggestion button
    function removeSuggestionButton() {
        const suggestionButtons = document.querySelectorAll('.suggestion-button');
        suggestionButtons.forEach(button => button.style.display = 'none');
        suggestionButtonsShown = false;
    }
    // Function to remove all suggestion buttons
    function removeSuggestionButtons() {
        const AllsuggestionButtons = document.querySelectorAll('.suggestion-button');
        AllsuggestionButtons.forEach(button => button.remove());
    }

    // dagdag
    function removeKeywordButtons() {
        const AllKeywordButtons = document.querySelectorAll('.keyword-button');
        const AllKeywordButton = document.querySelectorAll('.suggestionfix-button');
        AllKeywordButtons.forEach(button => button.remove());
        AllKeywordButton.forEach(button => button.remove());
    }
    // dagdag
    function removekeywordButton() {
        const keywordButtons = document.querySelectorAll('.keyword-button');
        const keywordButton = document.querySelectorAll('.suggestionfix-button');
        keywordButtons.forEach(button => button.style.display = 'none');
        keywordButton.forEach(button => button.style.display = 'none');
        keywordButtonsShown = false;
    }

    // Function to handle the suggestion button click
    function handleSuggestionButtonClick(event) {
        const userMessage = event.target.innerText;
        appendMessageToChatbox(userMessage, 'outgoing');

        // Clear the chat input field
        chatInput.value = '';

        // Remove all suggestion buttons
        removeSuggestionButtons();
        removeKeywordButtons();
        
        // Show the "thinking" message
        appendMessageToChatbox('Thinking...', 'thinking' );

        // Send message to server and receive response
        setTimeout(() => {
            sendChatMessage(userMessage);
            
            
        }, 2000); // Simulate a 2 second delay
    }

        // Event listener for when user taps the message box
        chatInput.addEventListener('click', showKeywordButtons, { once: true });
        

    // Function to show the keyword buttons
    function showKeywordButtons() {
        
        const keywords = ['Borrow Book', 'Return Book', 'Reserve Room', 'Requirements for Visit Library', 'Submit Thesis', 'Schedule of the Library', 'Printing Service','Late return of books','Overdue Book Penalty','Book Borrowing Duration','Borrow Limit  '];
        const keywordDescriptions = ['How to borrow book personally?', 'How to return book on the first floor?', 'How to reserve room in the library?', 'What are the requirements to enter the library?', 'How to submit accomplished thesis?', 'What is the library schedule?', 'How to print in the library?','What if I did not return the book on time?','What if I did not return the book on time?','How long a book can be borrowed?','How many book I can borrow?'];

            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
            });
        
    }

    function showborrowButton() {
        
        const keywords = ['How to borrow book personally?','How to get thesis online?','How to get newspaper physically?','How to get magazine virtually?'];
        const keywordDescriptions = ['How to borrow book personally?','How to get thesis online?','How to get newspaper physically?','How to get magazine virtually?'];

            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordsButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
                
            });
        
    }

    

    function showreturnButton() {
        
        const keywords = ['How to return book on the Circulation section?',
        'How to return thesis on the Thesis section?',
        'How to return item on the third floor?',
        'How to return material on Reference section?'];
        const keywordDescriptions = ['How to return book on the Circulation section?',
        'How to return thesis on the Thesis section?',
        'How to return item on the third floor?',
        'How to return material on Reference section?'];

            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordsButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
            });
        
    }
    function showtimeButton() {
        const keywords = ["What time does the library opens?", 
        "What is the available time of the library?", 
        "What is the closing time of library?", 
        "What is the library schedule?"];
        const keywordDescriptions = ["What time does the library opens?", 
        "What is the available time of the library?", 
        "What is the closing time of library?", 
        "What is the library schedule?"];
            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordsButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
            });
    }

    function showreserveButton() {
        const keywords = ['How to reserve room in the library?',
        'How to do room reservation?',
        'How to schedule room in library?',
        'How to set room reservation?'];
        const keywordDescriptions = ['How to reserve room in the library?',
        'How to do room reservation?',
        'How to schedule room in library?',
        'How to set room reservation?'];
            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordsButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
            });
    }

    function showprintButton() {
        const keywords = ['How to avail printing service?',
        'How to print inside the library?',
        'What floor can students avail printing?',
        'How to print in the library for free?'];
        const keywordDescriptions = ['How to avail printing service?',
        'How to print inside the library?',
        'What floor can students avail printing?',
        'How to print in the library for free?'];
            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordsButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
            });
    }
      
    function showpenaltyButton() {
        const keywords = ['What if I returned the book late?',
        'What if I return the item after the due date?',
        'What is the fee for returning an item late?',
        'What is the penalty fee for returning an item late?'];
        const keywordDescriptions = ['What if I returned the book late?',
        'What if I return the item after the due date?',
        'What is the fee for returning an item late?',
        'What is the penalty fee for returning an item late?'];
            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordsButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
            });
    }  
     
    function showdurationButton() {
        const keywords = ['How long can a book be borrowed for?',
        'How long can I borrow a reading materials?',
        'How many days I can borrow reading materaials?',
        'How long can I borrow reading materials?'];
        const keywordDescriptions = ['How long can a book be borrowed for?',
        'How long can I borrow a reading materials?',
        'How many days I can borrow reading materaials?',
        'What is the maximum duration for borrowing books?'];

            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordsButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
            });
    }
      
    function showlimitButton() {
        const keywords = ['How many books can I check out?',
        'How many books can I borrow at the library?','How many books am I permitted to borrow?'];
        const keywordDescriptions = ['How many books can I check out?',
        'How many books can I borrow at the library?','How many books am I permitted to borrow?'];
            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordsButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
            });
    }
     
    function showlateButton() {
        const keywords = ['What if I did not return the book on time?',
        'What is the penalty fee for late book returns?',
        'What if I returned the book after due date?'];
        const keywordDescriptions = ['What if I did not return the book on time?',
        'What is the penalty fee for late book returns?',
        'What if I returned the book after due date?'];
            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordsButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
            });
    }

    function showsubmitButton() {
        const keywords = ['How to submit accomplished thesis?',
        'How to pass thesis in library?',
        'How to do online submission of manuscript?',
        'How to submit thesis online at library?'];
        const keywordDescriptions = ['How to submit accomplished thesis?',
        'How to pass thesis in library?',
        'How to do online submission of manuscript?',
        'How to submit thesis online at library?'];
            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordsButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
            });
    }

    function showrequirementButton() {
        const keywords = ['What are the requirements on the library?',
        'What are the requirements for outsiders?',
        'What is the requirement for visitors?'];
        const keywordDescriptions = ['What are the requirements on the library?',
        'What are the requirements for outsiders?',
        'What is the requirement for visitors?'];
            keywords.forEach((keyword, index) => {
                const keywordButton = createKeywordsButton(keyword, keywordDescriptions[index]);
                chatbox.appendChild(keywordButton);
            });
    }

    // Function to create a keyword button
    function createKeywordButton(text, description) {
        const keywordButton = document.createElement('button');
        keywordButton.innerText = text;
        keywordButton.classList.add('keyword-button');
        keywordButton.addEventListener('click', () => handleKeywordButton(description));
        return keywordButton;
    }

    // Function to create a keyword button
    function createKeywordsButton(text, description) {
        const keywordButton = document.createElement('button');
        keywordButton.innerText = text;
        keywordButton.classList.add('suggestionfix-button');
        keywordButton.addEventListener('click', () => handleKeywordButton(description));
        return keywordButton;
    }

    // Function to handle the keyword button click
    function handleKeywordButton(keyword) {
        chatInput.value += ` ${keyword} `;
        const keywordButtons = document.querySelectorAll('.keyword-button');
        keywordButtons.forEach(btn => btn.remove());
        // Simulate a click event on the send chat button
        sendChatBtn.click();
    }
    // Event listener for sending a chat message
    sendChatBtn.addEventListener('click', handleChat);

    function handleChat() {
        const userMessage = chatInput.value.trim();
        if (!userMessage) return;

        // Clear all suggestion and keyword buttons
        removeSuggestionButtons();
        removeKeywordButtons()


        // Clear the input textarea and set its height to default
        chatInput.value = '';
        chatInput.style.height = `${inputInitHeight}px`;
    
        // Append outgoing message to chatbox
        appendMessageToChatbox(userMessage, 'outgoing');

        // Show the "thinking" message
        appendMessageToChatbox('Thinking...', 'thinking' );
        
        // Send message to server and receive response after the delay
        setTimeout(() => {
            sendChatMessage(userMessage);
            
        }, 2000); // Delay of 2 seconds
        
        // Event listener for when user taps the message box
        sendChatBtn.addEventListener('input', showKeywordButtons, { once: true });
    }
    
    // Function to send chat message to server
    function sendChatMessage(message) {
        fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {

                // Remove the "Thinking..." message
                const thinkingMessage = document.querySelector('.chatbox li.thinking');

                if (thinkingMessage) {
                    thinkingMessage.remove();
                }

                // Check if response is not null and not an empty string
                if (data.response && data.response.trim() !== '') {
                    appendMessageToChatbox(data.response, 'incoming');
                }
                
                const suggestionMessageId = 'suggestionMessage';
                // Function to show suggestion and add click event listener
                const showSuggestion = (showFunction) => {
                    appendMessageToChatbox("Did you mean this?.⬇️", 'incoming', suggestionMessageId);
                    showFunction();
                    addSuggestionClickListeners();
                }

                if (data.response.includes('sorry') && message.toLowerCase().includes('borrow')) {
                    appendMessageToChatbox(" Did you mean this?.⬇️", 'incoming');
                    showborrowButton();

                } else if (data.response.includes('sorry') && message.toLowerCase().includes('reserve')) {
                    appendMessageToChatbox(" Did you mean this?.⬇️", 'incoming');
                    showreserveButton();
                } else if (data.response.includes('sorry') && (message.toLowerCase().includes('schedule') || message.toLowerCase().includes('date') || message.toLowerCase().includes('time'))) {
                    appendMessageToChatbox(" Did you mean this?.⬇️", 'incoming');
                    showtimeButton();
                } else if (data.response.includes('sorry') && message.toLowerCase().includes('return')) {
                    appendMessageToChatbox(" Did you mean this?.⬇️", 'incoming');
                    showreturnButton();
                } else if (data.response.includes('sorry') && message.toLowerCase().includes('print')) {
                    appendMessageToChatbox(" Did you mean this?.⬇️", 'incoming');
                    showprintButton();
                } else if (data.response.includes('sorry') && (message.toLowerCase().includes('submit') || message.toLowerCase().includes('pass'))) {
                    appendMessageToChatbox(" Did you mean this?.⬇️", 'incoming');
                    showsubmitButton();
                } else if (data.response.includes('sorry') && message.toLowerCase().includes('requirements')) {
                    appendMessageToChatbox(" Did you mean this?.⬇️", 'incoming');
                    showrequirementButton();
                } else if (data.response.includes('sorry') && message.toLowerCase().includes('penalty')) {
                    appendMessageToChatbox(" Did you mean this?.⬇️", 'incoming');
                    showpenaltyButton();
                } else if (data.response.includes('sorry') && message.toLowerCase().includes('duration')) {
                    appendMessageToChatbox(" Did you mean this?.⬇️", 'incoming');
                    showdurationButton();
                } else if (data.response.includes('sorry') && message.toLowerCase().includes('limit')) {
                    appendMessageToChatbox(" Did you mean this?.⬇️", 'incoming');
                    showlimitButton();
                } else if (data.response.includes('sorry') && message.toLowerCase().includes('late')) {
                    appendMessageToChatbox(" Did you mean this?.⬇️", 'incoming');
                    showlateButton();
                } else if (data.response.includes('bye') && ( message.toLowerCase().includes ('end session') || message.toLowerCase().includes('end conversation') || message.toLowerCase().includes('conversation end') 
                    || message.toLowerCase().includes('end') || message.toLowerCase().includes('thank you') || message.toLowerCase().includes('thanks') || message.toLowerCase().includes('goodbye') || message.toLowerCase().includes('good bye')
                    || message.toLowerCase().includes('end convo') || message.toLowerCase().includes('bye'))) {
                    chatInput.disabled = true;
                    sendChatBtn.disabled = true;
                    showFeedbackModal();
                }else{
                    appendMessageToChatbox(data.follow_up_question, 'incoming'); 
                    showKeywordButtons();
                }
                        
                // Handle predefined text
                if (data.predefined_text) {
                    // Do something with the predefined text, such as displaying it in the chatbox
                    appendMessageToChatbox(data.predefined_text, 'incoming');
                     
                }
            })
    
            .catch(error => {
                console.error('Error:', error);
                // Handle error gracefully
                appendMessageToChatbox('Error occurred. Please try again.', 'error');
            });
    }

    // Function to add click event listeners to suggestion buttons
    function addSuggestionClickListeners() {
        const suggestionButtons = document.querySelectorAll('.suggestionfix-button');
        suggestionButtons.forEach(button => {
            button.addEventListener('click', () => {
                const suggestionMessage = document.getElementById('suggestionMessage');
                if (suggestionMessage) {
                    suggestionMessage.remove();
                }
            });
        });
    }

    // Function to create chat message element
    function createChatLi(message, className) {
        const chatLi = document.createElement('li');
        chatLi.classList.add('chat', className);
        
        // Add profile image
        const profileImg = document.createElement('img');
        profileImg.src = 'static/chatbot.png'; // 'static/chatbot.png' is the profile image path
        chatLi.appendChild(profileImg);

        // Add message content and timestamp
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message-container');

        const messageText = document.createElement('p');
        messageText.classList.add('message');
        messageText.textContent = message;

        const timestamp = document.createElement('span');
        timestamp.classList.add('timestamp');
        timestamp.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageContainer.appendChild(messageText);
        messageContainer.appendChild(timestamp);

        chatLi.appendChild(messageContainer);

        return chatLi;
    }

    // Function to append message to chatbox // NEW ADDED SCRIPT FOR AUTOMATIC SCROLL DOWN TO NEW MESSAGE
    function appendMessageToChatbox(message, className) {
        const chatLi = createChatLi(message, className);
        chatbox.appendChild(chatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
    }
    

    // Adjust input textarea height dynamically
    chatInput.addEventListener('input', () => {
        chatInput.style.height = `${inputInitHeight}px`;
        chatInput.style.height = `${chatInput.scrollHeight}px`;
    });

    // Submit chat message on Enter press (with Shift key)
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && window.innerWidth > 800) {
            e.preventDefault();
            handleChat();
        }
    });


    // Function to toggle chatbot display
    function toggleChatbot() {
        const body = document.querySelector('body');
        body.classList.toggle('show-chatbot');
    }
});

document.addEventListener("DOMContentLoaded", function () {
    // Event listener for the feedback submit button
    const feedbackForm = document.getElementById("feedbackForm");
    if (feedbackForm) {
        feedbackForm.addEventListener("submit", function (event) {
            // Prevent the default form submission
            event.preventDefault();

            // Call the submitFeedback function
            submitFeedback();
        });
    }

    setRating(defaultRatingIndex);
});

function showFeedbackModal() {
    const modal = document.getElementById('feedbackModal');
    console.log('Feedback modal displayed');
    modal.style.display = 'block';
}

function hideFeedbackModal() {
    const modal = document.getElementById('feedbackModal');
    modal.style.display = 'none';
    console.log('Feedback modal hidden');

    // Clear previous messages when closing the modal
    document.getElementById('feedbackMessages').innerHTML = '';
}

let hasSubmittedFeedback = false;
let currentRatingIndex = null;

function submitFeedback() {
    const rating = currentRatingIndex; // Get the current rating index
    const feedbackMessages = document.getElementById('feedbackMessages');
    const submitBtn = document.getElementById('feedbackSubmitBtn');
    const chatInput = document.querySelector('.chat-input textarea');
    const sendChatBtn = document.querySelector('.chat-input span');

    // Check if a rating is selected
    if (rating !== null && rating !== undefined) {
        const emoji = rating;
        const criteria = getCriteriaForEmoji(emoji);

        // Disable the submit button to prevent multiple submissions
        submitBtn.disabled = true;

        // (error checking) Check if the user has already submitted feedback
        if (hasSubmittedFeedback) {
            // Show a message if the user has already submitted feedback
            feedbackMessages.innerHTML = '<p class="error-message">You have already submitted feedback. You can only submit once.</p>';
            submitBtn.disabled = false;
            console.log('Feedback already submitted');
            return;
        }

        // Send an AJAX request to submit the feedback along with criteria
        fetch('/submit_feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Adjusted content type to JSON
            },
            body: JSON.stringify({ emoji: emoji, rating: criteria }), // Adjusted key names
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                feedbackMessages.innerHTML = '<p class="success-message">Rating submitted successfully!</p>';

                // Update the flag to indicate that the user has submitted feedback
                hasSubmittedFeedback = true;

                submitBtn.style.display = 'none';
            } else {
                feedbackMessages.innerHTML = '<p class="error-message">Failed to submit feedback. Please try again.</p>';
            }
        })
        .catch(error => {
            console.error('Error submitting feedback:', error);
            feedbackMessages.innerHTML = '<p class="error-message">Error submitting feedback. Please try again.</p>';
        })
        .finally(() => {
            submitBtn.disabled = false;
            if (chatInput) chatInput.disabled = true;
            if (sendChatBtn) sendChatBtn.disabled = true;
        });

    } else {
        // Show a message if no rating is selected
        feedbackMessages.innerHTML = '<p class="error-message">Please select a rating.</p>';
        console.log('No rating selected');
    }
}

// Function to handle emoji selection
function selectEmoji(emojiNumber) {
    // Clear existing selected emojis
    document.querySelectorAll('.star').forEach(label => {
        label.classList.remove('selected');
    });

    document.querySelectorAll('.emoji-label').forEach(label => {
        label.classList.remove('selected');
    });

    const selectedEmoji = document.querySelector(`.star[data-rate="${emojiNumber}"]`);
    // Add selected class to the clicked emoji
    if (selectedEmoji) {
        selectedEmoji.classList.add('selected');
        currentRatingIndex = emojiNumber;
    }

    const ratingInput = document.querySelector('input[name="rating"]');
    if (ratingInput) {
        ratingInput.value = emojiNumber;
    }

    // Show feedback modal if not already visible
    showFeedbackModal();

    // Show the submit button
    document.getElementById('feedbackSubmitBtn').classList.remove('hidden');
    submitFeedback(); // Automatically submit feedback when a rating is selected
}

// Console Log Function to get criteria based on emoji rating
function getCriteriaForEmoji(emoji) {
    switch (emoji) {
        case 1:
            return 'Poor';
        case 2:
            return 'Fair';
        case 3:
            return 'Good';
        case 4:
            return 'Very Good';
        case 5:
            return 'Excellent';
        default:
            return 'Unknown';
    }
}

let button = document.querySelector('.button');
let buttonText = document.querySelector('.tick');

const tickMark = "<svg width=\"18\" height=\"15\" viewBox=\"0 0 58 45\" xmlns=\"http://www.w3.org/2000/svg\"><path fill=\"#fff\" fill-rule=\"nonzero\" d=\"M19.11 44.64L.27 25.81l5.66-5.66 13.18 13.18L52.07.38l5.65 5.65\"/></svg>";

buttonText.innerHTML = "Submit";

button.addEventListener('click', function () {
    if (buttonText.innerHTML !== "Submit") {
        buttonText.innerHTML = "Submit";
    } else if (buttonText.innerHTML === "Submit") {
        buttonText.innerHTML = tickMark;
        // Hide the button after clicking
        button.classList.add('hidden');
    }
    this.classList.toggle('button__circle');

    setTimeout(function () {
        document.getElementById('feedbackModal').style.display = 'none';
        // After a delay, show the feedback modal again to start a new conversation
    }, 3000); // Timeout of 3 seconds
});

const stars = document.querySelectorAll(".star");
const emojiEl = document.querySelector(".emoji");
const statusEl = document.querySelector(".status");
const defaultRatingIndex = 0;
currentRatingIndex = 0;

const ratings = [
    { emoji: "", name: "Give us rating" },
    { emoji: "😔", name: "Poor" },
    { emoji: "🙁", name: "Fair" },
    { emoji: "🙂", name: "Good" },
    { emoji: "🤩", name: "Very Good" },
    { emoji: "🥰", name: "Excellent" }
];

const setRating = (index) => {
    stars.forEach((star) => star.classList.remove("selected"));
    if (index > 0 && index <= stars.length) {
        document
            .querySelector('[data-rate="' + index + '"]')
            .classList.add("selected");
    }
    emojiEl.innerHTML = ratings[index].emoji;
    statusEl.innerHTML = ratings[index].name;
};

const resetRating = () => {
    currentRatingIndex = defaultRatingIndex;
    setRating(defaultRatingIndex);
};

stars.forEach((star) => {
    star.addEventListener("click", function () {
        const criteria = parseInt(star.getAttribute("data-rate"));
        if (criteria === currentRatingIndex) {
            resetRating();
        } else {
            currentRatingIndex = criteria;
            setRating(criteria);
            submitFeedback(); // Automatically submit feedback when a rating is selected
        }
        console.log('Rating Submitted:', ratings[criteria].name);
        console.log('Star clicked with rating index:', criteria);
    });

    star.addEventListener("mouseover", function () {
        const index = parseInt(star.getAttribute("data-rate"));
        setRating(index);
    });

    star.addEventListener("mouseout", function () {
        setRating(currentRatingIndex);
    });
});
