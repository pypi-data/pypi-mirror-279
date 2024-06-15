from pydantic import BaseModel,Field

class APIKeyScheme(BaseModel):
    enable:bool=Field(default=True,description="Used to enable the check, if it is disabled the endpoint will log in without checking authentication")
    key:str=Field(default='',description="Header api key")
    