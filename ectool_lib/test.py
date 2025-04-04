import unittest
import ctypes
import os
import sys

class ECResult(ctypes.Structure):
    _fields_ = [("result_value", ctypes.c_char * 100)]

class TestEctoolLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            # Adjust path if needed for your environment
            cls.ectool_lib = ctypes.CDLL('./ec_lib.so')

            # Set up function signatures
            cls.ectool_lib.get_tempsinfo_all.restype = ctypes.c_char_p

            cls.ectool_lib.get_temp_sensor.restype = ECResult
            cls.ectool_lib.get_temp_sensor.argtypes = [ctypes.c_char_p]

            cls.ectool_lib.get_temps_all.restype = ctypes.c_char_p

            cls.ectool_lib.set_fan_duty.restype = ECResult
            cls.ectool_lib.set_fan_duty.argtypes = [ctypes.c_int]

            cls.ectool_lib.get_battery_info.restype = ctypes.c_char_p

            cls.ectool_lib.set_auto_fan_control.restype = ctypes.c_char_p
        except Exception as e:
            print(f"Failed to load the ectool library: {e}")
            sys.exit(1)

    def test_get_tempsinfo_all(self):
        """Test that get_tempsinfo_all returns a valid string"""
        result = self.ectool_lib.get_tempsinfo_all()
        self.assertIsNotNone(result)
        decoded = result.decode('utf-8')
        self.assertIn("CPU", decoded)
        self.assertIn("Battery", decoded)
        print(f"get_tempsinfo_all result: {decoded}")

    def test_get_temp_sensor(self):
        """Test that get_temp_sensor returns valid temperature information"""
        result = self.ectool_lib.get_temp_sensor(b"0")
        self.assertIsInstance(result, ECResult)
        decoded = result.result_value.decode('utf-8')
        self.assertIn("Reading temperature...0", decoded)
        self.assertIn("(= ", decoded)
        self.assertIn(" C)", decoded)
        print(f"get_temp_sensor result: {decoded}")

    def test_get_temps_all(self):
        """Test that get_temps_all returns all temperature data"""
        result = self.ectool_lib.get_temps_all()
        self.assertIsNotNone(result)
        decoded = result.decode('utf-8')
        self.assertIn("Reading temperature", decoded)
        self.assertIn("(= ", decoded)
        print(f"get_temps_all result: {decoded}")

    def test_set_fan_duty(self):
        """Test that set_fan_duty accepts a speed value and returns confirmation"""
        # Test with different speed values
        for speed in [0, 50, 100]:
            result = self.ectool_lib.set_fan_duty(speed)
            self.assertIsInstance(result, ECResult)
            decoded = result.result_value.decode('utf-8')
            self.assertIn(f"Setting fan duty to {speed}%", decoded)
            print(f"set_fan_duty({speed}) result: {decoded}")

    def test_get_battery_info(self):
        """Test that get_battery_info returns battery information"""
        result = self.ectool_lib.get_battery_info()
        self.assertIsNotNone(result)
        decoded = result.decode('utf-8')
        self.assertIn("Battery", decoded)
        self.assertIn("Status", decoded)
        print(f"get_battery_info result: {decoded}")

    def test_set_auto_fan_control(self):
        """Test that set_auto_fan_control enables automatic fan control"""
        result = self.ectool_lib.set_auto_fan_control()
        self.assertIsNotNone(result)
        decoded = result.decode('utf-8')
        self.assertIn("automatic fan control", decoded)
        print(f"set_auto_fan_control result: {decoded}")

if __name__ == '__main__':
    print("Starting EC Library tests...")
    unittest.main()
