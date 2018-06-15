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
        """
        csv_dict_reader = csv.DictReader(File)
        csv_dict_reader = list(DictReader(File,))"""
        if "images" in filename:
            """csv_dict_reader.fieldnames = ["ID", "IMAGE_NAME", "Latitude", "Longitude", "Date"]"""
            csv_dict_reader = list(DictReader(File,fieldnames = ["ID", "IMAGE_NAME", "Latitude", "Longitude", "Date"]))
        elif "sites" in filename:
            """csv_dict_reader.fieldnames = ["ID", "SITE_NAME", "Latitude", "Longitude"]"""
            csv_dict_reader = list(DictReader(File,fieldnames = ["ID", "SITE_NAME", "Latitude", "Longitude", "Date"]))
        for row in csv_dict_reader:
            dictResults.append(row)
        """print dictResults[0:1]"""
        return dictResults

"""def conver_csv_into_dict(filename):
    
    with open(filename) as File:
        dictReader = csv.DictReader(File)
        for row in dictReader:
            dictResults.append(row)
        print dictResults[0:1]"""
def haversine(lon1, lat1, lon2, lat2):
    from math import radians, cos, sin, asin, sqrt
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat /2 ) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers.
    # return the final calculation
    return c * r if c * r <= 5 else None
def getDistance (TARGET_Longitude, TARGET_Latitude, lng, lat):
    lat1 = TARGET_Latitude
    lon1 = TARGET_Longitude
    lat2 = lat
    lon2 = lng
    radius = 6371
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d if d <= 2 else None

download_file_from_s3(KEY_SITE_NAME)
download_file_from_s3(KEY_IMAGES_NAME)
dictResults_key = conver_csv_into_dict(KEY_SITE_NAME)
with open (KEY_IMAGES_NAME) as File:
    datarows= list(DictReader(File,fieldnames = ["ID", "IMAGE_NAME", "Latitude", "Longitude", "Date"]))
number_of_id=0
for res in dictResults_key:
    if 'ID' in res:
        number_of_id +=1

TARGET_Latitude = 0.0
TARGET_Longitude = 0.0
def export_dict_list_to_csv(data, filename):
    with open(filename, 'wb') as f:
        # Assuming that all dictionaries in the list have the same keys.
        headers = sorted([k for k, v in data[1].items()])
        csv_data = [headers]

        for d in data:
            csv_data.append([d[h] for h in headers])

        writer = csv.writer(f)
        writer.writerows(csv_data)
def haver_foo(item):
    lng = float(item['Longitude'])
    lat = float(item['Latitude'])

    return getDistance(TARGET_Longitude, TARGET_Latitude, lng, lat)
near_distance = 5
nearest_sites = sorted(datarows, key=haver_foo)

for i in range(number_of_id):
    print ("Checking for Site ", dictResults_key[i]['SITE_NAME'])
    TARGET_Latitude=float(dictResults_key[i]['Latitude'])
    print TARGET_Latitude
    TARGET_Longitude=float(dictResults_key[i]['Longitude'])
    print TARGET_Longitude
    for each in datarows:
        src_lng = float(each['Longitude'])
        src_lat = float(each['Latitude'])
        distance = haversine(TARGET_Longitude,TARGET_Latitude, src_lng, src_lat)
        if distance >= 0:
            print (distance , "KM Nearby Image Found", each['IMAGE_NAME'],each['ID'])
            final_result_dict.append(each)
    filename = "girish_" + dictResults_key[i]['SITE_NAME'] + "_challenge.csv"
    export_dict_list_to_csv(final_result_dict,filename)



