# Raspberry pi 3b setup for Parking management system

## Getting Started

### Prerequisites

* Raspberry pi 3b
* Any raspbian OS
* Any screen with HDMI 
* Keyboard
* SD card
* Micro-usb cable

* Note after enabling SSH or UART, Raspberry pi can be controlled through SSH or UART*
* (Optional) SSH connection
* (Optional) UART cable

### Installing for the first time 

1. Install any Raspbian OS (https://www.raspberrypi.org/downloads/) \
(*Note install desktop for newer users. For more advanced users use lite.*)\
2. Flash Raspbian OS (https://www.balena.io/etcher/ or any other flash program) 
3a. Power the Raspberry pi with micro-usb
3b. Boot up Raspberry Pi 3b with Raspbian OS
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

1. Configure wpa_supplicant.conf
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
2. Change ssid and psk if there isn't anything written in the file, write this.\
(_SSID is your network name_)\
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
5. Check your Raspberry pi's IP and locate inet 

```
ifconfig
```

6. Connect your through SSH by using cmd or PuTTY (https://www.putty.org/) \
(_If you're using cmd, use this command_) \
7a. ssh {user}@ip\
For example:
```
ssh pi@192.123.1.255
```
7b. Open PuTTY, select SSH and fill in the IP of your Raspberry Pi with port 22

### Connecting with UART

UART cable have 4 different pins, white (RX), green (TX), red (voltage), black (ground) \
![alt text](https://docs.microsoft.com/en-us/windows/iot-core/media/pinmappingsrpi/rp2_pinout.png) \
1. Connect RX -> TX (pin10), TX -> RX (pin8) 
2. Plug in the usb
3. Download/Install driver PL2303_Prolific_DriverInstaller_3.3.3.zip (For Window Users) and reboot PC
4. After rebooting search for Device manager in windows search bar.
5. Search for Ports (COM & LPT), Prolific USB-to-Serial Comm Port.\
_ If you get this message: Pl2303hxa phased out since 2012. Please contact your supplier follow step 5 to_
6. Right click on this message, update driver and select Browse my computer for driver software.
7. Choose the option to select available drivers from your computer.
8. In this option you'll get multiple certificate to choose from, choose the oldest certificate (from 200X).
9. Replug the usb, connect through PuTTY, select COM.
10. Write the COM where the Raspberry Pi is connected to and fill it at COM with 115200 as baud rate.\
Example :
![alt text] (https://i.stack.imgur.com/XgR6I.png)


Work in progress

