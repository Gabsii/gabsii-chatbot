document.getElementById("input").onkeydown = function(e){
    if(e.keyCode == 13){
        submit(e);
    }
};

document.getElementById("submit-button").onclick = function(e){
    submit(e);
};

document.getElementById("thumbsUp").onclick = function(e){
    goodAnswer(e);
}

function submit(e) {
    var message = document.getElementById("input").value;
    if(message){
        document.getElementById("input").value = '';
        sendQuestion(e, message);
    }
}

function sendQuestion(e, message) {
    var sentQuestion = createSentQuestion(message);
    document.getElementById('container').appendChild(sentQuestion);    
    document.getElementById('container').scrollTop = document.getElementById('container').scrollHeight;
    document.getElementById('user-status').innerText = 'typing...';
    var csrftoken = document.querySelectorAll('footer')[0].firstElementChild.value;

    var request = new XMLHttpRequest();
    request.open('POST', '/bot/chatbot/', true);
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            var resp = request.responseText;
            var sentAnswer = createSentAnswer(resp);
            document.getElementById('container').appendChild(sentAnswer);            
            document.getElementById('container').scrollTop = document.getElementById('container').scrollHeight;
            document.getElementById('user-status').innerText = 'online';
            addThumbsUp();
        } else {
          // We reached our target server, but it returned an error
            document.getElementById('user-status').innerText = '!ERROR!';
            console.log("error" + request.responseText);
        }
      };
      
      request.onerror = function() {
        // There was a connection error of some sort
      };
      
      request.send(JSON.stringify({text: message}));
}

function createSentQuestion(message) {
    var tree = document.createDocumentFragment();
    var bubbles = document.createElement("div");
    bubbles.className = 'bubbles';
    
    var sent = document.createElement("div");
    sent.className = 'sent';

    var bubbleMessage = document.createElement("span");
    bubbleMessage.className = 'bubble-message';
    bubbleMessage.appendChild(document.createTextNode(message));
    sent.appendChild(bubbleMessage);

    var bubbleTime = document.createElement("span");
    bubbleTime.className = 'bubble-time';
    bubbleTime.appendChild(document.createTextNode(("0" + new Date().getHours()).slice(-2) + ":" + ("0" + new Date().getMinutes()).slice(-2)));
    sent.appendChild(bubbleTime);

    bubbles.appendChild(sent);
    tree.appendChild(bubbles);
    
    return tree;
}

function createSentAnswer(message) {
    var tree = document.createDocumentFragment();
    var bubbles = document.createElement("div");
    bubbles.className = 'bubbles';
    
    var received = document.createElement("div");
    received.className = 'received';

    var bubbleMessage = document.createElement("span");
    bubbleMessage.className = 'bubble-message';
    // console.log(message, newMessage);
    bubbleMessage.innerHTML = message.split('\\n').join('<br />');
    received.appendChild(bubbleMessage);

    var bubbleTime = document.createElement("span");
    bubbleTime.className = 'bubble-time';
    bubbleTime.appendChild(document.createTextNode(("0" + new Date().getHours()).slice(-2) + ":" + ("0" + new Date().getMinutes()).slice(-2)));
    received.appendChild(bubbleTime);

    bubbles.appendChild(received);
    tree.appendChild(bubbles);
    
    return tree;
}

function addThumbsUp(){
    document.getElementById('thumbsUp').style.visibility = 'visible';
    var thumbsUpElement = document.getElementById('thumbsUp').cloneNode('true');
    document.getElementById('thumbsUp').remove();
    var lastReceived = document.querySelectorAll('.received');
    lastReceived[lastReceived.length - 1].parentNode.appendChild(thumbsUpElement);
    document.getElementById('thumbsUp').addEventListener('click', function(e){
        goodAnswer(e);
    });
}

function goodAnswer(e) {
    var request = new XMLHttpRequest();
    var lastReceived = document.querySelectorAll('.received');
    var csrftoken = document.querySelectorAll('footer')[0].firstElementChild.value;

    var text = lastReceived[lastReceived.length - 1].firstChild.innerText;     
    var response = lastReceived[lastReceived.length - 1].parentNode.previousElementSibling.firstElementChild.firstElementChild.innerText;
    
    request.open('POST', '/bot/goodAnswer/', true);
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            document.getElementById('thumbsUp').style.visibility = 'hidden';
            console.log(request.responseText);
        } else {
          // We reached our target server, but it returned an error
            document.getElementById('user-status').innerText = '!ERROR!';
            console.log("error" + request.responseText);
        }
      };
      
      request.onerror = function() {
        // There was a connection error of some sort
      };

      request.send(JSON.stringify({message: text, in_response_to: response}));
}