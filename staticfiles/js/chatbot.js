// Function to send a message to the server and update the chat history



function sendMessage() {
    var query = $('#query-input').val();
    var chatHistory = $('#chat-history').html();
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();
    $('#spinner2').show();
    $.ajax({
        type: 'POST',
        url: '/chatbot/',
        data: {
            'query': query,
            'chat_history[]': chatHistory.split('<br>').filter(Boolean)
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken); // Set CSRF token in request headers
        },
        success: function (data) {
            $('#spinner2').hide();
        /*   $('#chat-history').append('<strong>You  :</strong> ' + query + '<br>');
            $('#chat-history').append('<strong>Chatbot :</strong> ' + data.response + '<br>');
            $('#query-input').val(''); */


            $('#chat-history').append('<div style=" display: block; width:50%; clear:both; float:left; margin-top: 10px; background-color: rgb(125, 14, 128); font-size: 0.95rem; color: #fff; border-radius: 10px 10px 10px 0; white-space: pre-wrap; padding: 12px 16px;"><strong>You  :</strong> ' + query + '</div>');
        $('#chat-history').append('<div style="clear:both; float:right; margin-top: 10px;  background-color: #575357;; font-size: 0.95rem; color: #fff; border-radius: 10px 10px 0 10px; white-space: pre-wrap; padding: 12px 16px; max-width: 75%;"><strong>Chatbot :</strong> ' + data.response + '</div>');
        $('#query-input').val('');
        }
    });
}



// Function to clear the chat history
function clearChat() {
    $('#chat-history').html('');
    $('#query-input').val('');
}

// Event listener for the submit button
$('#submit-btn').click(function () {
    sendMessage();
});

// Event listener for the clear button
$('#clear-btn').click(function () {
    clearChat();
});