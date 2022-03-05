import shutil
import Imagematching.image 
from fastapi import APIRouter, UploadFile , File
from Models.test import User
from Config.db import conn 
from typing import List
from schemas.test import  userEntity, usersEntity  
from bson import ObjectId
user = APIRouter() 
global pathn
def getpath():
     return pathn
 
@user.get('/')
async def find_all_users():
    print(conn.CRIMINALRECORD.CRIMINALs.find())
    return  usersEntity(conn.CRIMINALRECORD.CRIMINALs.find())

@user.post("/image")
async def getimage(file: UploadFile=File(...)):
    global pathn
    try:
        pathn = f'upload/{file.filename}'
        with open(pathn ,"wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    getpath()
    name = Imagematching.image.name()
    name = name.title()
    
    criminaldic = {}
    criminaldic = Search_Name(name)
    print(criminaldic)

    return  criminaldic
    
     

@user.post('/')
async def create_user(user: User):
    conn.CRIMINALRECORD.CRIMINALs.insert_one(dict(user))
    return userEntity(conn.CRIMINALRECORD.CRIMINALs.find())


@user.get('/{Cnic}')
async def Search_Cnic(Cnic):
    allcriminal=[];
    allcriminal=usersEntity(conn.CRIMINALRECORD.CRIMINALs.find())
    a=0;
    for entry in allcriminal:
        for key,value in entry.items():
            if str(value) == str(Cnic):
                print(entry)
                return entry
         
    
    return "Not found"

@user.get('/{name}')
async def Search_by_Name_and_Cnic(name):
    dic={}
    dic = Search_Name(name.title())
    if(bool(dic)):
        return dic
    
    return "Not found"
     
def Search_Name(name):
    print(name)
    allcriminal=[];
    allcriminal=usersEntity(conn.CRIMINALRECORD.CRIMINALs.find())
    
    for entry in allcriminal:
        for key,value in entry.items():
            if str(value) == str(name):
                return entry
    
    return "Not found"

 
    
 


#uvicorn main:app --reload