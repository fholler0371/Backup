import boto3

class c_aws:
	def __init__(self, credentials):
		self.session = boto3.Session(aws_access_key_id=credentials["key"], aws_secret_access_key=credentials["secret"], region_name=credentials["region"])
		self.s3 = self.session.resource("s3")
