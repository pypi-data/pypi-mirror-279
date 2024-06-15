from motor import MoonsStepper, StepperModules
import simulate
from time import sleep

motor = MoonsStepper(StepperModules.STM17S_3RN, "0403", "6001", "TESTA", False)

simulate = simulate.moons_stepper_simulate(motor, 0, "http://localhost:3002")

MoonsStepper.list_all_ports()
motor.connect()
simulate.connect()

motor.start_jog("", 10)

sleep(5)

motor.stop_jog()
