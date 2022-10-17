//Using the HiveMQ public Broker, with a random client Id
var client = new Paho.MQTT.Client("broker.emqx.io", 8084, "myclientid_" + parseInt(Math.random() * 100, 10));

//Time Variable
var today = new Date();
var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
var userNCAPID = "NCAP001"
var myChart
var activeNCAPS = [];
var activeXDCR = [];

var tempDiff = 0;
var tempDiffString = '';
var currentTemp = 0;
var userSetPoint = 0;

$(function() {
var xValues = [];
var yValues = [];
var ctx = document.getElementById('myChart').getContext('2d');
myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: xValues,
      datasets: [{
        fill: false,
lineTension: 0,
backgroundColor: "rgba(0,0,255,1.0)",
borderColor: "rgba(0,0,255,0.1)",
data: yValues
}]
},
options: {
legend: {display: false},
scales: {
yAxes: [{ticks: {min: 6, max:16}}],
}
}
});
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    /* Toggle between adding and removing the "active" class,
    to highlight the button that controls the panel */
    this.classList.toggle("active");

    /* Toggle between hiding and showing the active panel */
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}
});



//Gets  called if the websocket/mqtt connection gets disconnected for any reason
client.onConnectionLost = function(responseObject) {
  //Depending on your scenario you could implement a reconnect logic here
  alert("connection lost: " + responseObject.errorMessage);
};

//Gets called whenever you receive a message for your subscriptions
client.onMessageArrived = function(message) {
  //Do something with the push message you received
  if (message.destinationName == 'RUSMARTLAB/Heartbeat'){
    today = new Date();
    time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    $('#heartbeatMessages').html('<span>Topic: ' + message.destinationName + '  | ' + message.payloadString + '   |   ' + time + '</span><br/>');
    var splitPayload = message.payloadString.split(",");
    addRowHeartbeatTable(splitPayload[0], time)
  }
  else {
    $('#receivedMessages').prepend('<span>Topic: ' + message.destinationName + '  | ' + message.payloadString + '</span><br/>');
    var splitPayload = message.payloadString.split(",");
    $('#messages_details').html('');
    $('#messages_details').append('<span>Network Service Type: ' + splitPayload[0] + '</span><br/>')
    if (splitPayload[0] == '1'){
      $('#messages_details').append('<span>Network Service ID: ' + splitPayload[1] + '</span><br/>')
      $('#messages_details').append('<span>Message Type: ' + splitPayload[2] + '</span><br/>')
      if (splitPayload[1] == '3'){
        $('#messages_details').append('<span>Message Length(Bytes): ' + splitPayload[3] + '</span><br/>')
        $('#messages_details').append('<span>Error Code: ' + splitPayload[4] + '</span><br/>')
        $('#messages_details').append('<span>NCAP ID: ' + splitPayload[5] + '</span><br/>')
        $('#messages_details').append('<span>NCAP Name: ' + splitPayload[6] + '</span><br/>')
        $('#messages_details').append('<span>Address Type: ' + splitPayload[7] + '</span><br/>')
        $('#messages_details').append('<span>IP Address: ' + splitPayload[8] + '</span><br/>')
        $('#entity1_NCAP').html('')
        $('#entity1_NCAP').append('<h3>NCAP Name: ' + splitPayload[6] + '</h3>')
        $('#entity1_NCAP').append('<b>NCAP ID:</b> ' + splitPayload[5] + '<br/>')
        $('#entity1_NCAP').append('<b>NCAP IP Address:</b> ' + splitPayload[8])

      }
      else if (splitPayload[1] == '5'){
        $('#messages_details').append('<span>Message Length(Bytes): ' + splitPayload[3] + '</span><br/>')
        $('#messages_details').append('<span>Error Code: ' + splitPayload[4] + '</span><br/>')
        $('#messages_details').append('<span>NCAP ID: ' + splitPayload[5] + '</span><br/>')
        $('#messages_details').append('<span>Number of TIMS: ' + splitPayload[6] + '</span><br/>')
        $('#messages_details').append('<span>TIM ID Array: ' + splitPayload[7] + '</span><br/>')
        $('#messages_details').append('<span>TIM Name Array: ' + splitPayload[8] + '</span><br/>')
        $('#entity1_TIM').html('')
        $('#entity1_TIM').append('<h3>TIM Names: ' + splitPayload[8]+ '</h3>')
        $('#entity1_TIM').append('<b>TIM IDs:</b> ' + splitPayload[7] + '<br/>')

      }
      else if (splitPayload[1] == '6'){
        $('#messages_details').append('<span>Message Length(Bytes): ' + splitPayload[3] + '</span><br/>')
        $('#messages_details').append('<span>Error Code: ' + splitPayload[4] + '</span><br/>')
        $('#messages_details').append('<span>NCAP ID: ' + splitPayload[5] + '</span><br/>')
        $('#messages_details').append('<span>TIM ID: ' + splitPayload[6] + '</span><br/>')
        $('#messages_details').append('<span>Number of Channels: ' + splitPayload[7] + '</span><br/>')
        $('#messages_details').append('<span>XDCR Channel ID Array: ' + splitPayload[8] + '</span><br/>')
        $('#messages_details').append('<span>XDCR Channel Name Array: ' + splitPayload[9] + '</span><br/>')
        $('#entity1_XDCR').html('')
        $('#entity1_XDCR').append('<h3>Transducer Names: ' + splitPayload[9]+ '</h3>')
        $('#entity1_XDCR').append('<b>Channel IDs:</b> ' + splitPayload[8] + '<br/>')
      }
    }
    else if (splitPayload[0] == '2'){
      $('#messages_details').append('<span>Network Service ID: ' + splitPayload[1] + '</span><br/>')
      $('#messages_details').append('<span>Message Type: ' + splitPayload[2] + '</span><br/>')
      if (splitPayload[1] == '1'){
        $('#messages_details').append('<span>Message Length(Bytes): ' + splitPayload[3] + '</span><br/>')
        $('#messages_details').append('<span>Error Code: ' + splitPayload[4] + '</span><br/>')
        $('#messages_details').append('<span>NCAP ID: ' + splitPayload[5] + '</span><br/>')
        $('#messages_details').append('<span>TIM ID: ' + splitPayload[6] + '</span><br/>')
        $('#messages_details').append('<span>XDCR Chan ID: ' + splitPayload[7] + '</span><br/>')
        $('#messages_details').append('<span>XDCR Reading: ' + splitPayload[8] + '</span><br/>')
        $('#messages_details').append('<span>Time Stamp: ' + splitPayload[9] + '</span><br/>')
        addData(myChart, splitPayload[9], splitPayload[8]);
        currentTemp = parseFloat(splitPayload[8]);
        tempDiff = userSetPoint - currentTemp;
        tempDiffString = String(tempDiff.toFixed(1))
        $('#ControlAmount').html('<p>Temperature Error: ' + String(tempDiff) + '</p>')
      }
    }
    else if (splitPayload[0] == '4') {
      $('#messages_details').append('<span>Network Service ID: ' + splitPayload[1] + '</span><br/>')
      $('#messages_details').append('<span>Message Type: ' + splitPayload[2] + '</span><br/>')
      if (splitPayload[1]=='1'){
        $('#messages_details').append('<span>Message Length(Bytes): ' + splitPayload[3] + '</span><br/>')
        $('#messages_details').append('<span>Error Code: ' + splitPayload[4] + '</span><br/>')
        $('#messages_details').append('<span>APPL ID: ' + splitPayload[5] + '</span><br/>')
        $('#messages_details').append('<span>Subscription ID: ' + splitPayload[6] + '</span><br/>')
        $('#messages_details').append('<span>NCAP ID: ' + splitPayload[7] + '</span><br/>')
        $('#messages_details').append('<span>TIM ID: ' + splitPayload[8] + '</span><br/>')
        $('#messages_details').append('<span>XDCR Chan ID: ' + splitPayload[9] + '</span><br/>')
      }
      else if (splitPayload[1]=='2'){
        $('#messages_details').append('<span>Message Length(Bytes): ' + splitPayload[3] + '</span><br/>')
        $('#messages_details').append('<span>Error Code: ' + splitPayload[4] + '</span><br/>')
        $('#messages_details').append('<span>NCAP ID: ' + splitPayload[5] + '</span><br/>')
        $('#messages_details').append('<span>TIM ID: ' + splitPayload[6] + '</span><br/>')
        $('#messages_details').append('<span>XDCR Chan ID: ' + splitPayload[7] + '</span><br/>')
        addRowAlertTable(splitPayload[7], time)

      }
    }
  }
};

//Connect Options
var options = {
  timeout: 3,
  //Gets Called if the connection has sucessfully been established
  onSuccess: function() {
    alert("Connected");
  },
  //Gets Called if the connection could not be established
  onFailure: function(message) {
    alert("Connection failed: " + message.errorMessage);
  }
};

var setUserNCAPID = function setUserNCAPID(){
   userNCAPID=document.getElementById('input1').value;
}

var setUserAPPLID = function setUserAPPLID(){
   userAPPLID=document.getElementById('input2').value;
}

var setUserChanID = function setUserChanID(){
   userChanID=document.getElementById('userChanID').value;
}

var setUserSetPoint = function (){
  userSetPoint=document.getElementById('setPoint').value;
}

//Creates a new Messaging.Message Object and sends it to the HiveMQ MQTT Broker
var publish = function(payload, topic, qos) {
  //Send your message (also possible to serialize it as JSON or protobuf or just use a string, no limitations)
  var message = new Paho.MQTT.Message(payload);
  message.destinationName = topic + userNCAPID;
  message.qos = qos;
  client.send(message);
  $('#sentMessages').html('');
  $('#sentMessages').append('<span>Payload Sent: ' + payload + '</span><br/>');
  var splitPayload = message.payloadString.split(",");
  if (splitPayload[0] == 1){
    $('#sentMessages').append('<span>Network Service Type: ' + splitPayload[0] + '</span><br/>')
    $('#sentMessages').append('<span>Network Service ID: ' + splitPayload[1] + '</span><br/>')
    $('#sentMessages').append('<span>Message Type: ' + splitPayload[2] + '</span><br/>')
    if (splitPayload[1] == '3'){
      $('#sentMessages').append('<span>Message Length(Bytes): ' + splitPayload[3] + '</span><br/>')
      $('#sentMessages').append('<span>Application ID: ' + splitPayload[4] + '</span><br/>')
    }
    else if (splitPayload[1] == '5'){
      $('#sentMessages').append('<span>Message Length(Bytes): ' + splitPayload[3] + '</span><br/>')
      $('#sentMessages').append('<span>Error Code: ' + splitPayload[4] + '</span><br/>')
      $('#sentMessages').append('<span>NCAP ID: ' + splitPayload[5] + '</span><br/>')
    }
    else if (splitPayload[1] == '6'){
      $('#sentMessages').append('<span>Message Length(Bytes): ' + splitPayload[3] + '</span><br/>')
      $('#sentMessages').append('<span>NCAP ID: ' + splitPayload[4] + '</span><br/>')
      $('#sentMessages').append('<span>TIM ID: ' + splitPayload[5] + '</span><br/>')
    }
  }
}

var subscribe = function(topic, qos){
  client.subscribe(topic + userAPPLID, qos);
}


var addRowNetTable = function (NCAPID, NCAPName, NCAPAddress) {
  var table = document.getElementById("networkEntityTable");
  var row = table.insertRow(-1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  cell1.innerHTML = NCAPID;
  cell2.innerHTML = NCAPName;
  cell3.innerHTML = NCAPAddress;
}

var addRowHeartbeatTable = function (NCAPID, time){
  var table = document.getElementById("heartbeatTable2");
  if (activeNCAPS.includes(NCAPID)){
    table.rows[activeNCAPS.indexOf(NCAPID)+1].cells[1].innerHTML = time;
  }
  else{
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.innerHTML = NCAPID;
    cell2.innerHTML = time;
    activeNCAPS.push(NCAPID)
  }
}

var addRowAlertTable = function (XDCR_Channel, time){
  var table = document.getElementById("transducerEventTable");
  if (activeXDCR.includes(XDCR_Channel)){
    table.rows[activeXDCR.indexOf(XDCR_Channel)+1].cells[1].innerHTML = time;
  }
  else{
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.innerHTML = XDCR_Channel;
    cell2.innerHTML = time;
    activeNCAPS.push(activeXDCR)
  }
}


var discoverNCAP = function (NCAPID){
  subscribe('RUSMARTLAB/', {qos: 2});
  // Send NCAP Discover Command
  // netSvcType, netSvcId, msgType, msgLength, appId, timeout
  // Publish to the NCAPID as set by button and user field.
  var NCAP_DiscoverPreamble = '1,3,1,8,';
  publish(NCAP_DiscoverPreamble.concat(userAPPLID, ',1'), 'RUSMARTLAB/',2);
  //publish('1,5,1,16,1,1', 'RUSMARTLAB/',2);
  //publish('1,6,1,16,1,1', 'RUSMARTLAB/',2);
}

var addData = function (chart, label, data) {
    //var ctx = document.getElementById('myChart').getContext('2d');
    //chart = myChart;
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

var removeData = function (chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}
