#!/media/pi/data/SM/smarthome/env/bin/python3

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Version 1.0
"""

import __main__ as main_lib
import os, sys, time

basepath = os.path.dirname(os.path.abspath(main_lib.__file__))
sys.path.append(basepath+"/lib")

import config
import helper
import aws

def main():
	cfg = config.c_config()
	cfg.load(basepath+"/cfg/"+os.path.splitext(os.path.basename(main_lib.__file__))[0]+".json")
	tmp = config.c_config()
	tmp.data['last'] = 0
	tmp.load(basepath+"/tmp/"+os.path.splitext(os.path.basename(main_lib.__file__))[0]+".json")
	for packet in cfg.data["packets"]:
		list = []
		for entry in packet['folder']:
			if not ("recursive" in entry):
				entry["recursive"] = False
			list = list + helper.scandir(basepath, entry['path'], entry['recursive'])
			awsSession = aws.c_aws(cfg.data["aws"]["key"])
		for file in list:
			if tmp.data['last']-packet['delta']<int(os.path.getmtime(file)):
				key = file.replace(basepath, packet['s3folder'])
				awsSession.s3.Bucket(packet["s3bucket"]).upload_file(file, key)
	tmp.data['last'] = int(time.time())
	tmp.save()

if __name__ == '__main__':
	main()
