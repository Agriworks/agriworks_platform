import secrets



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

    



   