from nicegui import Event, ui, app
import paho.mqtt.client as mqtt
import nats
import asyncio
import ElectricInfo

mqtt_sensor = Event[ElectricInfo.ElectricInfo]()
nats_sensor = Event[str]()

async def start_mqtt_client():
    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"Connected to MQTT server with code {reason_code}")
        client.subscribe("highvoltage")

    def on_message(client, userdata, msg):
        my_message = ElectricInfo.ElectricInfo(msg.payload)
        mqtt_sensor.emit(my_message)

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect("localhost", 1883, 60)
    mqttc.loop_start()

async def start_nats_client():
    async def on_message(msg):
        subject = msg.subject
        data = msg.data.decode()
        nats_sensor.emit(data)

    nats_server = "nats://localhost:4222"
    nats_client = await nats.connect(nats_server)

    print("Connected to NATS on " + nats_server)
    subscription = await nats_client.subscribe("analyzed", cb=on_message)
    
    while True:
        await asyncio.sleep(1)


def parse_message(message):
    return message

@ui.refreshable
def display_mqtt_messages(messages) -> None:
    for electric_info in messages:
        with ui.element().classes("flex flex-col mx-auto mt-2 mb-2 p-2 w-[80%] h-fit bg-[#E56515] rounded-3xl"):
            ui.label("ID: " + str(electric_info.id)).classes("flex text-center mx-auto wrap-anywhere")
            ui.label("Date: " + electric_info.date + " " + electric_info.time).classes("flex text-center mx-auto wrap-anywhere")
            ui.label("Global Active Power: " + str(electric_info.global_active_power)).classes("flex text-center mx-auto wrap-anywhere")
            ui.label("Global Reactive Power: " + str(electric_info.global_reactive_power)).classes("flex text-center mx-auto wrap-anywhere")
            ui.label("Global Intensity: " + str(electric_info.global_intensity)).classes("flex text-center mx-auto wrap-anywhere")
            ui.label("Voltage: " + str(electric_info.voltage)).classes("flex text-center mx-auto wrap-anywhere")
            ui.label("SM1: " + str(electric_info.sub_metering_1) + " SM2: " + str(electric_info.sub_metering_2) + " SM3: " + str(electric_info.sub_metering_3)).classes("flex text-center mx-auto wrap-anywhere")


@ui.refreshable
def display_nats_messages(messages) -> None:
    for message in messages:
        with ui.element().classes("flex mx-auto mt-2 mb-2 p-2 w-fit bg-[#FBA45C] rounded-3xl text-wrap"):
            ui.label(message).classes("flex text-center mx-auto wrap-anywhere")

def full_page():
    ui.add_css('''
        #c0 {
            background-color: #919599
        }
        #c3 {
            height: 100vh
        }
    ''')

    mqtt_messages = []
    nats_messages = []

    def update_mqtt_messages(message: ElectricInfo.ElectricInfo):
        print("Recieved update from MQTT! " + message.__str__())
        mqtt_messages.insert(0, message)
        display_mqtt_messages.refresh()

    def update_nats_messages(message: str):
        print("Recieved update from NATS! " + message)
        nats_messages.insert(0, message)
        display_nats_messages.refresh()

    with ui.row().classes("flex w-full h-full"):
        with ui.element().classes("flex flex-nowrap flex-col mx-auto my-auto w-[40%] h-120 bg-[#CDCDCB] rounded-3xl"):
            ui.label("MQTT messages").classes("flex mx-auto mt-1 mb-1")
            display_mqtt_messages(mqtt_messages)

        with ui.element().classes("flex flex-col overflow-y-scroll mx-auto my-auto w-[40%] h-120 bg-[#CDCDCB] rounded-3xl"):
            ui.label("NATS messages").classes("flex mx-auto mt-1 mb-1")
            display_nats_messages(nats_messages)
    
    mqtt_sensor.subscribe(update_mqtt_messages)
    nats_sensor.subscribe(update_nats_messages)

app.on_startup(start_mqtt_client())
app.on_startup(start_nats_client())

ui.run(full_page)


#919599
#CDCDCB
#F8F8F8
#FBA45C
#E56515


