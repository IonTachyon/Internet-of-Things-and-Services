const MqttNatsClient = require("./MqttNatsClient");

var client = new MqttNatsClient();

client.connect();

console.log("MQTTnatsClient successfully connected!");

