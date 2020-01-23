# Raspberry pi 3b setup for Parking management system

## Getting Started
1. [Requirements](https://github.com/robertkarajev/Mobility-Control-Center/tree/raspberry_startup/Setup_raspberry#installing-for-the-first-time)

2. [Installing for the first time](https://github.com/robertkarajev/Mobility-Control-Center/tree/raspberry_startup/Setup_raspberry#installing-for-the-first-time)

3. [Connecting with SSH](https://github.com/robertkarajev/Mobility-Control-Center/tree/raspberry_startup/Setup_raspberry#connecting-with-ssh)

4. [Connecting with UART](https://github.com/robertkarajev/Mobility-Control-Center/tree/raspberry_startup/Setup_raspberry#connecting-with-uart)

5. [Requirements for testing](https://github.com/robertkarajev/Mobility-Control-Center/tree/raspberry_startup/Setup_raspberry#testing)

### Requirements

* Raspberry pi 3b
* Any raspbian OS
* Any screen with HDMI 
* Mouse & Keyboard
* SD card
* Micro-usb cable

**Note after enabling SSH or UART, Raspberry pi can be controlled through SSH or UART and doesn't require Mouse and Keyboard**
* (Optional) SSH connection
* (Optional) UART cable **Using UART might cause random crashes for your PC

### Installing for the first time 

1. Install any Raspbian OS (https://www.raspberrypi.org/downloads/)
(**Desktop for newer users. For more advanced users use lite.**)
2. Flash Raspbian OS (https://www.balena.io/etcher/ or any other flash program)
3. Power the Raspberry pi with micro-usb and Boot up Raspberry Pi 3b with Raspbian OS
4. Log in Raspberry Pi with the default user and password (user:pi & pw:raspberry)
5. Enter raspi-config, select Interfacing Options or locate Interfacing Options (this might differ from each version of OS)
```
sudo raspi-config
```
6. Enable SSH or/and UART.
7. Reboot your Raspberry Pi
```
sudo reboot
```

### Connecting with SSH
*If you have the desktop version, skip to 5 for further instruction.*
*Step 1 to 4 can be use for WiFi connection*
1. Configure wpa_supplicant.conf
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
2. Change ssid and psk if there isn't anything written in the file, write this.

(_SSID is your network name_)
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
ssid="yourSSID"
psk="yourwifipassword"
}
```
3. CTRL-X, then Y to save and exit

4. reboot your Raspberry Pi 
5. To locate your Raspberry pi's IP use the following command and locate inet for acquire your IP 

```
ifconfig
```
6. Connect your through SSH by using cmd or PuTTY (https://www.putty.org/)

(*If you're using cmd, follow step 7 else step 8*)
7. ssh {user}@ip
For example:
```
ssh pi@192.123.1.255
```
8. Open PuTTY, select SSH and fill in the IP of your Raspberry Pi with port 22

### Connecting with UART

UART cable have 4 different pins, white (RX), green (TX), red (voltage), black (ground)
![alt text](https://docs.microsoft.com/en-us/windows/iot-core/media/pinmappingsrpi/rp2_pinout.png)
1. Connect RX -> TX (pin10), TX -> RX (pin8) 
2. Connect the usb to the PC 
3. Download/Install driver PL2303_Prolific_DriverInstaller_3.3.3.zip (For Window Users) and reboot PC
4. After rebooting search for Device manager in windows search bar.
5. Search for Ports (COM & LPT), Prolific USB-to-Serial Comm Port.
(* If you get this message: Pl2303hxa phased out since 2012. Please contact your supplier follow step 6-9*)
6. Right click on this message, update driver and select Browse my computer for driver software.
7. Choose the option to select available drivers from your computer.
8. In this option you'll get multiple certificate to choose from, choose the oldest certificate (from 200X).
9. Replug the usb, connect through PuTTY, select COM.
10. Write the COM where the Raspberry Pi is connected to and fill it at COM with 115200 as baud rate (speed field).
Example :

![alt text](https://i.stack.imgur.com/XgR6I.png)

## Testing
To check the correct setup, use wiegand_read_v3.py. This script will return id of the card in hexdecimal by executing run() in the module.

### Requirements for testing

**Hardware**

Either use one of these Wiegand readers or use another RFID scanner
* Wiegand 26bits 125kHz ( https://benselectronics.nl/wiegand-26-bit-rfid-long-distance-reader.-125khz/ )
* Wiegand 34bits 13.56MHz( https://benselectronics.nl/wiegand-34-bit-rfid-reader.-13.56-mhz/)

**RFID tags can only be used for the corresponding frequency**
* RFID tags 125kHz/13.56MHz
* Raspberry Pi 3b or newer (pin layout may differ with newer versions)
* Jumpercables
* Powersupply 9V - 12V

**Software**

* Python 3.X or newer version 
* Python packages
** Internet connection is needed to update the raspberry pi**
1. Update the raspberry pi's software and download python packages by executing the following commands
```
sudo apt-get update && sudo apt-get dist-upgrade
python install get-pip.py
sudo pip install sshtunnel RPi.GPIO mysql-connector paho-mqtt jsonlib datatime 
```
2. After installing, plug the scanner's D0 into GPIO17/pin11 and D1 into GPIO27/pin13 of the raspberry pi 3b, add the power supply and have a common ground with the raspberry pi 3b. See image below.

![alt text](https://drive.google.com/uc?export=view&id=1OS_gIt10I7cUcFQ2PT3f4dMx125Rtxks)

3. Start up the raspberry pi and copy the wiegand_read_v3.py file/create it by using the following commands
```
sudo nano wiegand_read_v3.py
```
4. To run this script use, scan the card and it will display hexadecimal values on cmd:
```
python3 wiegand_read_v3.py
```





















