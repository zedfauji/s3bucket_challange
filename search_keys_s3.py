import boto3

s3 = boto3.client('s3')
s3.list_objects_v2(Bucket='devops-data-out-bucket')

def get_s3_keys(bucket):
    keys = []
    resp = s3.list_objects_v2(Bucket='devops-data-out-bucket')
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys