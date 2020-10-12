import secrets
import json

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


    def getMap(self, dataset):

        name_col = 'States'
        data_col = 'Density'
        
        print("In the getMap function   ")
        #the geojson file with the borders, the shape file
        with open("Services/US_States.json", "r") as read_file:
            area = json.load(read_file)    

        #assign the color fill to each line
        colors =[(237,248,233), (186,228,179), (116,196,118), (49,163,84), (0,109,44)]
        numColors = len(colors)
        low = int(dataset[0][data_col])
        high = int(dataset[0][data_col])

        for line in dataset:
            x = int(line[data_col])
            high = max(x, high)
            low = min(x,low)


        bucketSize = (high - low)/numColors

        for line in area["features"]:
            name = line["properties"]["NAME"]
            for dataset_line in dataset:
                if name == dataset_line[name_col]:
                    num = int(dataset_line[data_col])
                    line["properties"]["data"] = num
                    bucketNum = int((num - low)//bucketSize)
                    line["properties"]["color"] = colors[bucketNum]
                    break
        
        bucketGrades = []
        for i in range(numColors):
            bucketGrades.append(int(low + i * bucketSize))

        return area, colors, bucketGrades