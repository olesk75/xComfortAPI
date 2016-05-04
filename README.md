# xComfortAPI
### Python API for Eaton xComfort Smart Home Controller (SHC) 
xComfortAPI provides an API to the Eatcon xComfort Smart Home Controller (SHC)
This allows for reading and setting values in the SHC, which in plain language
allows you to both check and set all values the SHC knows, which gives you
control of all your lights/heaters/blinds/alarms/whatever you have installed.

This API does *not* provide any means of directly controlling actuators via
radio signal using Eaton's proprietary protocol. Instead it simulates the
Android/iOS app that is used to control the complete installation through a
SHC, as the SHC can be controlled through these apps, as well as by logging
on to the web page of the SHC.

######Example usage (get and print all zones the SHC knows):

```python

    from xComfortAPI import xComfortAPI
  
    my_house = xComfortAPI(url, username, password, verbose=verbose)  # We get a SHC instance, which contains the session ID
  	zones = my_house.get_zone_devices()
	my_house.show_zones(zones)
```

####Current status:
The xComfort API is active development. It currently reads values fine, but
I've run into a snag when trying to write them back. The API also needs more
functions for standard operations, especially for more easily manipulating
single devices. The good news that the basic functionality works well and is
reasonably robust, so hopefully soon... 

###FAQ
####TODO