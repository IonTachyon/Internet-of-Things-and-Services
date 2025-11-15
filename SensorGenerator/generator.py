import http.client
import time
import ElectricInfo

file = open("household_power_consumption.txt")

read_from_save_file = open("seek.txt", "r")
seek = int(read_from_save_file.readline())
read_from_save_file.close()

file.seek(seek, 0)

for x in range(25):
    line = file.readline()
    electric_info = ElectricInfo.ElectricInfo(line)
    print(electric_info.jsonify().__str__())
    httpClient = http.client.HTTPConnection("localhost:8080")
    httpClient.request("POST", "/electric", body = electric_info.jsonify())
    seek = file.tell()
    time.sleep(2)

save_file = open("seek.txt", "w")
save_file.write(str(seek))

file.close()
save_file.close()