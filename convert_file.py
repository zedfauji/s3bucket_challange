import boto3
import botocore
import csv
from csv import DictReader
from pprint import pprint
from operator import itemgetter
from collections import Counter
import math
""" Declaring buckets Names """
BUCKET_OUT_NAME = 'devops-data-out-bucket-zed'
BUCKET_IN_NAME = 'devops-data-in-bucket-zed'
KEY_SITE_NAME = 'sites.csv'
KEY_IMAGES_NAME = 'images.csv'
dictResults = []
dictResults_key = []
final_result_dict = []

s3 = boto3.resource('s3')
def download_file_from_s3(filename):
    try:
        KEY = filename
        s3.Bucket(BUCKET_OUT_NAME).download_file(KEY,filename)
    except botocore.exceptions.ClientError as e:
        if e.response['ERROR']['Code'] == "404":
            print("File doesn't exist in s3")
        else:
            raise
def conver_csv_into_dict(filename):
    
    
    with open(filename) as File:

        if "images" in filename:
            csv_dict_reader = list(DictReader(File,fieldnames = ["ID", "IMAGE_NAME", "Latitude", "Longitude", "Date"]))
        elif "sites" in filename:
            csv_dict_reader = list(DictReader(File,fieldnames = ["ID", "SITE_NAME", "Latitude", "Longitude", "Date"]))
        return csv_dict_reader

download_file_from_s3(KEY_SITE_NAME)
download_file_from_s3(KEY_IMAGES_NAME)
dictResults_key = conver_csv_into_dict(KEY_SITE_NAME)
imagesRow = conver_csv_into_dict(KEY_IMAGES_NAME)
sitesRow = conver_csv_into_dict(KEY_SITE_NAME)
for each in imagesRow:
    print each

print " --------------END OF one FILE--------------------------------- "
for each in sitesRow:
    print each
