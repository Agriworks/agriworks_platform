import secrets
import json
from shapely.geometry import shape, GeometryCollection, Point


class VisualizeService():
    def __init__(self):
        return
    
    def getFormattedData(self, dataset, xAxis, yAxis):
        color = ['rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)']


        data = {}
        

        for line in dataset:
            if line[xAxis] in data:
                data[line[xAxis]] += round(float(line[yAxis]))
            else:
                data[line[xAxis]] = round(float(line[yAxis]))
        
        datacollection = {}
        datacollection['datasets'] = []
        datacollection['labels'] = []


        datasetObj = {'label':'', 
                      'data':[],
                      'backgroundColor':[],
                      'borderColor': [],
                      'borderWidth': 1,
                      'fill': False}

        for key, value in data.items():
            datacollection['labels'].append(key)
            datasetObj['data'].append(value)
            datasetObj['label'] = yAxis
            randomColor = secrets.choice(color)
            datasetObj['backgroundColor'].append(randomColor)
            datasetObj['borderColor'].append(randomColor)
        

        datacollection['datasets'].append(datasetObj)


        return datacollection


    def getMap(self, dataset, loc_col, data_col):

        checkName = False

        print("In the getMap Function")

        #the geojson file with the borders, the shape file
        with open("Services/US_States.json", "r") as read_file:
            area = json.load(read_file)    

        #assign the color fill to each line
        colors =[(237,248,233), (186,228,179), (116,196,118), (49,163,84), (0,109,44)]
        numColors = len(colors)
        low = int(dataset[0] [data_col])
        high = int(dataset[0][data_col])

        for line in dataset:
            x = int(line[data_col])
            high = max(x, high)
            low = min(x,low)

        bucketSize = (high - low)/numColors

        if checkName:
            for line in area["features"]:
                name = line["properties"]["NAME"]
                for dataset_line in dataset:
                    if name == dataset_line[loc_col]:
                        num = int(dataset_line[data_col])
                        line["properties"]["data"] = num
                        bucketNum = int((num - low)//bucketSize)
                        line["properties"]["color"] = colors[bucketNum]
                        break

        else: #using location coordinates
            #first loop through all the features and add data and color properties
            print("About to go through features")
            for line in area["features"]:
                num = 0
                line["properties"]["data"] = num
                bucketNum = int((num - low)//bucketSize)
                line["properties"]["color"] = colors[bucketNum]

            #then loop through the dataset, I did the double loop this way because if the location from the dataset matches a feature, then you can break loop
            for dataset_line in dataset:
                loc = dataset_line[loc_col]
                num = int(dataset_line[data_col])
                #convert the location to a point
                result = [x.strip() for x in loc.split(',')]
                point = Point(result[0], result[1])
                print(point)
                for feature in area["features"]:
                    polygon = shape(feature['geometry'])

                    if polygon.contains(point):
                        print("Found where it belongs")
            
        bucketGrades = []
        for i in range(numColors):
            bucketGrades.append(int(low + i * bucketSize))

        return area, colors, bucketGrades