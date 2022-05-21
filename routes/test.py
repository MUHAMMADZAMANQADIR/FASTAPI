import shutil
import Imagematching.image 
from fastapi import APIRouter, UploadFile , File
from Models.test import User
from Config.db import conn 
from typing import List
from schemas.test import  userEntity, usersEntity  
from difflib import SequenceMatcher ,get_close_matches
from bson import ObjectId
from io import BytesIO
from PIL import Image
user = APIRouter() 
global pathn
global allcriminals
def getpath():
     return pathn


@user.get('/')
async def find_all_users():
    print(conn.CRIMINALRECORD.CRIMINALs.find())
    allcriminal = usersEntity(conn.CRIMINALRECORD.CRIMINALs.find())
    return allcriminal


def similarity(str1, list):
    return get_close_matches(str1 ,list ,n=3 ,cutoff=0.1)


@user.get('/similarcases/{inputstr}')
async def find_similarcases(inputstr):
    global allcriminals
    allcriminals = usersEntity(conn.CRIMINALRECORD.CRIMINALs.find())
    Descriptionlist=[];
    matches=[]
    for entry in allcriminals:
        for key,value in entry.items():
            if key == 'Description':
                Descriptionlist.append(value)
    
    matches = similarity(inputstr, Descriptionlist)
    
    if(len(matches)>=0):
        
       return getsimilarcasesdata(matches)
    else:
        "Nothing similar"
    
                
def getsimilarcasesdata(list):
    i=0
    data=[]
    print(len(list))
    while(i < len(list)):
        for entry in allcriminals:
            for key, value in entry.items():
                if str(value) == str(list[i]):
                   data.append(entry)
                   i=i+1;
                   if(i==len(list)):
                       return data
                 
#------------------------


@user.post("/files")
async def UploadImage(file: bytes = File(...)):
    with open('image.jpg', 'wb') as image:
        image.write(file)
        image.close()
    return 'got it'
@user.post("/putObject")
async def put_object(file: UploadFile = File(...)) -> str:

    request_object_content = await file.read()
    img = Image.open(BytesIO(request_object_content))
    
    return "okay";
#-------------------
@user.post("/image")
async def getimage(file: UploadFile = File(...)):
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
    
    return {"Not found"}

 
    
 


# pipenv shell and uvicorn main:app --reload and http://127.0.0.1:8000/docs