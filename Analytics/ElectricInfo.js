class ElectricInfo {
    constructor(
        id, 
        date, 
        time, 
        global_active_power, 
        global_reactive_power, 
        voltage, 
        global_intensity, 
        sub_metering_1,
        sub_metering_2,
        sub_metering_3) 
        {
            this.id = id;
            this.date = date;
            this.time = time;
            this.global_active_power = global_active_power;
            this.global_reactive_power = global_reactive_power;
            this.voltage = voltage;
            this.global_intensity = global_intensity;
            this.sub_metering_1 = sub_metering_1;
            this.sub_metering_2 = sub_metering_2;
            this.sub_metering_3 = sub_metering_3;
        }
}
