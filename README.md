# IECONN22_1451_Rowan

In order to run the NCAP server:
  Install the latest version of Python 3

  Download NCAPServer1451.py from the repository

  Install the paho MQTT python client with "pip3 install paho-mqtt"

  Using IDLE, open NCAPServer1451.py

  Run the python file

# List of working functions
## Discovery Services
- [ ] 10.1.1 NCAP Announcement
- [ ] 10.1.2 NCAP TIM Announcement
- [ ] 10.1.3 NCAP TIM XDCR Announcement
- [x] 10.1.4 NCAP Discovery
- [x] 10.1.5 NCAP TIM Discovery
- [x] 10.1.6 NCAP TIM XDCR Discovery


## Transducer Access Services
- [ ] Synchronous Read XDCR Sample Data From a Channel of a TIM
- [ ] Synchronous Read XDCR Block Data From a Channel of a TIM
- [ ] Synchronous Read XDCR Sample Data From Multiple Channels of a TIM
- [ ] Synchronous Read XDCR Block Data From Multiple Channels of a TIM
- [ ] Synchronous Read XDCR Sample Data From Multiple Channels of Multiple TIMs
- [ ] Synchronous Read XDCR Block Data From Multiple Channels of Multiple TIMs
- [ ] Synchronous Write XDCR Sample Data From a Channel of a TIM
- [ ] Synchronous Write XDCR Block Data From a Channel of a TIM
- [ ] Synchronous Write XDCR Sample Data From Multiple Channels of a TIM
- [ ] Synchronous Write XDCR Block Data From Multiple Channels of a TIM
- [ ] Synchronous Write XDCR Sample Data From Multiple Channels of Multiple TIMs
- [ ] Synchronous Write XDCR Block Data From Multiple Channels of Multiple TIMs
- [ ] Asynchronous Read XDCR Sample Data From a Channel of a TIM
- [ ] Callback Asynchronous Read XDCR Sample Data From a Channel of a TIM
- [ ] Asynchronous Read XDCR Block Data From a Channel of a TIM
- [ ] Callback Asynchronous Read XDCR Block Data From a Channel of a TIM
- [ ] Asynchronous Read XDCR Sample Data From Multiple Channels of a TIM
- [ ] Callback Asynchronous Read XDCR Sample Data From Multiple Channels of a TIM
- [ ] Asynchronous Read XDCR Block Data From Multiple Channels of a TIM
- [ ] Callback Asynchronous Read XDCR Block Data From Multiple Channels of a TIM
- [ ] Asynchronous Read XDCR Sample Data From Multiple Channels of Multiple TIMs
- [ ] Callback Asynchronous Read XDCR Sample Data From Multiple Channels of Multiple TIMs
- [ ] Asynchronous Read XDCR Block Data From Multiple Channels of Multiple TIMs
- [ ] Callback Asynchronous Read XDCR Block Data From Multiple Channels of Multiple TIMs
- [ ] Asynchronous Write XDCR Sample Data From a Channel of a TIM
- [ ] Callback Asynchronous Write XDCR Sample Data From a Channel of a TIM
- [ ] Asynchronous Write XDCR Block Data From a Channel of a TIM
- [ ] Callback Asynchronous Write XDCR Block Data From a Channel of a TIM
- [ ] Asynchronous Write XDCR Sample Data From Multiple Channels of a TIM
- [ ] Callback Asynchronous Write XDCR Sample Data From Multiple Channels of a TIM
- [ ] Asynchronous Write XDCR Block Data From Multiple Channels of a TIM
- [ ] Callback Asynchronous Write XDCR Block Data From Multiple Channels of a TIM
- [ ] Asynchronous Write XDCR Sample Data From Multiple Channels of Multiple TIMs
- [ ] Callback Asynchronous Write XDCR Sample Data From Multiple Channels of Multiple TIMs
- [ ] Asynchronous Write XDCR Block Data From Multiple Channels of Multiple TIMs
- [ ] Callback Asynchronous Write XDCR Block Data From Multiple Channels of Multiple TIMs

## TEDS Access Services
- [ ] 10.3.1 Query TEDS
- [ ] Read TEDS
- [ ] Write TEDS
- [ ] Update TEDS

## Event Notification Services
- [ ] Subscribe New TIM From NCAP
- [ ] Notify New TIM to APP
- [ ] Subscribe a TIM Departure from NCAP
- [ ] Notify a Departed TIM to APP
- [ ] Subscribe XDCR Alert from One Channel of One TIM
- [ ] Notify XDCR Alert from One Channel of One TIM
- [ ] Subscribe XDCR Alert from Multiple Channels of One TIM
- [ ] Notify XDCR Alert from Multiple Channels of One TIM
- [ ] Subscribe XDCR Alerts from Multiple Channels of Multiple TIMs
- [ ] Notify XDCR Alerts from Multiple Channels of Multiple TIMs
- [ ] Setup A XDCR Alert Threshold for One Channel of One TIM
- [ ] Setup XDCR Alert Thresholds for Multiple Channels of a TIM
- [ ] Setup XDCR Alert Thresholds for Multiple Channels of Multiple TIMs


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


## 17 OCT 22 1245:
Client will automatically generate a "random" APPLID to prevent simultaneous users from existing on the network. This was done by replacing the field for user input and now it is randomly generated.

This now also requires the Client to be subscribed to the correct topics with the newly generated ID.

TODO: TIM Discover in the client example needs to be a field you can enter and control separately since we do not know how many TIMs will be connected.

PROBLEM!!!
There is no current way in the TIM and XDCR Discover to know who to respond to. The current temporary fix is to remember the APPID from the initial discovery request. This WILL NOT Work with multiple devices.

Sugessted Fix to 1451.0 10.1.6
NetSvcType netSvcType//(1)
NetSvcIdnetSvcId// (5)
MsgType msgType // (1)
UInt16 msgLength
UUID appID
UUID ncapId
TimeDurationtimeout

## 17 OCT 22 1515:
