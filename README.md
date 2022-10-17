# IECONN22_1451_Rowan


# Change Log
## 16 OCT 22 2057:
Uploaded initial code. Removing references to TIM Code and removing massively commented out code.

## 16 OCT 22 2127:
Replaced instances of explicit broker names to a global variable mqttBroker. Allows for adaptability if changing the broker address.

NCAPS_ID Changed to be randomly generated integer.

NCAPS_Name changed to be Process appended by the newly generated ID.

Initial Subscription topics changed to include the automatically generated NCAPS_Name.

## 16 OCT 22 2227:
Changed IP Address to pull local IP address of the local machine.

To support multiple clients connecting, we need to store the current clients and their information inside of either a dict or tuple, and access them based off what needs to be done. This will need to be accessed based on the client requesting them. For the initial change, we will not verify that this is a verified user, rather just respond as needed.

The Application ID will be remembered through the Discover Services initially, however, it should be noted that this is the purpose of the Join Requests. We will pull the APPL ID from the discovery request.

Current changes are in Thread132, while it does not publish to the correct new topic, it will respond back to the original topic. It also prints to the new topic to the console.

TODO: Ensure the correct topic is saved.

## 17 OCT 22 1145:
The Website needs to be updated to allow for a different APPL ID to be sent. This is currently hardcoded.

Website JS updated to send the NCAP Client ID as entered by the user, not just hardcoded. Moved the multiple publishes to the JS from the HTML.
