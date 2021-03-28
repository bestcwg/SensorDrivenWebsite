const latestDiv = document.querySelector("#latest");
const minMaxTempDiv = document.querySelector("#min_max_temp");
const minMaxHumDiv = document.querySelector("#min_max_hum");
const minMaxPresDiv = document.querySelector("#min_max_pres");

let client;

startConnect()

// Called after form input is processed
function startConnect() {
    // Generate a random client ID
    const clientID = "clientID-" + parseInt(Math.random() * 1000);

    // Print output for the user in the console
    console.log("Using the following client value: " + clientID);

    // Initialize new Paho client connection
    client = new Paho.MQTT.Client("itwot.cs.au.dk", 8883, clientID);

    // Set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // Connect the client, if successful, call onConnect function
    client.connect({
        onSuccess: onConnect,
        useSSL: true
    });
}

// Called when the client connects
function onConnect() {
    // Fetch the MQTT topic from the form
    const topic = "au676174/#";

    // Print output for the user in the console
    console.log("Subscribing to:" + topic);

    // Subscribe to the requested topic
    client.subscribe(topic);
}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
    console.log("onConnectionLost: Connection Lost");
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost: " + responseObject.errorMessage);
    }
}

// Called when a message arrives
function onMessageArrived(message) {
    const payload = message.payloadString;
    const data = JSON.parse(payload);
    if (message.destinationName.endsWith("/data")) {
        latestDiv.innerHTML = `<span>Date: ${data['date']} Temperatur: ${data['temp']} Humidity: ${data['hum']} Air pressure: ${data['pres']}</span><br/>`;
    }
    if (message.destinationName.endsWith("/min_max")) {
        minMaxTempDiv.innerHTML = `<span><h3>Min:</h3> Date: ${data[0]['date']} temperatur: ${data[0]['MIN(temp)']}</span><br/>` + `<span><h3>Max:</h3> Date: ${data[1]['date']} temperatur: ${data[1]['MAX(temp)']}</span><br/>`;
        minMaxHumDiv.innerHTML = `<span><h3>Min:</h3> Date: ${data[2]['date']} humidity: ${data[2]['MIN(hum)']}</span><br/>` + `<span><h3>Max:</h3> Date: ${data[3]['date']} humidity: ${data[3]['MAX(hum)']}</span><br/>`;
        minMaxPresDiv.innerHTML = `<span><h3>Min:</h3> Date: ${data[4]['date']} air pressure: ${data[4]['MIN(pres)']}</span><br/>` + `<span><h3>Max:</h3> Date: ${data[5]['date']} air pressure: ${data[5]['MAX(pres)']}</span><br/>`;
    }
    console.log("onMessageArrived: " + payload);
}
