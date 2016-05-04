# xComfortAPI
### Python API for Eaton xComfort Smart Home Controller (SHC)
Eaton xComfort is a system for home automation that is dominant in several 
countries in Europe. Unfortunately, Eaton does not share API access or 
documentation on how third parties can integrate with their systems. It would
appear they are solidly stuck on the "pre-internet of things" era, and little
seems to be changing. Their hardware, however, is really good, so all that was
missing was an API.

xComfortAPI is a Python API to the Eaton xComfort Smart Home Controller (SHC)
This allows for reading and setting values in the SHC, which in plain language
allows you to both check and set all values the SHC knows, which gives you
control of all your lights/heaters/blinds/alarms/whatever you have installed.

This API does *not* provide any means of directly controlling actuators via
radio signal using Eaton's proprietary protocol. Instead it simulates the
Android/iOS app that is used to control the complete installation through a
SHC, as the SHC can be controlled through these apps, as well as by logging
on to the web page of the SHC.

The API is written in Python3, but should with small tweaks work with Python2.

######Example usage (get and print all zones the SHC knows):

```python

    from xComfortAPI import xComfortAPI
  
    my_house = xComfortAPI(url, username, password, verbose=True)
  	zones = my_house.get_zone_devices()
	my_house.show_zones(zones)
	
	# We get the zone ("hz_1") and device id ("xCo:5355820_u0") above
	my_house.switch('hz_1', 'xCo:5355820_u0', 'off')  # Switches off living room lights
```

####Current status:
The xComfort API is active development. The API needs more functions for 
standard operations, especially for more easily manipulating single devices. 
The good news that the basic functionality works well and is
reasonably robust, so hopefully soon... 

###FAQ
####TODO

###Disclaimer
I AM IN NO WAS ASSOCIATED WITH EATON OR XCOMFORT AND TAKE ABSOLUTELY NO RESPONSIBILITY
FOR THE RESULTS OF USING THIS API. IF YOUR HOUSE BURNS DOWN AND/OR YOUR CAT GETS 
ELECTROCUTED, I ACCEPT NO RESPONSIBILITY WHATSOEVER. USE AT OWN RISK! 

THIS SOFTWARE AND DOCUMENTATION IS PROVIDED "AS IS," AND COPYRIGHT HOLDERS MAKE NO
REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO, 
WARRANTIES OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE
OF THE SOFTWARE OR DOCUMENTATION WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS,
TRADEMARKS OR OTHER RIGHTS.

COPYRIGHT HOLDERS WILL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL
DAMAGES ARISING OUT OF ANY USE OF THE SOFTWARE OR DOCUMENTATION.