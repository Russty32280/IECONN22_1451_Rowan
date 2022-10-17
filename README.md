# IECONN22_1451_Rowan


# Change Log
## 16 OCT 22 2057:
Uploaded initial code. Removing references to TIM Code and removing massively commented out code.

## 16 OCT 22 2127:
Replaced instances of explicit broker names to a global variable mqttBroker. Allows for adaptability if changing the broker address.

NCAPS_ID Changed to be randomly generated integer.

NCAPS_Name changed to be Process appended by the newly generated ID.

Initial Subscription topics changed to include the automatically generated NCAPS_Name.
