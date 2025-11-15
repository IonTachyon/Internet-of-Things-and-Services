from pydantic import BaseModel
import json

class ElectricInfo:
	id: int
	date: str
	time: str
	global_active_power: float
	global_reactive_power: float
	voltage: float
	global_intensity: float
	sub_metering_1: float
	sub_metering_2: float
	sub_metering_3: float

	def __init__(self, string: str):
		jsonified = json.loads(string)
		self.id = jsonified["Id"]
		self.date = jsonified["Date"]
		self.time = jsonified["Time"]
		self.global_active_power = jsonified["Global_active_power"]
		self.global_reactive_power = jsonified["Global_reactive_power"]
		self.voltage = jsonified["Voltage"]
		self.global_intensity = jsonified["Global_intensity"]
		self.sub_metering_1 = jsonified["Sub_metering_1"]
		self.sub_metering_2 = jsonified["Sub_metering_2"]
		self.sub_metering_3 = jsonified["Sub_metering_3"]

	def __str__(self):
		return f'''
		ID: {str(self.id)} 
		Date: {self.date} Time: {self.time} 
		Global active power: {str(self.global_active_power)} Global reactive power: {str(self.global_reactive_power)} 
		Voltage: {str(self.voltage)} 
		Global Intensity: {str(self.global_intensity)} 
		Sub Metering 1: {str(self.sub_metering_1)} Sub Metering 2: {str(self.sub_metering_2)} Sub Metering 3: {str(self.sub_metering_3)}
		'''