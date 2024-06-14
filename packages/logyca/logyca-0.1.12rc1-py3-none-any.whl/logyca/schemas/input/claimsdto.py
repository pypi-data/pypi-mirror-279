from pydantic import BaseModel,Field

class ClaimsDTO(BaseModel):
    name:str=Field(default='',description="User name")
    email:str=Field(default='',description="Email from user")
    expirationTimeUTCBogota:str=Field(default='',description="Expiration data from user token")
