from pydantic import BaseModel

class BearerToken(BaseModel):
    scheme: str = 'Bearer'
    credentials: str

