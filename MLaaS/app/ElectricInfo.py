from pydantic import BaseModel
class ElectricInfo(BaseModel):
	Id: int
	Date: str
	Time: str
	Global_active_power: float
	Global_reactive_power: float
	Voltage: float
	Global_intensity: float
	Sub_metering_1: float
	Sub_metering_2: float
	Sub_metering_3: float