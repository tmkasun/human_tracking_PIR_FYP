var webSocketURL = "ws://" + ApplicationOptions.constance.WEB_SOCKET_SERVER + ":" + ApplicationOptions.constance.WEB_SOCKET_PORT
var websocket;

// Make the function wait until the connection is made...
var waitTime = 1000;
function waitForSocketConnection(socket, callback) {
    setTimeout(
        function () {
            if (socket.readyState === 1) {
                initializeWebSocket();
                waitTime = 1000;
                console.log("Connection is made");
                if (callback != null) {
                    callback();
                }
                return;

            } else {
                websocket = new WebSocket(webSocketURL);
                waitTime += 400;
                $.UIkit.notify({
                    message: "wait for connection " + waitTime / 1000 + " Seconds...",
                    status: 'warning',
                    timeout: waitTime,
                    pos: 'top-center'
                });
                waitForSocketConnection(websocket, callback);
            }

        }, waitTime); // wait 5 milisecond for the connection...
}

var webSocketOnOpen = function () {
    $.UIkit.notify({
        message: 'You Are Connectedto Map Server!!',
        status: 'success',
        timeout: ApplicationOptions.constance.NOTIFY_SUCCESS_TIMEOUT,
        pos: 'top-center'
    });
};

var webSocketOnError = function (e) {
    $.UIkit.notify({
        message: 'Something went wrong when trying to connect to <b>' + webSocketURL + '<b/>',
        status: 'danger',
        timeout: ApplicationOptions.constance.NOTIFY_DANGER_TIMEOUT,
        pos: 'top-center'
    });
//    waitForSocketConnection(websocket);
};

var webSocketOnClose = function (e) {
    $.UIkit.notify({
        message: 'Connection lost with server!!',
        status: 'danger',
        timeout: ApplicationOptions.constance.NOTIFY_DANGER_TIMEOUT,
        pos: 'top-center'
    });
    waitForSocketConnection(websocket);
};

var previous_heat_points = [];
var density = 0;
function clear_last() {
    for (var point in previous_heat_points) {
        map.removeLayer(previous_heat_points[point]);
    }
}
var webSocketOnMessage = function (event) {
    var coordinates_array = JSON.parse(event.data);
    density = 0;
    clear_last();
    for (var coordinates_index in coordinates_array) {
        density+=1;
        var coordinates = coordinates_array[coordinates_index];
        var heat_layer_options = {
            radius: 50,
            maxZoom: 23,
            blur: 40
            //gradient: {0.4: 'blue', 0.65: 'lime', 1: 'red'}
        };
        var heat = L.heatLayer([
            [coordinates.lat, coordinates.lng, 1] // lat, lng, intensity
        ], heat_layer_options).addTo(map);
        previous_heat_points.push(heat);

    }

    density_message.content(lhs+density+rhs);


};

var lhs = "<span style='text-align: center;margin:auto; display:table;'>Population Density: <b style='color:red'>";
var rhs = "</b></span>";

var density_message = $.UIkit.notify({
    message: lhs + density + rhs,
    status: 'success',
    timeout: 0,
    pos: 'top-center'
});

function initializeWebSocket() {
    websocket = new WebSocket(webSocketURL);
    websocket.onmessage = webSocketOnMessage;
    websocket.onclose = webSocketOnClose;
    websocket.onerror = webSocketOnError;
    websocket.onopen = webSocketOnOpen;
}


initializeWebSocket();

function LocalStorageArray(id) {
    if (typeof (sessionStorage) === 'undefined') {
        // Sorry! No Web Storage support..
        return ['speed']; // TODO: fetch this array from backend DB rather than keeping as in-memory array
    }
    if (id === undefined) {
        throw 'Should provide an id to create a local storage!';
    }
    var DELIMITER = ','; // Private variable delimiter
    this.storageId = id;
    sessionStorage.setItem(id, 'speed'); // TODO: <note> even tho we use `sessionStorage` because of this line previous it get overwritten in each page refresh
    this.getArray = function () {
        return sessionStorage.getItem(this.storageId).split(DELIMITER);
    };

    this.length = this.getArray().length;

    this.push = function (value) {
        var currentStorageValue = sessionStorage.getItem(this.storageId);
        var updatedStorageValue;
        if (currentStorageValue === null) {
            updatedStorageValue = value;
        } else {
            updatedStorageValue = currentStorageValue + DELIMITER + value;
        }
        sessionStorage.setItem(this.storageId, updatedStorageValue);
        this.length += 1;
    };
    this.isEmpty = function () {
        return (this.getArray().length === 0);
    };
    this.splice = function (index, howmany) {
        var currentArray = this.getArray();
        currentArray.splice(index, howmany);
        var updatedStorageValue = currentArray.toString();
        sessionStorage.setItem(this.storageId, updatedStorageValue);
        this.length -= howmany;
        // TODO: should return spliced section as array
    };
}