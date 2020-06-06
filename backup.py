#!/media/pi/data/SM/smarthome/env/bin/python3

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
	list = []
	for entry in cfg.data['folder']:
		if not ("recursive" in entry):
			entry["recursive"] = False
		list = list + helper.scandir(basepath, entry['path'], entry['recursive'])
	awsSession = aws.c_aws(cfg.data["aws"]["key"])
	for file in list:
		if tmp.data['last']-cfg.data['delta']<int(os.path.getmtime(file)):
			key = file.replace(basepath, cfg.data['s3folder'])
			awsSession.s3.Bucket(cfg.data["s3bucket"]).upload_file(file, key)
	tmp.data['last'] = int(time.time())
	tmp.save()

if __name__ == '__main__':
	main()
