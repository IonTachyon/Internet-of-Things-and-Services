
using Newtonsoft.Json;
using MQTTnet;
using DataManager.Model;

var mqttFactory = new MqttClientFactory();
IMqttClient mqttClient = mqttFactory.CreateMqttClient();

MqttClientOptions options = new MqttClientOptionsBuilder().WithClientId("event_manager").WithTcpServer("mosquitto", 1883).Build();

mqttClient.ApplicationMessageReceivedAsync += async e =>
{
    string payload = e.ApplicationMessage.ConvertPayloadToString();
    ElectricInfoDB? electricInfoDB = JsonConvert.DeserializeObject<ElectricInfoDB>(payload);

    if (electricInfoDB == null)
    {
        Console.WriteLine("ElectricInfo failed to deserialize, or is null value!");
    }
    else if (electricInfoDB.Voltage > 235)
    {
        Console.WriteLine(electricInfoDB.ToString());
        
        var applicationMessage = new MqttApplicationMessageBuilder()
            .WithTopic("highvoltage")
            .WithPayload(payload)
            .Build();

        await mqttClient.PublishAsync(applicationMessage, CancellationToken.None);
    }
    return;
};

await mqttClient.ConnectAsync(options, CancellationToken.None);

var mqttSubscribeOptions = mqttFactory.CreateSubscribeOptionsBuilder().WithTopicFilter("newelectricinfo").Build();

await mqttClient.SubscribeAsync(mqttSubscribeOptions, CancellationToken.None);

Console.WriteLine("MQTT Client subscribed to topic.");

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.Run();
