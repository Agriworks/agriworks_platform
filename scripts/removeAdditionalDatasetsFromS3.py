## This script is to remove additional datasets from S3 that don't exist in Mongo

import boto3
import botocore
from pymongo import MongoClient
from pprint import pprint
from bson.objectid import ObjectId
import yaml

## NOTE: CREDS FILE NOT AVAILABLE ON PROD
creds = yaml.safe_load(open("../creds.yaml", "r"))
dbHostUri = "mongodb+srv://" + creds["DB_USER"] + ":" + creds["DB_PASSWORD"] + "@cluster0-ollas.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
db = MongoClient(dbHostUri).test

serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)

s3 = boto3.resource('s3')
bucketName = "agriworks-user-datasets"
bucket = s3.Bucket(bucketName)

s3Length = sum(1 for i in bucket.objects.all())
print('s3 Size =',s3Length)

for key in bucket.objects.all():
    if not db.dataset.find_one({'_id': ObjectId(key.key.split('.')[0])}):
        print(key.key)
        obj = s3.Object(bucketName, key.key)
        obj.delete()

print('________DELETED__________')

for key in bucket.objects.all():
    if not db.dataset.find_one({'_id': ObjectId(key.key.split('.')[0])}):
        print(key.key) ## Should not print any keys here, if the deletion was successful
