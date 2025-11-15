import json

class ElectricInfo:
    def __init__(self, string: str):
        list_of_parameters = string.split(";")
        self.id = 0
        self.date = list_of_parameters[0]
        self.time = list_of_parameters[1]
        self.global_active_power = float(list_of_parameters[2])
        self.global_reactive_power = float(list_of_parameters[3])
        self.voltage = float(list_of_parameters[4])
        self.global_intensity = float(list_of_parameters[5])
        self.sub_metering_1 = float(list_of_parameters[6])
        self.sub_metering_2 = float(list_of_parameters[7])
        self.sub_metering_3 = float(list_of_parameters[8])
            
    def jsonify(self):
        return json.dumps(self.__dict__)
    
