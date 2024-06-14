from pydantic import BaseModel,Field

class OAuthTokenScheme(BaseModel):
    enable:bool=Field(default=True,description="Used to enable the check, if it is disabled the endpoint will log in without checking authentication")
    endpoint_azure_b2c_apicrud:str=Field(default=True,description="enpoint azure b2c apicrudurl")
    endpoint_azure_b2c_apicrud_method_validate_login:str=Field(default=True,description="endpoint azure b2c apicrud method for  validate login")
    logyca_apikey:str=Field(default='',description="Api key for platform")
    