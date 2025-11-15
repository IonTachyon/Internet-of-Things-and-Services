var mqtt = require('mqtt');
var nats = require('nats');
var axios = require('axios');
const { ElectricInfo } = require('./ElectricInfo');

const mqtt_host = 'mqtt://mosquitto:1883';
const nats_host = { servers: "nats://nats:4222" }
class MqttNatsClient
{
    constructor() {
        this.mqtt_client = null;
    }

    async connect() {
        this.mqtt_client = mqtt.connect(mqtt_host);

            this.mqtt_client.on('error', (err) => {
            console.log(err)
            })

            this.mqtt_client.on('connect', () => {
                console.log("MQTT mqtt_client connected to " + this.host)
            })

            this.mqtt_client.subscribe('highvoltage', {qos: 0});

            this.mqtt_client.on('message', async function(topic, message) {
                try
                {
                    var obj = JSON.parse(message);   
                    await axios.post('http://mlaas:80/analyze', obj)
                    .then(async reply => {
                        var codec = nats.StringCodec();
                        var nats_client = await nats.connect(nats_host);
                        nats_client.publish("analyzed", codec.encode(reply.data));
                        console.log(message.toString());   
                        nats_client.drain()
                    })
                    .catch(err => {
                        console.log(err)
                    })
                }
                catch(error)
                {
                    console.log(error)
                }
            });

            this.mqtt_client.on('close', () => {
                console.log("MQTT mqtt_client disconnected from " + this.host);
                this.nats_client.drain()
            });
        
    }
}


module.exports = MqttNatsClient