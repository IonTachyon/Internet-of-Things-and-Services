from typing import Union
from pydantic import BaseModel

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from google.protobuf.json_format import MessageToJson
import json

from ElectricInfo import ElectricInfo

import grpc
import datamanager_pb2_grpc
import datamanager_pb2

from fastapi import FastAPI

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello():
    return {"Hello": "World"}


@app.get("/electric/{id}")
def read_electric_info(id: int):
    with grpc.insecure_channel('datamanager:8080') as channel:
            stub = datamanager_pb2_grpc.DataManagerStub(channel)
            stub_request = datamanager_pb2.ElectricID(
                id = id
            )
            stub_response = stub.Read(stub_request)
            print(stub_response)
            json_string = MessageToJson(stub_response)
            json_true = json.loads(json_string) 
            print(json_true)
            return json_true

@app.put("/electric")
def update_electric_info(electric_info: ElectricInfo):
    with grpc.insecure_channel('datamanager:8080') as channel:
            stub = datamanager_pb2_grpc.DataManagerStub(channel)
            stub_request = datamanager_pb2.ElectricInfo(
                id = electric_info.id,
                date = electric_info.date,
                time = electric_info.time,
                global_active_power = electric_info.global_active_power,
                global_reactive_power = electric_info.global_reactive_power,
                global_intensity = electric_info.global_intensity,
                voltage = electric_info.voltage,
                sub_metering_1 = electric_info.sub_metering_1,
	            sub_metering_2 = electric_info.sub_metering_2,
	            sub_metering_3 = electric_info.sub_metering_3
            )
            stub_response = stub.Update(stub_request)
            json_string = MessageToJson(stub_response)
            json_true = json.loads(json_string) 
            print(json_true)
            return json_true

@app.post("/electric")
def add_electric_info(electric_info: ElectricInfo):
    with grpc.insecure_channel('datamanager:8080') as channel:
            stub = datamanager_pb2_grpc.DataManagerStub(channel)
            stub_request = datamanager_pb2.ElectricInfo(
                id = electric_info.id,
                date = electric_info.date,
                time = electric_info.time,
                global_active_power = electric_info.global_active_power,
                global_reactive_power = electric_info.global_reactive_power,
                global_intensity = electric_info.global_intensity,
                voltage = electric_info.voltage,
                sub_metering_1 = electric_info.sub_metering_1,
	            sub_metering_2 = electric_info.sub_metering_2,
	            sub_metering_3 = electric_info.sub_metering_3
            )
            stub_response = stub.Create(stub_request)
            json_string = MessageToJson(stub_response)
            json_true = json.loads(json_string) 
            print(json_true)
            return json_true

@app.delete("/electric/{id}")
def delete_electric_info(id: int):
    with grpc.insecure_channel('datamanager:8080') as channel:
            stub = datamanager_pb2_grpc.DataManagerStub(channel)
            stub_request = datamanager_pb2.ElectricID(
                id = id
            )
            stub_response = stub.Delete(stub_request)
            print(stub_response)
            json_string = MessageToJson(stub_response)
            json_true = json.loads(json_string) 
            print(json_true)
            return json_true

@app.get("/electric/span/{start_date}/{end_date}")
def get_date_span(start_date: str, end_date: str):
    with grpc.insecure_channel('datamanager:8080') as channel:
            stub = datamanager_pb2_grpc.DataManagerStub(channel)
            stub_request = datamanager_pb2.DateSpan(
                start_date = start_date,
                end_date = end_date
            )
            stub_response = stub.ReadAllInDateSpan(stub_request)
            json_string = MessageToJson(stub_response)
            json_true = json.loads(json_string) 
            print(json_true)
            return json_true

@app.get("/electric/min/{start_date}/{end_date}")
def minimum_active_power(start_date: str, end_date: str):
    with grpc.insecure_channel('datamanager:8080') as channel:
            stub = datamanager_pb2_grpc.DataManagerStub(channel)
            stub_request = datamanager_pb2.DateSpan(
                start_date = start_date,
                end_date = end_date
            )
            stub_response = stub.ReadAllInDateSpan(stub_request)
            json_string = MessageToJson(stub_response)
            json_true = json.loads(json_string) 
            print(json_true)
            min_info = json_true["list"]["info"][0]
            for info in json_true["list"]["info"]:
                if min_info["globalActivePower"] > info["globalActivePower"]:
                    min_info = info
            return min_info

@app.get("/electric/max/{start_date}/{end_date}")
def maximum_active_power(start_date: str, end_date: str):
    with grpc.insecure_channel('datamanager:8080') as channel:
            stub = datamanager_pb2_grpc.DataManagerStub(channel)
            stub_request = datamanager_pb2.DateSpan(
                start_date = start_date,
                end_date = end_date
            )
            stub_response = stub.ReadAllInDateSpan(stub_request)
            json_string = MessageToJson(stub_response)
            json_true = json.loads(json_string) 
            print(json_true)
            max_info = json_true["list"]["info"][0]
            for info in json_true["list"]["info"]:
                if max_info["globalActivePower"] < info["globalActivePower"]:
                    max_info = info
            return max_info

@app.get("/electric/avg/{start_date}/{end_date}")
def average_active_power(start_date: str, end_date: str):
    with grpc.insecure_channel('datamanager:8080') as channel:
            stub = datamanager_pb2_grpc.DataManagerStub(channel)
            stub_request = datamanager_pb2.DateSpan(
                start_date = start_date,
                end_date = end_date
            )
            list = []
            stub_response = stub.ReadAllInDateSpan(stub_request)
            json_string = MessageToJson(stub_response)
            json_true = json.loads(json_string) 
            print(json_true)
            avg_active = 0
            for info in json_true["list"]["info"]:
                avg_active += info["globalActivePower"]
            avg_active /= len(json_true["list"]["info"])
            return avg_active

@app.get("/electric/sum/{start_date}/{end_date}")
def sum_of_active_power(start_date: str, end_date: str):
    with grpc.insecure_channel('datamanager:8080') as channel:
            stub = datamanager_pb2_grpc.DataManagerStub(channel)
            stub_request = datamanager_pb2.DateSpan(
                start_date = start_date,
                end_date = end_date
            )
            list = []
            stub_response = stub.ReadAllInDateSpan(stub_request)
            json_string = MessageToJson(stub_response)
            json_true = json.loads(json_string) 
            print(json_true)
            sum_active = 0
            for info in json_true["list"]["info"]:
                sum_active += info["globalActivePower"]
            return sum_active