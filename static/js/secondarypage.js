const dataTable = document.querySelector("#data tbody");

var currentPage = 1;
var numberOfPages = 0;

let client;

fetchData(currentPage);
startConnect();

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
    if (message.destinationName.endsWith("/data")) {
        fetchData(currentPage);
        console.log("onMessageArrived: " + payload);
    }
}

function fetchData(page) {
    // Fetches data through xml request
    const request = new XMLHttpRequest();
    const requestURL = 'https://itwot.cs.au.dk/VM13/opg4a/measurements_by_page/'+page;
    //const requestURL = 'http://192.168.86.75:6500/measurements_by_page/'+page;
    //const requestURL = 'http://192.168.86.75:6500/get_all_measurements';
  
    // When request is loaded
    request.onload = () => {
        if (request.status === 200) {
            // Get data - add to graph and table
            updatePage(request.responseText);
        }
    };
  
    // Setup and send request
    request.open('GET', requestURL);
    request.setRequestHeader('Accept', 'application/json');
    request.send();
}
  
function updatePage(data) {
    // Updates page with the data from the xml request
    list = JSON.parse(data);
    
    dataTable.innerHTML = "";

    if (list.length < 20) {
        numberOfPages = currentPage
    }
    if (list.length == 0 & currentPage == 1) {
        dataTable.innerHTML =
        `<tr>
            <td>No data</td>
            <td>No data</td>
            <td>No data</td>
            <td>No data</td>
        </tr>`; 
    }
    
    for (let r = 0; r < list.length; r++) {
        dataTable.innerHTML +=
        `<tr>
            <td>${list[r].date}</td>
            <td>${list[r].temp}</td>
            <td>${list[r].hum}</td>
            <td>${list[r].pres}</td>
        </tr>`; 
    }
    check();
}

function nextPage() {
    currentPage += 1;
    fetchData(currentPage);
}

function previousPage() {
    currentPage -= 1;
    fetchData(currentPage);
}

function check() {
    // checks for the buttons not to go out of bound
    document.getElementById("next").disabled = currentPage == numberOfPages ? true : false;
    document.getElementById("previous").disabled = currentPage == 1 ? true : false;
    document.getElementById("first").disabled = currentPage == 1 ? true : false;
    document.getElementById("last").disabled = currentPage == numberOfPages ? true : false;
}