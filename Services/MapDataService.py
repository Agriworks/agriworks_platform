import secrets
import json
from flask import current_app


from shapely.geometry import Point, shape
from shapely.geometry.polygon import Polygon

class MapDataService():
    def __init__(self):
        return

    def map(self, dataset, column_labels, loc_col, data_col1, data_col2):
        print("Right here")
        panelLabel = 'Value'
        if loc_col == '-1' or data_col1 == '-1':
            #if the call did not specify a location or data col, it finds the first location or data col to use
            location = False
            data = False
            print("In first loop")
            for label in column_labels:
                print(label)
                value = column_labels[label]
                if(not location and (value == 'loc_district' or value == 'loc_state' or value == 'loc_village' or value == 'loc_country')):
                    location = label
                if(not data and (value == 'data_num')):
                    data = label    
                    panelLabel = label
                if(not (not location or not data)):
                    break
        else:
            location = loc_col
            if data_col2 == '-1':
                data = data_col1
                panelLabel = data_col1
            else:
                #add a new col to dataset that is the first data_col divided by the second data col
                for line in dataset:
                    line["newDataColForChoroMap"] = float(line[data_col1])/float(line[data_col2])
                data = "newDataColForChoroMap" #made the name extra complicated to make sure that it is not a name that another column would have
                panelLabel = data_col1 + ' per ' + data_col2

        return self.getMap(dataset, location, data, column_labels, panelLabel)

    
    def getAdminLevel(self, column_labels, loc_col):
        name = column_labels[loc_col]
        
        if name == 'loc_country':
            return 0
        if name == 'loc_state':
            return 1
        if name == 'loc_district':
            return 2
        if name == 'loc_village':
            return 3
        
        return -1

        

    def getMap(self, dataset, loc_col, data_col, admin_level, panelLabel):

        print("Getting map")
        print(loc_col)
        print(data_col)
        print(admin_level)
        
        admin_level = self.getAdminLevel(admin_level, loc_col)

        if admin_level == -1:
            return -1,-1,-1
    
        data_col = data_col.strip() #remove any spaces

        nameField = "NAME_" + str(admin_level) #the way the json is set up is that the most specific name for a feature is a at Name_ + the admin level

        checkName = True # if the location column is the name of places, then we will match features to rows by names

        if(isinstance(loc_col, list)): # if it is long and lat then it will be a list
            checkName = False 

        fileName = "GeoJSON/IND_adm" + str(admin_level) + ".geojson"

        #the geojson file with the borders, the shape file
        with open(fileName, encoding="utf-8") as read_file:
            area = json.load(read_file)

        # print("Opened file")

        #assign the color fill to each line
        colors =[(237,248,233), (186,228,179), (116,196,118), (49,163,84), (0,109,44)] #GREEN
        #colors = [(239,243,255), (189,215,231), (107,174,214), (49,130,189), (8,81,156)] BLUE
        numColors = len(colors)
       

        if checkName:

            # print("About to get high and low")
            # print(dataset[0])

            #get the high and low so that the right color can be assigned when giving it the data 
            low = int(dataset[0][data_col])
            high = int(dataset[0][data_col])

            # print("This worked")


            for line in dataset:
                x = int(line[data_col])
                high = max(x, high)
                low = min(x,low)

            # print("Got high and low")
            # print(low)
            # print(high)

            bucketSize = (high - low)/numColors

            # print("Got Bucket Size")

            for line in area["features"]:
                line["properties"]["name"] = line["properties"][nameField]
                name = line["properties"][nameField]
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

            # print("This is done")

        else: #using location coordinates

            #update low and high as we run through the dataset
            low = int(0) #if you set it to something that is not 0 and then there is a feature that has not locations in it, the low would not be right
            high = int(dataset[0][data_col])

            #then loop through the dataset, I did the double loop this way because if the location from the dataset matches a feature, then you can break loop
            for dataset_line in dataset:
                loc = dataset_line[loc_col]
                num = int(dataset_line[data_col])
                #convert the location to a point
                if loc_col.length == 1:
                    result = [x.strip() for x in loc.split(',')]
                else:
                    result = [loc_col[0], loc_col[1]]
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
                line["properties"]["name"] = line["properties"][nameField]
            
        bucketGrades = []
        for i in range(numColors):
            bucketGrades.append(int(low + i * bucketSize))



        print("Made Map")
        return area, colors, bucketGrades, panelLabel