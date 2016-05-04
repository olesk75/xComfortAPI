from configparser import ConfigParser
from xComfortAPI import xComfortAPI

# Using configparser to load username/password and URL from INI-file (slightly overkill for this script, but works nicely)
ini_file = 'xcomfort.ini'  # Copy the example ini-file to xcomfort.ini and substitute your information
config_parser = ConfigParser()
config_parser.read(ini_file)

try:
	username = config_parser.get('API', 'username')
	password = config_parser.get('API', 'password')
	url = config_parser.get('API', 'url')
	verbose = config_parser.getboolean('API', 'verbose', fallback=False)
except Exception as err:
	print('Error in ini file' + ini_file + ': ' + str(err))
	print('Please see xcomfort.ini.example for syntax. Aborting...')
	exit(1)

# We now got URL, username, password and verbosity from INI-file, so we create an instance, my_house(), of the xComfortAPI class
my_house = xComfortAPI(url, username, password, verbose=verbose)  # We get a SHC instance, which contains the session ID

"""
Here we poll all zones and devices. Still, there is a LOT that can be done through the JSON PRC requests.
To see a complete list of available methods, use the 'system.listMethods' method (over 500 methods defined)
"""

# Getting firmware data
sysinfo = my_house.query('Settings/getSystemInfo')
my_house.show_diagnostics()

print('Uptime:' + sysinfo['uptime'])
print('Firmware version:' + sysinfo['shc_version'])
print('OS version:' + sysinfo['os_version'])

zones = my_house.get_zone_devices()
my_house.print_zones(zones)

# Example of switching a light _off_
# The light is in zone 'hz_1' with id 'xCo:5355820_u0' (see output from my_house.print_zones(zones) to get zone and ID)
my_house.switch('hz_1', 'xCo:5355820_u0', 'off')

exit(0)
