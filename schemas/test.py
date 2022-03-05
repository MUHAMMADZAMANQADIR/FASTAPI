def userEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "name":item["name"],
        "Cnic" : item["Cnic"],
        "Location" :item["Location"],
        "CaseType":item["CaseType"],
        "Description":item["Description"],
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]