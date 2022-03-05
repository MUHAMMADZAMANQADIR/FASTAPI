from pydantic import BaseModel 
from typing import Optional

 
    
class User(BaseModel):
    name: str
    Cnic: int
    Location :str
    CaseType:str
    Description:Optional[str]=None
     
    