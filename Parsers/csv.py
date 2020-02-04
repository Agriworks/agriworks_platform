import pandas as pd
import numpy
from Parsers import Parser

class CSVParser(Parser):

    def __init__(self):
        self.data = pd.read_csv(self.datasetSource)

    def createLegendAndNonRepeatingKeys(self):
        #Combine repeated column data into legend
        for i in self.keys:
            if len(self.data[i]) <= 1: #if only one row of values, then quit
                break
            if self.data[i].nunique() == 1: #if all entries have the same value
                if str(self.data[i][0]) != 'nan': #checking to make sure value in not nan
                    self.legend[i] = self.data[i][0]
                if isinstance(self.data[i][0], numpy.int64):
                    self.legend[i] = int(self.data[i][0])
            else:
                #TODO: Optimize
                currentNonRepeatedKeyIndex = self.keys.index(i)
                self.nonRepeatingKeys.append(self.keys[currentNonRepeatedKeyIndex])                   
    
    def createDataObjects(self):
        #Populate data into database 
        for i in range(len(self.data)):
            dataObject = DataObject(dataSetId=self.datasetId)
            for j in range(len(self.keys)):
                currentItem = self.data.iloc[i][j]
                if (self.keys[j] not in self.legend):                      
                    if (isinstance(currentItem, numpy.int64)):
                        currentItem = int(currentItem) #cast int64 objects to ints 
                    dataObject[keys[j]] = currentItem
            dataObject.save()

    def parse(self):
        self.createLegendAndNonRepeatingKeys()

        datasetObject = Dataset(
            name=self.datasetName,
            author=self.datasetAuthor,
            keys=self.nonRepeatingKeys,
            legend=self.legend,
            public=True if request.form.get("permissions") == "Public" else False,
            tags=request.form.get("tags"),
            datasetType=request.form.get("type")
        )
        
        datasetObject.save()

        self.datasetId = datasetObject.id

        self.createDataObjects()
