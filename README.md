# Intelligent Mobility
A minor at University of Applied Science Rotterdam for 4th year students.

# Smart Urban Parking
Is an autonomous parking system thats uses Rfid-tags to navigate inside a parking lot that automatically registers arriving cars to random generated parking spaces.

# Dependencies
```
python 3.X+
all the files included
```

# on client imports:
```
sshtunnel
RPi.GPIO
paho-mqtt
jsonlib
random
string
json
time
os
datetime
threading
```

# on server imports:
```
mysql-connector
paho-mqtt
threading
json
time
pygame
```

# other dependancies
```
a database which is running and conform with how it is described further in the document
```

# The database
![database.png](https://drive.google.com/uc?export=view&id=1Aj3LvTur35IWqjrIl2ch4h0lmWE634xm)

# general working
![flowchart](https://drive.google.com/uc?export=view&id=10ah_xs_YguLb7vbNeSg0DeprGHoH5x0X)
<!--
The rfid scanner attached to the raspberry of the client reads a tag. The car makes a random 4 string long ID and tries to connect to the server through mqtt the server checks if the ID was already known and sends the result back. If the client gets the result it wanted it will ask for a path to the server. the server checks
-->
