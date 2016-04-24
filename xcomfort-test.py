from configparser import ConfigParser
from xComfortAPI import xComfortAPI

ini_file = 'xcomfort.ini'
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

my_house = xComfortAPI(url, username, password, verbose=verbose)  # We get a SHC instance, which contains the session ID

"""
Here we poll all zones and devices. Still, there is a LOT that can be done through the JSON PRC requests.
To see a complete list of available methods, use the 'system.listMethods' method (over 500 methods defined)
"""

# Getting firmware data
sysinfo = my_house.query('Settings/getSystemInfo')

print('Uptime:' + sysinfo['uptime'])
print('Firmware version:' + sysinfo['shc_version'])
print('OS version:' + sysinfo['os_version'])

# diagnostics = shc_query(session_ID, url, 'Diagnostics/getAllSystemStates')
# TODO: fill out
# Check for pending updates: Settings/getSoftwareStatus and RfFirmware/getFirmwareInfo
# SHC device info: Settings/getRemoteInfo
# System status "Diagnostics/getAllSystemStates"

zones = my_house.get_zone_devices()
my_house.show_zones(zones)

exit(0)
