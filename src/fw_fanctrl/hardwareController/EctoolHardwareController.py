import re
import ctypes
from abc import ABC
from fw_fanctrl.hardwareController.HardwareController import HardwareController

class ECResult(ctypes.Structure):
    _fields_ = [("result_value", ctypes.c_char * 100)]

try:
    ectool_lib = ctypes.CDLL('./ec_lib.so')  # Hardcoded for testing
    ectool_lib.get_tempsinfo_all.restype = ctypes.c_char_p
    ectool_lib.get_temp_sensor.restype = ECResult
    ectool_lib.get_temp_sensor.argtypes = [ctypes.c_char_p]
    ectool_lib.get_temps_all.restype = ctypes.c_char_p
    ectool_lib.set_fan_duty.restype = ECResult
    ectool_lib.set_fan_duty.argtypes = [ctypes.c_int]
    ectool_lib.get_battery_info.restype = ctypes.c_char_p
    ectool_lib.set_auto_fan_control.restype = ctypes.c_char_p
except Exception as e:
    print(f"Failed to load the ectool library: {e}")

class EctoolHardwareController(HardwareController, ABC):
    noBatterySensorMode = False
    nonBatterySensors = None

    def __init__(self, no_battery_sensor_mode=False):
        if no_battery_sensor_mode:
            self.noBatterySensorMode = True
            self.populate_non_battery_sensors()

    def populate_non_battery_sensors(self):
        self.nonBatterySensors = []
        try:
            raw_out = ectool_lib.get_tempsinfo_all().decode('utf-8')
            battery_sensors_raw = re.findall(r"\d+ Battery", raw_out, re.MULTILINE)
            battery_sensors = [x.split(" ")[0] for x in battery_sensors_raw]
            for x in re.findall(r"^\d+", raw_out, re.MULTILINE):
                if x not in battery_sensors:
                    self.nonBatterySensors.append(x)
        except Exception as e:
            print(f"falling back to subprocess: {e}")
            # Implement fallback logic here

    def get_temperature(self):
        try:
            if self.noBatterySensorMode:
                raw_out = ""
                for x in self.nonBatterySensors:
                    result = ectool_lib.get_temp_sensor(x.encode('utf-8'))
                    sensor_output = result.result_value.decode('utf-8')
                    raw_out += sensor_output
            else:
                raw_out = ectool_lib.get_temps_all().decode('utf-8')
            raw_temps = re.findall(r"\(= (\d+) C\)", raw_out)
            temps = sorted([x for x in [int(x) for x in raw_temps] if x > 0], reverse=True)
            if len(temps) == 0:
                return 50
            return float(round(temps[0], 2))
        except Exception as e:
            print(f"falling back to subprocess: {e}")
            # Implement fallback logic here
            return 50

    def set_speed(self, speed):
        try:
            result = ectool_lib.set_fan_duty(int(speed))
            # Check result.result_value if needed
        except Exception as e:
            # Implement fallback logic here
            print(f"falling back to subprocess: {e}")

    def is_on_ac(self):
        try:
            raw_out = ectool_lib.get_battery_info().decode('utf-8')
            return "AC_PRESENT" in raw_out
        except Exception as e:
            print(f"falling back to subprocess: {e}")
            # Implement fallback logic here
            return False

    def pause(self):
        try:
            # Add any required arguments if needed
            ectool_lib.set_auto_fan_control()
        except Exception as e:
            print(f"falling back to subprocess: {e}")
            # Implement fallback logic here

    def resume(self):
        # Empty for ectool, as setting an arbitrary speed disables the automatic fan control
        pass
