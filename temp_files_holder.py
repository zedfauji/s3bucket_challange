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


"""def conver_csv_into_dict(filename):
    
    with open(filename) as File:
        dictReader = csv.DictReader(File)
        for row in dictReader:
            dictResults.append(row)
        print dictResults[0:1]"""

