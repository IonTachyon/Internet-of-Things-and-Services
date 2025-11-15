using Azure.Core;
using DataManager.Model;
using Grpc.Core;
using Microsoft.EntityFrameworkCore;
using MQTTnet;
using Newtonsoft.Json;

using static Microsoft.EntityFrameworkCore.DbLoggerCategory;

namespace DataManager.Services
{
    public class DataManagerService : DataManager.DataManagerBase
    {
        private DatabaseContext _dbContext;
        private IMqttClient _mqttClient;

        public DataManagerService(DatabaseContext dbContext, IMqttClient mqttClient) {
            _dbContext = dbContext;
            _mqttClient = mqttClient;
        }

        public override async Task<Response> Create(ElectricInfo request, ServerCallContext context)
        {
            ElectricInfoDB newEntity = ConvertToDBFormat(request);

            await _dbContext.AddAsync(newEntity);
            await _dbContext.SaveChangesAsync();

            Response response = new Response();
            response.Message = "Succesfully added new ElectricInfo!";
            response.Result = 200;
            response.List = new ElectricInfoList();

            MqttClientOptions options = new MqttClientOptionsBuilder()
                .WithClientId("datamanager")
                .WithTcpServer("mosquitto", 1883)
                .Build();

            await _mqttClient.ConnectAsync(options, CancellationToken.None);

            string json = JsonConvert.SerializeObject(newEntity);

            var applicationMessage = new MqttApplicationMessageBuilder()
            .WithTopic("newelectricinfo")
            .WithPayload(json)
            .Build();

            await _mqttClient.PublishAsync(applicationMessage, CancellationToken.None);

            await _mqttClient.DisconnectAsync();
            return response;
        }

        public override async Task<Response> Read(ElectricID request, ServerCallContext context)
        {
            ElectricInfoDB? electricInfoDB = await _dbContext.ElectricInfos.FindAsync(request.Id);
            
            if (electricInfoDB == null)
            {
                Response failResponse = new Response();
                failResponse.Message = "Failed to read ElectricInfo!";
                failResponse.Result = 400;
                failResponse.List = new ElectricInfoList();

                return failResponse;
            }

            ElectricInfoList list = new ElectricInfoList();
            ElectricInfo info = ConvertFromDBFormat(electricInfoDB);

            list.Info.Add(info);

            Response response = new Response();
            response.Message = "Successfully read ElectricInfo!";
            response.Result = 200;
            response.List = list;

            return response;
        }
        public override async Task<Response> Update(ElectricInfo request, ServerCallContext context)
        {
            ElectricInfoDB? toUpdate = await _dbContext.ElectricInfos.FindAsync(request.Id);
            if (toUpdate == null)
            {
                Response failResponse = new Response();
                failResponse.Message = "Failed to update ElectricInfo!";
                failResponse.Result = 400;
                failResponse.List = new ElectricInfoList();
                return failResponse;
            };

            ElectricInfoDB requestConverted = ConvertToDBFormat(request);
            toUpdate.Date = requestConverted.Date;
            toUpdate.Time = requestConverted.Time;

            toUpdate.Global_active_power = requestConverted.Global_active_power;
            toUpdate.Global_intensity = requestConverted.Global_intensity;
            toUpdate.Global_reactive_power = requestConverted.Global_reactive_power;

            toUpdate.Voltage = requestConverted.Voltage;

            toUpdate.Sub_metering_1 = requestConverted.Sub_metering_1;
            toUpdate.Sub_metering_2 = requestConverted.Sub_metering_2;
            toUpdate.Sub_metering_3 = requestConverted.Sub_metering_3;

            _dbContext.ElectricInfos.Update(toUpdate);
            await _dbContext.SaveChangesAsync();

            Response response = new Response();
            response.Message = "Succesfully updated ElectricInfo!";
            response.Result = 200;
            response.List = new ElectricInfoList();
            response.List.Info.Add(request);

            return response;
        }

        public override async Task<Response> Delete(ElectricID request, ServerCallContext context)
        {
            ElectricInfoDB? toDelete = await _dbContext.ElectricInfos.FindAsync(request.Id);
            if (toDelete == null)
            {
                Response failResponse = new Response();
                failResponse.Message = "Failed to update ElectricInfo!";
                failResponse.Result = 400;
                failResponse.List = new ElectricInfoList();
                return failResponse;
            }

            _dbContext.Remove(toDelete);
            await _dbContext.SaveChangesAsync();

            Response response = new Response();
            response.Message = "Succesfully deleted ElectricInfo!";
            response.Result = 200;
            response.List = new ElectricInfoList();
            response.List.Info.Add(ConvertFromDBFormat(toDelete));
            return response;
        }

        public override async Task<Response> ReadAllInDateSpan(DateSpan request, ServerCallContext context)
        {
            string[] dateValuesStart = request.StartDate.Split('-');
            string[] dateValuesEnd = request.EndDate.Split('-');

            DateOnly dateStart = new DateOnly(Int32.Parse(dateValuesStart[2]), Int32.Parse(dateValuesStart[1]), Int32.Parse(dateValuesStart[0]));
            DateOnly dateEnd = new DateOnly(Int32.Parse(dateValuesEnd[2]), Int32.Parse(dateValuesEnd[1]), Int32.Parse(dateValuesEnd[0]));

            List<ElectricInfoDB> electricInfoDBs = await _dbContext.ElectricInfos.Where(e => e.Date >= dateStart && e.Date <= dateEnd).ToListAsync();
            List<ElectricInfo> electricInfoList = new List<ElectricInfo>();

            Response response = new Response();
            response.Message = "Succesfully got all valid ElectricInfo!";
            response.Result = 200;
            response.List = new ElectricInfoList();

            foreach (ElectricInfoDB electricInfoDB in electricInfoDBs)
            {
                ElectricInfo info = ConvertFromDBFormat(electricInfoDB);
                response.List.Info.Add(info);
            }

            return response;
        }

        private ElectricInfoDB ConvertToDBFormat(ElectricInfo request)
        {
            string[] dateValues = request.Date.Split('-');
            string[] timeValues = request.Time.Split(":");

            ElectricInfoDB newEntity = new ElectricInfoDB
            {
                Date = new DateOnly(Int32.Parse(dateValues[2]), Int32.Parse(dateValues[1]), Int32.Parse(dateValues[0])),
                Time = new TimeOnly(Int32.Parse(timeValues[0]), Int32.Parse(timeValues[1]), Int32.Parse(timeValues[2])),
                Global_active_power = request.GlobalActivePower,
                Global_intensity = request.GlobalIntensity,
                Global_reactive_power = request.GlobalReactivePower,
                Voltage = request.Voltage,
                Sub_metering_1 = request.SubMetering1,
                Sub_metering_2 = request.SubMetering2,
                Sub_metering_3 = request.SubMetering3
            };

            if(request.Id != -1)
            {
                newEntity.Id = request.Id;
            }

            return newEntity;
        }

        private ElectricInfo ConvertFromDBFormat(ElectricInfoDB electricInfoDB)
        {
            ElectricInfo info = new ElectricInfo();

            string hour = electricInfoDB.Time.Hour < 10 ? $"0{electricInfoDB.Time.Hour}" : $"{electricInfoDB.Time.Hour}";
            string minute = electricInfoDB.Time.Minute < 10 ? $"0{electricInfoDB.Time.Minute}" : $"{electricInfoDB.Time.Minute}";
            string second = electricInfoDB.Time.Second < 10 ? $"0{electricInfoDB.Time.Second}" : $"{electricInfoDB.Time.Second}";
            
            info.Date = $"{electricInfoDB.Date.Day}-{electricInfoDB.Date.Month}-{electricInfoDB.Date.Year}";
            info.Time = $"{hour}:{minute}:{second}";
                
            info.GlobalActivePower = electricInfoDB.Global_active_power;
            info.GlobalIntensity = electricInfoDB.Global_intensity;
            info.GlobalReactivePower = electricInfoDB.Global_reactive_power;

            info.Voltage = electricInfoDB.Voltage;

            info.SubMetering1 = electricInfoDB.Sub_metering_1;
            info.SubMetering2 = electricInfoDB.Sub_metering_2;
            info.SubMetering3 = electricInfoDB.Sub_metering_3;

            return info;
        }
    }
}
