from logyca.schemas.input.api_key import APIKeyScheme
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

header_value="x-api-key"

auth_scheme_api_key_header = APIKeyHeader(name=header_value, auto_error=False)

class APIKey:
    '''Description

    ## Example of use
    from fastapi import FastAPI, Depends
    from logyca import APIKeyScheme, APIKey
    import os

    APY_KEY=os.getenv('APY_KEY','password_key')

    app = FastAPI()

    settings_api_key=APIKeyScheme(key=APY_KEY, enable=True)
    get_api_key = APIKey(settings_api_key)

    @app.get("/data/")
    def read_item(api_key: str = Depends(get_api_key)):
        return {"api_key checked ok: ": f"{api_key}"}
    '''    
    def __init__(self,api_key_scheme:APIKeyScheme):
        self.api_key=api_key_scheme.key
        self.check_enable=api_key_scheme.enable
    
    async def __call__(self,api_key_header: str = Security(auth_scheme_api_key_header)):
        '''Description
        Used by fastapi dependency injection
        '''
        if self.check_enable is False:
            return ''
        elif api_key_header == self.api_key:
            return api_key_header   
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
            )
