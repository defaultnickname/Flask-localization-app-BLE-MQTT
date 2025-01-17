// Create a client instance

function connect() {

    let client = new Paho.Client('localhost', 8000, '/mqtt', 'twojdad');

// set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

// connect the client
    client.connect({
        onSuccess: onConnect,

    });

    function sub(topic){
        client.subscribe(filter=topic);

    }

// called when the client connects
    function onConnect() {
        // Once a connection has been made, make a subscription and send a message.
        console.log("onConnect");
        sub("test/front/1");
        sub("test/front/2");




    }

// called when the client loses its connection
    function onConnectionLost(responseObject) {
        if (responseObject.errorCode !== 0) {
            console.log("onConnectionLost:" + responseObject.errorMessage);
        }


    }

// called when a message arrives
    function onMessageArrived(message) {
        console.log("onMessageArrived:" + message.payloadString);
        let res = message.payloadString.split(" ");
        console.log(res)
        dra.updateTarget(parseInt(res[2])-1, parseInt(res[0]),parseInt(res[1]))
    }

}