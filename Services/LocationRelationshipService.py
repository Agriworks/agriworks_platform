from flask import current_app
import csv

class LocationRelationshipService():
    def __init__(self):
        # TODO: update version functionality
        self.version = None
        # Load location relationships onto memory upon initization
        villageToDistrictDic = {}
        districtToStateDic = {}
        districtToVillageDic = {}
        stateToDistrictDic = {}
        with open("LocationRelationShip.csv") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=",")
            # csvreader.next()
            for row in csvreader:
                print(row)
                villageToDistrictDic[row[2]] = row[1]
                districtToStateDic[row[1]] = row[0]
                if row[1] not in districtToVillageDic.keys():
                    districtToVillageDic[row[1]] = set()
                districtToVillageDic[row[1]].add(row[2])
                if row[0] not in stateToDistrictDic.keys():
                    stateToDistrictDic[row[0]] = set()
                stateToDistrictDic[row[0]].add(row[1])
        self.villageToDistrictDic = villageToDistrictDic
        self.districtToStateDic = districtToStateDic
        self.districtToVillageDic = districtToVillageDic
        self.stateToDistrictDic = stateToDistrictDic
        return

    def villageToDistrict(self,village):
        return self.villageToDistrictDic[village]

    def districtToState(self,district):
        return self.districtToStateDic[district]

    def districtToVillage(self,district):
        return self.districtToVillageDic[district]

    def stateToDistrict(self,state):
        return self.stateToDistrictDic[state]
        
    def getVersion(self):
        return self.version
