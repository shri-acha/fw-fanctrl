#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cstring>

struct ECResult {
    char result_value[100];
};

const char* const MOCK_SENSORS_LIST =
    "0 CPU: 35 C\n"
    "1 Battery: 30 C\n"
    "2 GPU: 40 C\n"
    "3 Ambient: 25 C\n"
    "4 Battery: 31 C\n"
    "5 PCH: 38 C\n";

const char* const MOCK_ALL_TEMPS =
    "Reading temperature...0 = 35 (= 35 C)\n"
    "Reading temperature...1 = 30 (= 30 C)\n"
    "Reading temperature...2 = 40 (= 40 C)\n"
    "Reading temperature...3 = 25 (= 25 C)\n"
    "Reading temperature...4 = 31 (= 31 C)\n"
    "Reading temperature...5 = 38 (= 38 C)\n";

const char* const MOCK_BATTERY_INFO =
    "Battery 0:\n"
    "  Status:   0x0021\n"
    "  Flags:    AC_PRESENT BATT_PRESENT CHARGING\n"
    "  Voltage:  12356 mV\n"
    "  Current:  123 mA\n"
    "  Desired:  1234 mV\n"
    "  Capacity: 85%\n";

extern "C" {
    const char* get_tempsinfo_all() {
        return MOCK_SENSORS_LIST;
    }

    ECResult get_temp_sensor(const char* sensor_id) {
        ECResult result;
        int temperature = 30 + (rand() % 21);
        snprintf(result.result_value, sizeof(result.result_value),
                "Reading temperature...%s = %d (= %d C)\n",
                sensor_id, temperature, temperature);
        printf("%s\n", result.result_value); // Added missing semicolon
        return result;
    }

    const char* get_temps_all() {
        return MOCK_ALL_TEMPS;
    }

    ECResult set_fan_duty(int speed) {
        ECResult result;
        int clamped_speed = std::min(100, std::max(0, speed));
        snprintf(result.result_value, sizeof(result.result_value),
                "Setting fan duty to %d%%\n", clamped_speed);
        return result;
    }

    const char* get_battery_info() {
        return MOCK_BATTERY_INFO;
    }

    const char* set_auto_fan_control() {
        return "Enabling automatic fan control\n";
    }
}
