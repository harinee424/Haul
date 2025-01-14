// initializing socket connection
var socket = io();

let user_input = document.querySelector("#chat-input");
let send_button = document.querySelector("#send-request");

let chats = document.querySelector(".chats");

send_button.addEventListener("click", function(){
    const user_text = user_input.value.trim();
    if (user_text == "") {
        return;
    }
    socket.emit("user-input", {
        "data": user_text
    });
    addMessage("user-text", user_text);
    user_input.value = "";
})

socket.on("bot-response", function(data){
    addMessage("bot-text", data);
})

function addMessage(className, message) {
    let p = document.createElement("p");
    let span = document.createElement("span");
    p.classList.add(className);
    span.textContent = message;
    p.appendChild(span);
    chats.appendChild(p);
}