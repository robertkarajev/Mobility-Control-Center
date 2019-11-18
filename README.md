# Raspberry pi 3b setup for Parking management system

## Getting Started

### Prerequisites

* Raspberry pi 3b
* Any raspbian OS
* Any screen with HDMI 
* Keyboard
* SD card

* Note after enabling SSH or UART, Raspberry pi can be controlled through SSH or UART*
* (Optional) SSH connection
* (Optional) UART cable

### Installing for the first time 

1. Install any Raspbian OS (https://www.raspberrypi.org/downloads/)
*Note install desktop for newer users. For advanced use lite.*
2. Flash Raspbian OS (https://www.balena.io/etcher/ or any other flash program) 
3. Boot up Raspberry Pi 3b with Raspbian OS
4. Log in Raspberry Pi with the default user and password (user:pi & pw:raspberry)
5. Enter raspi-config, select Interfacing Options or locate Interfacing Options (this might differ from each version of OS)
```
sudo raspi-config
```
6. Enable SSH and UART.
7. Reboot your Raspberry Pi
```
sudo reboot
```

### Connecting with SSH
*If you have the desktop version, skip to 5 for further instruction.
1. Configure wpa_supplicant.conf
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
2. Change ssid and psk if there isn't anything written in the file, write this.
_SSID is your network name_
```
cntrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
ssid="yourSSID"
psk="yourwifipassword"
}
```
3. CTRL-X, then Y to save and exit

4. reboot your Raspberry Pi 

----------------------------------------------------------

5. Check your Raspberry pi's IP and locate inet 

```
ifconfig
```

6. Connect your through SSH by using cmd or PuTTY (https://www.putty.org/)
_If you're using cmd, use this command_
.ssh {user}@ip
For example:
```
ssh pi@145.123.1.255
```

### Connecting with UART

1.

## (1)Raspberry setup serial connection
##### **Requirements**

-Raspberry 3\
-UART cable (white=RX, green= TX, red= voltage, black = ground)\


#####Setup
(1) Install driver for UART cable with CP210x_Universal_Windows_Driver.zip
(2) 


Work in progress

