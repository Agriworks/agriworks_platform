from Services.LocationRelationshipService import LocationRelationshipService 

service = LocationRelationshipService()

def test_villageToDistrict():
    assert service.villageToDistrict("Tewksbury") == "Hunterdon"
    assert service.villageToDistrict("Manasquan") == "Monmouth"

def test_districtToState():
    assert service.districtToState("Hunterdon") == "New Jersey"
    assert service.districtToState("Monmouth") == "New Jersey"

def test_districtToVillage():
    assert len(service.districtToVillage("Hunterdon")) == 3 
    assert "Wall" in service.districtToVillage("Monmouth")

def test_stateToDistrict():
    assert len(service.stateToDistrict("New Jersey")) == 2
    assert "Hunterdon" in service.stateToDistrict("New Jersey")

