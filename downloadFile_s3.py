import boto3
import botocore
BUCKET_NAME = 'devops-data-out-bucket'
s3 = boto3.resource('s3')
my_bucket = s3.Bucket(BUCKET_NAME)
for file in my_bucket.objects.all():
    print file.key

files_in_s3 = my_bucket.objects.all()

print files_in_s3