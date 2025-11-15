from typing import Union
from pydantic import BaseModel

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import json

from ElectricInfo import ElectricInfo

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


@app.post("/analyze")
def analyze_electric_info(electric_info: ElectricInfo):
    if electric_info.Global_active_power > 4:
        return {electric_info.Id, "High Power Usage"}
    if electric_info.Global_active_power < 1:
        return {electric_info.Id, "Low Power Usage"}    
    return {electric_info.Id, "Average Power Usage"}


            
