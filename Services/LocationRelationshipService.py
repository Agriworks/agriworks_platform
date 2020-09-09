import csv

class LocationRelationshipService():
    def __init__(self):
        # TODO: update version functionality
        self.version = None
        # Load location relationships onto memory upon initization
        villageToDistrictDic = {}
        districtToStateDic = {}
        with open("../LocationRelationships.csv") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=",")
            csvreader.next()
            for row in csvreader:
                villageToDistrictDic[row[2]] = row[1]
                districtToStateDic[row[1]] = row[0]
        self.villageToDistrictDic = villageToDistrictDic
        self.districtToStateDic = districtToStateDic
        return

    def villageToDistrict(self,village):
        return self.villageToDistrictDic[village]

    def districtToState(self,district):
        return self.districtToStateDic[district]

    def getVersion(self):
        return self.version

    