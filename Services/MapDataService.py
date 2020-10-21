import secrets
import json
from flask import current_app


from shapely.geometry import Point, shape
from shapely.geometry.polygon import Polygon

import boto3
import botocore

s3 = current_app.awsSession.client('s3')

class MapDataService():
    def __init__(self):
        return

    
    def getGeojson(self, admin_level):
        name = "IND_adm" + str(admin_level) + ".geojson"
        nameField = "NAME" + admin_level




    def getMap(self, dataset, loc_col, data_col):

        print("Int here")
        checkName = True

        #the geojson file with the borders, the shape file
        with open("Services/IND_adm1.geojson", encoding="utf-8") as read_file:
            area = json.load(read_file)

        print("opened file")
        #assign the color fill to each line
        colors =[(237,248,233), (186,228,179), (116,196,118), (49,163,84), (0,109,44)] #GREEN
        #colors = [(239,243,255), (189,215,231), (107,174,214), (49,130,189), (8,81,156)] BLUE
        numColors = len(colors)
       

        if checkName:
            #get the high and low so that the right color can be assigned when giving it the data 
            low = int(dataset[0] [data_col])
            high = int(dataset[0][data_col])


            for line in dataset:
                x = int(line[data_col])
                high = max(x, high)
                low = min(x,low)

            print("Got high and low")
            print(low)
            print(high)

            bucketSize = (high - low)/numColors

            for line in area["features"]:
                name = line["properties"]["NAME_1"]
                found_match = False
                for dataset_line in dataset:
                    if name == dataset_line[loc_col]:
                        num = int(dataset_line[data_col])
                        line["properties"]["data"] = num
                        bucketNum = int((num - low -1)//bucketSize)
                        line["properties"]["color"] = colors[bucketNum]
                        found_match = True
                        break
                if not found_match:
                    line["properties"]["data"] = 0
                    line["properties"]["color"] = colors[0]
                    low = 0

        else: #using location coordinates

            #update low and high as we run through the dataset
            low = int(0) #if you set it to something that is not 0 and then there is a feature that has not locations in it, the low would not be right
            high = int(dataset[0][data_col])

            #then loop through the dataset, I did the double loop this way because if the location from the dataset matches a feature, then you can break loop
            for dataset_line in dataset:
                loc = dataset_line[loc_col]
                num = int(dataset_line[data_col])
                #convert the location to a point
                result = [x.strip() for x in loc.split(',')]
                point = Point(float(result[1]), float(result[0])) #need to switch it for reason due to Shapely

                for feature in area["features"]:
                    polygon = shape(feature['geometry'])
                    if polygon.contains(point):
                        if "data" in feature["properties"]:
                            pre_num = feature["properties"]["data"] #what the data was already set to
                            high = max(high, (pre_num + num))
                            feature["properties"]["data"] = pre_num + num
                        else:
                            high = max(high, num)
                            feature["properties"]["data"] = num
                        break
                    
            bucketSize = (high - low)/numColors

            #assign all of the features colors 
            for line in area["features"]:
                if not "data" in line["properties"]:
                    line["properties"]["data"] = 0
                num = line["properties"]["data"]
                bucketNum = int((num - low)//bucketSize)
                line["properties"]["color"] = colors[bucketNum]
            
        bucketGrades = []
        for i in range(numColors):
            bucketGrades.append(int(low + i * bucketSize))


        return area, colors, bucketGrades