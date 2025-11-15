from pydantic import BaseModel
class ElectricInfo(BaseModel):
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