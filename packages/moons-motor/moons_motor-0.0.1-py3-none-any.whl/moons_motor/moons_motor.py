import serial
from serial.tools import list_ports
import re
import time
import threading
import socketio
from rich import print
from rich.console import Console
from rich.panel import Panel
import queue


class moons_stepper_status:
    def __init__(self, address=""):

        # info
        self.address = ""
        self.position = 0  # IP
        self.temperature = 0  # IT
        self.sensor_status = 0  # IS
        self.voltage = 0  # IU
        self.acceleration = 0  # AC
        self.deceleration = 0  # DE
        self.velocity = 0  # VE
        self.distance = 0  # DI
        self.jog_speed = 0  # JS

        # status
        self.status_string = ""
        self.alarm = False
        self.disabled = False
        self.drive_fault = False
        self.moving = False
        self.homing = False
        self.jogging = False
        self.motion_in_progess = False
        self.ready = False
        self.stoping = False
        self.waiting = False

    def update_info(self, info: dict) -> bool:
        if info is None or len(info) < 1:
            print("Update failed: input is None")
            return False
        self.position = info["pos"]
        self.temperature = info["temp"]
        self.sensor_status = info["sensor"]
        self.voltage = info["vol"]
        self.acceleration = info["accel"]
        self.deceleration = info["decel"]
        self.velocity = info["vel"]
        self.distance = info["dis"]
        self.jog_speed = info["jogsp"]
        return True

    def update_status(self, status_string) -> bool:
        if status_string == None and status_string == "":
            print("Update failed: input is empty or None")
            return False
        self.status_string = status_string
        self.alarm = "A" in status_string
        self.disabled = "D" in status_string
        self.drive_fault = "E" in status_string
        self.moving = "F" in status_string
        self.homing = "H" in status_string
        self.jogging = "J" in status_string
        self.motion_in_progess = "M" in status_string
        self.ready = "R" in status_string
        self.stoping = "S" in status_string
        self.waiting = "T" in status_string
        return True

    def get_info(self) -> str:
        return f"""
        Position: {self.position}
        Temperature: {self.temperature}
        Sensor Status: {self.sensor_status}
        Voltage: {self.voltage}
        Acceleration: {self.acceleration}
        Deceleration: {self.deceleration}
        Velocity: {self.velocity}
        Distance: {self.distance}
        Jog Speed: {self.jog_speed}"""

    def get_status(self) -> str:
        return f"""
        Alarm: {self.alarm}
        Disabled: {self.disabled}
        Drive Fault: {self.drive_fault}
        Moving: {self.moving}
        Homing: {self.homing}
        Jogging: {self.jogging}
        Motion in Progress: {self.motion_in_progess}
        Ready: {self.ready}
        Stoping: {self.stoping}
        Waiting: {self.waiting}"""


class moons_stepper:
    motorAdress = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "!",
        '"',
        "#",
        "$",
        "%",
        "&",
        "'",
        "(",
        ")",
        "*",
        "+",
        ",",
        "-",
        ".",
        "/",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "@",
    ]

    def __init__(
        self,
        model,
        VID,
        PID,
        SERIAL_NUM,
        only_simlate=False,
        universe=0,
        simulate_ip="localhost",
        simulate_port=3001,
    ):
        self.universe = universe
        self.model = model
        self.only_simulate = only_simlate
        self.device = ""
        self.VID = VID
        self.PID = PID
        self.SERIAL_NUM = SERIAL_NUM
        self.ser = None
        self.listeningBuffer = ""
        self.listeningBufferPre = ""
        self.transmitDelay = 0.010
        self.lock = False
        self.Opened = False
        self.new_data_event = threading.Event()
        self.new_value_event = threading.Event()
        self.on_send_event = threading.Event()
        self.recvQueue = queue.Queue()
        self.sendQueue = queue.Queue()
        self.command_cache = queue.Queue()
        self.usedSendQueue = queue.Queue()
        self.simulator = moons_stepper_simulate(
            self,
            universe=universe,
            server_address=f"http://{simulate_ip}:{simulate_port}",
        )

        self.console = Console()

        self.is_log_message = True

        self.microstep = {
            0: 200,
            1: 400,
            3: 2000,
            4: 5000,
            5: 10000,
            6: 12800,
            7: 18000,
            8: 20000,
            9: 21600,
            10: 25000,
            11: 25400,
            12: 25600,
            13: 36000,
            14: 50000,
            15: 50800,
        }
        self.simulator.connect()

    # region connection & main functions
    @staticmethod
    def list_all_ports():
        # print("░░░░░░░░░░░░░░░░░░░ All COMPorts ░░░░░░░░░░░░░░░░░░░░░\n")
        ports = list(list_ports.comports())
        simple_ports = []
        port_info = ""
        for p in ports:
            port_info += f"■ {p.device} {p.description} [blue]{p.usb_info()}[/blue]"
            if p != ports[-1]:
                port_info += "\n"
            simple_ports.append(p.description)
        # print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
        print(Panel(port_info, title="All COMPorts"))
        return simple_ports

    def connect(self, COM=None, baudrate=9600, callback=None):
        if self.only_simulate:
            self.Opened = True
            self.device = f"Simulate-{self.universe}"
            print(f"{self.device} connected")
            if callback:
                callback(self.device, self.Opened)
            return

        def attempt_connect(COM, baudrate):
            try:
                self.ser = serial.Serial(COM, baudrate)
                if self.ser is None:
                    print("> Device not found")
                    self.Opened = False
                if self.ser.is_open:
                    print(f"Device: {self.device} | COM: {COM} connected")
                    self.Opened = True
            except:
                print("> Device error")
                self.Opened = False

        if COM is not None and not self.only_simulate:
            attempt_connect(COM, baudrate)
            if callback:
                callback(self.device, self.Opened)
            return
        ports = list(list_ports.comports())
        for p in ports:
            m = re.match(
                r"USB\s*VID:PID=(\w+):(\w+)\s*SER=([A-Za-z0-9]+)", p.usb_info()
            )
            if (
                m
                and m.group(1) == self.VID
                and m.group(2) == self.PID
                and m.group(3) == self.SERIAL_NUM
            ):
                print(
                    f"Device: {p.description} | VID: {m.group(1)} | PID: {m.group(2)} | SER: {m.group(3)} connected"
                )

                self.device = p.description

                attempt_connect(p.device, baudrate)
                if callback:
                    callback(self.device, self.Opened)
                    break
                # try:
                #     self.ser = serial.Serial(p.device, baudrate)
                # except Exception as e:
                #     print(f"Permission Error: {e}")
                #     self.Opened = False
                #     return

                # self.listeningThread = threading.Thread(target=self.listening)
                # self.sendingThread = threading.Thread(target=self.sending)
                # self.listeningThread.daemon = True
                # self.sendingThread.daemon = True
                # self.listeningThread.start()
                # self.sendingThread.start()

                break

            if self.only_simulate:
                self.device = "Simulate"
                self.Opened = True
            if not self.Opened:
                print("> Device not found")
                if callback:
                    callback(self.device, self.Opened)
                # self.sendingThread = threading.Thread(target=self.sending)
                # self.sendingThread.daemon = True
                # self.sendingThread.start()
        # self.device = "Target device"
        # if self.ser is None and not self.only_simlate:
        #     print("> Device not found")
        #     self.Opened = False

    def disconnect(self):
        if self.only_simulate:
            self.listen = False
            self.is_sending = False
            self.Opened = False
            print(f"Simulate-{self.universe} disconnected")
            return
        if self.ser is not None and self.ser.is_open:
            self.listen = False
            self.is_sending = False
            self.Opened = False
            self.ser.flush()
            self.ser.close()
            # if self.device is not None:
            #     print("{} Disconnected".format(self.device))
            # else:
            print(f"{self.device} Disconnected")

    def send(self, command, eol=b"\r"):
        if (self.ser != None and self.ser.is_open) or self.only_simulate:
            # self.sendQueue.put(command + "\r")
            # self.temp_cmd = self.sendQueue.get()
            self.temp_cmd = command + "\r"

            if "~" in self.temp_cmd:
                # remove ~ in self.temp_cmd
                self.temp_cmd = self.temp_cmd[1:]
            else:
                self.usedSendQueue.put(self.temp_cmd)
                # self.command_cache.put(self.temp_cmd)
            if self.ser is not None or not self.only_simulate:
                self.ser.write(self.temp_cmd.encode("ascii"))
            if self.is_log_message:
                print(
                    f"[bold green]Send to {self.device}:[/bold green] {self.temp_cmd}"
                )
            self.simulator.emit("motor", f"{self.universe}-{self.temp_cmd}")
        else:
            print(f"{self.device} is not open")

    def sending(self):
        self.is_sending = True
        print("Sending thread started")
        # start_time = time.time()
        try:
            while self.is_sending:
                # start_time = time.time()
                if self.sendQueue.empty():
                    continue
                # self.temp_cmd = ""
                self.temp_cmd = self.sendQueue.get_nowait()

                if "~" in self.temp_cmd:
                    # remove ~ in self.temp_cmd
                    self.temp_cmd = self.temp_cmd[1:]
                else:
                    self.usedSendQueue.put(self.temp_cmd)
                # self.command_cache.put(self.temp_cmd)

                if self.ser is not None and self.ser.is_open is not self.only_simulate:
                    self.ser.write(self.temp_cmd.encode("ascii"))
                # print(
                #     f"[bold green]Send to {self.device}:[/bold green] {self.temp_cmd}"
                # )
                # self.simulate.emit("motor", f"{self.universe}-{self.temp_cmd}")
                # print(f"[bold yellow]Cache:[/bold yellow]{self.temp_cmd}")

                self.sendQueue.task_done()

                time.sleep(0.05)

        except Exception as e:
            print("Error in sending thread:")
            print(e)
            self.is_sending = False

    def listening(self):
        self.listen = True
        self.listeningBuffer = ""
        print("Listening thread started")
        # start_time = time.time()
        try:
            while True:
                # start_time = time.time()
                if not self.listen:
                    break
                if self.only_simulate:
                    continue
                if self.ser is not None and self.ser.is_open:
                    if self.ser.in_waiting > 0:
                        self.listeningBuffer += self.ser.read(1).decode(
                            "utf-8", "replace"
                        )
                        if self.listeningBuffer.endswith("\r"):
                            self.recvQueue.put(self.listeningBuffer)
                            self.listeningBuffer = ""
                else:
                    print(f"{self.device} is not open")
                if not self.recvQueue.empty():
                    self.temp_recv = self.recvQueue.get()
                    self.temp_used_cmd = self.usedSendQueue.get()
                    print(
                        f"[bold green]Recv:[/bold green] {self.temp_used_cmd}->{self.temp_recv}"
                    )
                    self.recvQueue.task_done()
                    self.usedSendQueue.task_done()
                time.sleep(0.05)
                # print(f"Time: {time.time()-start_time}")
        except Exception as e:
            print("Error in listening thread:")
            print(e)
            self.listen = False
        print("Listening thread stopped")

    # endregion

    # region motor motion functions
    def enable(self, motor_address="", enable=True):
        cmd = "ME" if enable else "MD"
        self.send(self.addressed_cmd(motor_address, cmd))

    def move_absolute(self, motor_address="", position=0, speed=0.15):
        # if speed > 0:
        #     self.set_velocity(motor_address, speed)
        self.send(self.addressed_cmd(motor_address, f"VE{speed}"))
        self.send(self.addressed_cmd(motor_address, f"FP{position}"))

    def move_fixed_distance(self, motor_address="", distance=100, speed=0.15):
        # if speed > 0:
        #     self.set_velocity(motor_address, speed)
        self.send(self.addressed_cmd(motor_address, "VE{}".format(speed)))
        self.send(self.addressed_cmd(motor_address, "FL{}".format(int(distance))))

    def start_jog(self, motor_address="", speed=0.15, direction="CW"):
        # if direction == "CW":
        #     self.send(self.addressed_cmd(motor_address, "DI1"))
        # if direction == "CCW":
        #     self.send(self.addressed_cmd(motor_address, "DI-1"))
        self.send(self.addressed_cmd(motor_address, "JS{}".format(speed)))
        self.send(self.addressed_cmd(motor_address, "CJ"))

    def change_jog_speed(self, motor_address="", speed=0.15):
        self.send(self.addressed_cmd(motor_address, "CS{}".format(speed)))

    def stop_jog(self, motor_address=""):
        self.send(self.addressed_cmd(motor_address, "SJ"))

    def stop(self, motor_address=""):
        self.send(self.addressed_cmd(motor_address, "ST"))

    def stop_with_deceleration(self, motor_address=""):
        self.send(self.addressed_cmd(motor_address, "STD"))

    def stop_and_kill(self, motor_address="", with_deceleration=True):
        if with_deceleration:
            self.send(self.addressed_cmd(motor_address, "SKD"))
        else:
            self.send(self.addressed_cmd(motor_address, "SK"))

    def setup_motor(self, motor_address="", kill=False):
        if kill:
            self.stop_and_kill(motor_address)
        # time.sleep(1)
        self.set_transmit_delay(motor_address, 25)
        self.set_return_format_dexcimal(motor_address)
        # self.motor_wait(motor_address, 0.1)
        # status = self.get_status(motor_address)

    def calibrate(self, motor_address="", speed=0.3, onStart=None, onComplete=None):
        self.send(self.addressed_cmd(motor_address, "VE{}".format(speed)))
        # self.send(self.addressed_cmd(motor_address, "WT0.2"))
        self.send(self.addressed_cmd(motor_address, "DI10"))
        # time.sleep(self.transmitDelay)
        # self.send(self.addressed_cmd(motor_address, "FS3F"))
        self.send(self.addressed_cmd(motor_address, "SH3F"))
        self.send(self.addressed_cmd(motor_address, "EP0"))
        self.send(self.addressed_cmd(motor_address, "SP0"))

    # speed slow= 0.25, medium=1, fast=5
    def set_transmit_delay(self, motor_address="", delay=15):
        self.send(self.addressed_cmd(motor_address, "TD{}".format(delay)))

    # endregion
    # region motor status functions
    def get_position(self, motor_address):
        self.send(self.addressed_cmd(motor_address, "IP"))
        self.new_value_event.wait(timeout=0.5)
        return self.get_value()

    def get_temperature(self, motor_address):
        self.send(self.addressed_cmd(motor_address, "IT"))
        self.new_value_event.wait(timeout=0.5)
        return int(self.get_value()) / 10

    def get_sensor_status(self, motor_address):
        self.send(self.addressed_cmd(motor_address, "IS"))
        self.new_value_event.wait(timeout=0.5)
        return self.get_value()

    def get_votalge(self, motor_address):
        self.send(self.addressed_cmd(motor_address, "IU"))
        self.new_value_event.wait(timeout=0.5)
        return self.get_value()

    def get_acceleration(self, motor_address):
        self.send(self.addressed_cmd(motor_address, "AC"))
        self.new_value_event.wait(timeout=0.5)
        return self.get_value()

    def get_deceleration(self, motor_address):
        self.send(self.addressed_cmd(motor_address, "DE"))
        self.new_value_event.wait(timeout=0.5)
        return self.get_value()

    def get_velocity(self, motor_address):
        self.send(self.addressed_cmd(motor_address, "VE"))
        self.new_value_event.wait(timeout=0.5)
        return self.get_value()

    def get_distance(self, motor_address):
        self.send(self.addressed_cmd(motor_address, "DI"))
        self.new_value_event.wait(timeout=0.5)
        return self.get_value()

    def get_jog_speed(self, motor_address):
        self.send(self.addressed_cmd(motor_address, "JS"))
        self.new_value_event.wait(timeout=0.5)
        return self.get_value()

    def get_info(self, motor_address):
        self.set_return_format_dexcimal(motor_address)
        self.motor_wait(motor_address, 0.1)
        info = {
            "pos": str(self.get_position(motor_address)),
            "temp": str(self.get_temperature(motor_address)),
            "sensor": str(self.get_sensor_status(motor_address)),
            "vol": str(self.get_votalge(motor_address)),
            "accel": str(self.get_acceleration(motor_address)),
            "decel": str(self.get_deceleration(motor_address)),
            "vel": str(self.get_velocity(motor_address)),
            "dis": str(self.get_distance(motor_address)),
            "jogsp": str(self.get_jog_speed(motor_address)),
        }
        return info

    def get_status(self, motor_address) -> str:
        self.set_return_format_dexcimal(motor_address)
        self.send(self.addressed_cmd(motor_address, "RS"))
        self.new_value_event.wait(timeout=0.5)
        return str(self.get_value())

    def set_return_format_dexcimal(self, motor_address):
        self.send(self.addressed_cmd(motor_address, "IFD"))

    def set_return_format_hexdecimal(self, motor_address):
        self.send(self.addressed_cmd(motor_address, "IFH"))

    # endregion

    # region utility functions
    def motor_wait(self, motor_address, wait_time):
        self.send(self.addressed_cmd(motor_address, "WT{}".format(wait_time)))

    def addressed_cmd(self, motor_address, command):
        if motor_address == "":
            return f"~{command}"
        return f"{motor_address}{command}"

    def get_value(self):
        print("Waiting for value")
        self.new_data_event.wait(timeout=0.5)
        print("Recv:" + self.listeningBufferPre)
        self.new_data_event.clear()
        if "%" in self.listeningBufferPre:
            return "success_ack"
        if "?" in self.listeningBufferPre:
            return "fail_ack"
        if "*" in self.listeningBufferPre:
            return "buffered_ack"
        self.new_value_event.set()
        pattern = r"=(\w+(?:\.\w+)?|\d+(?:\.\d+)?)"
        result = re.search(pattern, self.listeningBufferPre)
        self.listeningBufferPre = ""
        self.new_value_event.clear()
        if result:
            return result.group(1)
        else:
            return "No_value_found"


class moons_stepper_simulate:
    def __init__(
        self,
        moons_motor: moons_stepper,
        universe: int = 0,
        server_address: str = "http://localhost:3001",
    ):
        self.server_address = server_address
        self.universe = universe
        self.moons_motor = moons_motor
        self.io = socketio.SimpleClient()
        self.connected = False
        self.is_log_message = True

    def connect(self):
        try:
            self.is_log_message = False
            self.io.connect(self.server_address)
            self.connected = True
            print(f"Socket connected to {self.server_address}[{self.io.sid}]")
            # self.rederict_thread = threading.Thread(
            #     target=self.rederict_job,
            # )
            # self.rederict_thread.daemon = True
            # self.rederict_thread.start()
        except Exception as e:
            print(f"Socket connection error: {e}")
            self.connected = False

    def rederict_job(self):
        if not self.connected:
            print("Socket not connected")
            return
        if self.moons_motor is None:
            print("Motor is None")
            return
        while True:
            # self.moons_motor.on_send_event.wait(timeout=0.5)
            if self.moons_motor.command_cache.empty():
                continue
            cmd = self.moons_motor.command_cache.get_nowait()
            # self.moons_motor.command_cache.task_done()

            self.emit("motor", f"{self.universe}-{cmd}")
            # self.moons_motor.command_cache = ""
            # self.moons_motor.on_send_event.clear()

            if not self.connected:
                break
            time.sleep(0.05)

    def disconnect(self):
        self.io.disconnect()

    def emit(self, eventName: str, data):
        if not self.connected:
            print("Socket not connected")
            return
        self.io.emit(eventName, data)
        if self.is_log_message:
            print("[bold blue]Send to socket:[/bold blue] {}\n".format(data))


# endregion

# SERIAL => 上次已知父系(尾巴+A) 或是事件分頁
# reg USB\s*VID:PID=(\w+):(\w+)\s*SER=([A-Za-z0-9]+)

# serial_num  裝置例項路徑
# TD(Tramsmit Delay) = 15
