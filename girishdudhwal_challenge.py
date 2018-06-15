__author__ = "Girish Dudhwal"
__credits__ = ["stackoverflow, Google, and obviously haversine equation"]
__version__ = "1.0.1"
__maintainer__ = "Girish Dudhwal"
__email__ = "girishdudhwal@gmail.com"
__status__ = "Production Ready"
import boto3
import botocore
import csv
from csv import DictReader
from operator import itemgetter
from collections import Counter
import math
from datetime import datetime
import sys
""" Declaring Globals """
BUCKET_OUT_NAME = 'devops-data-out-bucket'
BUCKET_IN_NAME = 'devops-data-in-bucket'
KEY_SITE_NAME = 'sites.csv'
KEY_IMAGES_NAME = 'images.csv'
number_of_id=0
TARGET_Latitude = 0.0
TARGET_Longitude = 0.0
near_distance = 5
site_contents = []
final_result_dict = []

""" Logic Behind this program as taking range of distance to be 5 KM,
    if nearby distance is less or equal to 5 KM, we are considering them as near by """


""" Connecting to S3 Bucket as resource using Boto3 """
s3 = boto3.resource('s3')


def download_file_from_s3(filename):
    """
    This Function will download the file from S3 and check if the file exists
    """
    try:
        KEY = filename
        s3.Bucket(BUCKET_OUT_NAME).download_file(KEY,filename)
    except botocore.exceptions.ClientError as e:
        if e.response['ERROR']['Code'] == "404":
            print("File doesn't exist in s3")
        else:
            raise

def uploadTos3(filename,s3_bucket_name):
    """This function will be called to upload file to s3 bucket """
    s3_path = 'girishdudhwal/' + filename
    try:
        KEY = filename
        s3.Bucket(s3_bucket_name).upload_file(KEY,s3_path,ExtraArgs={'ACL':'public-read-write'})
    except botocore.exceptions.ClientError as e:
        if e.response['ERROR']['Code'] == "401":
            print ("Dont have permission to upload")
            pass
        else:
            raise

def conver_csv_into_dict(filename):
    """ 
    This function will convert the CSV file as  list of dictionaries along with Headers 
    """
    with open(filename) as File:

        if "images" in filename:
            csv_dict_reader = list(DictReader(File,fieldnames = ["ID", "IMAGE_NAME", "Latitude", "Longitude", "Date"]))
        elif "sites" in filename:
            csv_dict_reader = list(DictReader(File,fieldnames = ["ID", "SITE_NAME", "Latitude", "Longitude", "Date"]))
        return csv_dict_reader

def getNumberofIds (item):
    """ This method return how many ID's are there in File sites.csv """
    number_of_id = 0
    for each in item:
        if 'ID' in each:
            number_of_id +=1
    return number_of_id

def export_dict_list_to_csv(data, filename):
    """ This function will Write the list dict to CSV File """
    with open(filename, 'wb') as f:
        # Assuming that all dictionaries in the list have the same keys.
        headers = sorted([k for k, v in data[1].items()])
        csv_data = [headers]

        for d in data:
            csv_data.append([d[h] for h in headers])

        writer = csv.writer(f)
        writer.writerows(csv_data)
        print "Files Written"
        print "Uploading to s3"
        uploadTos3(filename,BUCKET_IN_NAME)

def checkDates(firstdate,seconddate):
    """ This function will check the dates and compare if the images belongs to same date"""
    firstdate = firstdate
    seconddate = seconddate
    firstdate = datetime.strptime(firstdate,'%Y-%m-%d')
    seconddate = datetime.strptime(seconddate,'%Y-%m-%d')
  
    if firstdate == seconddate:
        return True
    else:
        return False

def haversine(lon1, lat1, lon2, lat2):
    """ This function was copied through searching python haversin from stack overflow """
    """ This function calculate the distance between 2 sets of long and lat """
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
    """if distance calculated is equal or less than 5 then we will return , else None"""
    return c * r if c * r <= 5 else None


download_file_from_s3(KEY_SITE_NAME)
download_file_from_s3(KEY_IMAGES_NAME)
site_contents = conver_csv_into_dict(KEY_SITE_NAME)

""" We count how many id's are there in Sites.csv """
number_of_id = getNumberofIds(site_contents)

image_content = conver_csv_into_dict(KEY_IMAGES_NAME)
for i in range(number_of_id):
    print ("Checking for Site ", site_contents[i]['SITE_NAME'])

    """ Taking Lat and long from sites.csv as Target lat and long for calculations """
    TARGET_Latitude=float(site_contents[i]['Latitude'])
    TARGET_Longitude=float(site_contents[i]['Longitude'])

    for each in image_content:
        src_lng = float(each['Longitude'])
        src_lat = float(each['Latitude'])
        distance = haversine(TARGET_Longitude,TARGET_Latitude, src_lng, src_lat)
        try:
            if checkDates(site_contents[i]['Date'],each['Date']):
                continue
        
        except:
            break
        else:
            if distance >= 0:
                    final_result_dict.append(each)
           
    filename = "girish_" + site_contents[i]['SITE_NAME'] + "_challenge.csv"    
    sorted_final_result_dict = sorted(final_result_dict,key=itemgetter('Latitude'))
    export_dict_list_to_csv(sorted_final_result_dict,filename)
filename= sys.argv[0]
uploadTos3(filename,BUCKET_IN_NAME)
    




