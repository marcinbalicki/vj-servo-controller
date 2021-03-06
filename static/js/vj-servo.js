console.log("Start");
var socket = io.connect('http://' + document.domain + ':' + location.port + '/servo');

socket.on('connect', function(msg) {
    console.log('[INFO] Socket connected.');
});

function sendPosition() {
    console.log('sendPosition, value: ' + $('#position').val());
    socket.emit('moveTo', $('#position').val());
}

function sendStop() {
    console.log('sendStop');
    socket.emit('stop');
}

function pullToLeft() {
    socket.emit('pullToLeft');
}

function pullToRight() {
    socket.emit('pullToRight');
}

function sendEnable() {
    socket.emit('enable');
}

function resetCenter() {
    socket.emit('resetCenter');
}
