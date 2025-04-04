#include <algorithm>
#include <cstdio>
#include <cstdlib>

#define MAX_RESULT_STRING_SIZE 100


// MOCK DATA
const char* const MOCK_SENSORS_LIST =
    "0 CPU: 35 C\n"
    "1 Battery: 30 C\n"
    "2 GPU: 40 C\n"
    "3 Ambient: 25 C\n"
    "4 Battery: 31 C\n"
    "5 PCH: 38 C\n";

struct sensors_list{
    char* name;
    int temperature;
};


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
    "  Voltage:  1234 mV\n"
    "  Current:  123 mA\n"
    "  Desired:  1234 mV\n"
    "  Capacity: 85%\n";

struct BATTERY_INFO{
    uint status;
    char* flags;
    uint voltage;
    uint current;
    uint desired;
    uint capacity;
};

struct ectool_result{
    char result_value[MAX_RESULT_STRING_SIZE];
};

