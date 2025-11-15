using DataManager.Model;
using DataManager.Services;
using MQTTnet;

//using DataManager.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddGrpc();
builder.Services.AddGrpcReflection();
builder.Services.AddDbContext<DatabaseContext>(options =>
{
    options.UseNpgsql("Host=postgres;Port=5432;Database=Electric;Username=iontachyon;Password=testpassword11");
});

IMqttClient mqttclient = new MqttClientFactory().CreateMqttClient();

builder.Services.AddSingleton<IMqttClient>(mqttclient);

var app = builder.Build();

// Configure the HTTP request pipeline.
app.MapGet("/", () => "Communication with gRPC endpoints must be made through a gRPC client. To learn how to create a client, visit: https://go.microsoft.com/fwlink/?linkid=2086909");
app.MapGrpcService<DataManagerService>();
app.MapGrpcReflectionService();
app.Run();


