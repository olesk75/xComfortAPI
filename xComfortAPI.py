"""
xComfortAPI provides an API to the Eatcon xComfort Smart Home Controller (SHC)
This allows for reading and setting values in the SHC, which in plain language
allows you to both check and set all values the SHC knows, which gives you
control of all your lights/heaters/blinds/alarms/whatever you have installed.

This API does *not* provide any means of directly controlling actuators via
radio signal using Eaton's proprietary protocol. Instead it simulates the
Android/iOS app that is used to control the complete installation through a
SHC, as the SHC can be controlled through these apps, as well as by logging
on to the web page of the SHC.

IMPORTANT: For the API to be able to control the SHC, it must be available
on the network (duh!). This means that if you want to connect to the SHC when
you are not at the same local network as the SHC (from outside your house),
the SHC must be reachable through your router. Simply put: if you are able to
log on to the SHC web UI from where you run your script, you'll be fine. If
you can't you need to configure your firewall to allow access to the SHC.
Explaining how to do this is outside the scope of this little text - Google
is your friend!

"""

import json
import requests


class xComfortAPI:
	def __init__(self, url, username, password, verbose=False):
		"""
		Class to access a Smart Home Controller (SHC) via its web API.
		:param url: the URL of the SHC, for example: http://my_home.dyndns.org:8080
		:param username: normally "admin" - the user you normally use to log on to the web interface of the SHC
		:param password: the password for the user
		"""
		self.url = url
		self.username = username
		self.password = password
		self.verbose = verbose
		self.session_ID = ''
		self._get_session_id()
		if self.verbose:
			print('Got session id "', self.session_ID, '"', sep='')

	def _get_session_id(self):
		"""
		Logs in to the SHC and gives us a session ID cookie that is authenticated and we reuse to make our JSON RPC calls
		:return: session ID cookie(string)
		"""
		headers = {'User-Agent': 'Mozilla/5.0'}

		session = requests.Session()
		try:
			session.get(self.url)
		except Exception as err:
			if 'failed to respond' in str(err):
				print('ERROR:', self.url, 'did not respond to our connection attempt. Please check your URL address\nAborting...')
				exit(1)
			else:
				print('ERROR:', err, '\nAborting...')
				exit(1)

		response = session.post(self.url, headers=headers, auth=(self.username, self.password))
		if response.status_code != 200:
			if response.status_code == 401:
				print('Invalid username/password\nAborting...')
				exit(1)
			else:
				print('Server responded with status code', str(response.status_code), '\nAborting...')
		else:
			self.session_ID = requests.utils.dict_from_cookiejar(session.cookies)['JSESSIONID']

	def query(self, method, params=['', '']):
		"""
		Sends query to SHC's JSON RPC interface
		:param method: the JSON RPC method
		:param params: parameters for the JSON RPC method (defaults to list of two empty string)
		:param debug: print debug information
		:return: dict of response from SHC
		"""
		json_url = self.url + '/remote/json-rpc'
		data = {
			"jsonrpc": "2.0",
			'method': method,  # Settings/getSystemInfo
			'params': params,
			'id': 1
		}
		headers = {
			'Accept': 'application/json',
			'Cookie': 'JSESSIONID=' + self.session_ID,
			'Accept-Encoding': 'gzip, deflate',
			'Content-Type': 'application/json',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
		}

		try:
			response = requests.post(json_url, data=json.dumps(data), headers=headers).json()
		except ValueError as err:
			if err == 'Expecting value: line 1 column 1 (char 0)':
				print('The SHC gave an invalid response. Most likely, this is due to an incorrect URL in your INI-file')
				print('Please verify that your URL is of the format "http://IP:port", or just "http://IP" if you use default port 80')
			exit(1)

		if 'result' not in response:
			response['result'] = [{}]  # In case we have a zone without devices for example

		if self.verbose:
			print('Query returned', len(response['result']), 'datapoints')

		return response['result']

	def get_zone_devices(self):
		"""
		Getting all zones and functions
		:return: list of zones with all devices in each zone
		"""
		zone_list = self.query('HFM/getZones')  # Returns a list of dicts in this case
		for zone in zone_list:
			zone.pop('virtual', None)
			zone.pop('mainIndoorTemperature', None)
			zone['devices'] = self.query('StatusControlFunction/getDevices', params=[zone['zoneId'], ''])
		return zone_list

	def show_zones(self, zones):
		"""
		Prints all zones and their devices in human readable form
		:param zones:
		"""
		for zone in zones:
			print(zone['zoneName'], '(' + zone['zoneId'] + ')')
			for device in zone['devices']:
				if 'name' in device:
					print('\t{:<55}{:>10}{}'.format(device['name'], device['value'], device['unit']))

