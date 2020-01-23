let ws = new WebSocket("ws://127.0.0.1:5678/");

ws.onmessage = function (event) {
    alert(event.data);
};

function callServerListener(id, event_type) {
    ws.send(id+":"+event_type);
}