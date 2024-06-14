from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from logyca.utils.helpers.stringshelpers import buildUrl
from logyca.utils.helpers.datetimehelpers import convertDateTimeStampUTCtoUTCColombia
from logyca.utils.constants.logycastatusenum import LogycaStatusEnum
from logyca.schemas.output.apIresultdto import APIResultDTO
from logyca.schemas.input.oauth_token import OAuthTokenScheme
import jwt
import aiohttp
from logyca.schemas.input.claimsdto import ClaimsDTO
from logyca.schemas.input.jwt import BearerToken
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from logyca.utils.constants.messages import Messages

auth_scheme = HTTPBearer(auto_error=False)

class OAuthToken:
    '''Description

    ## Example of use
    from fastapi import FastAPI, Depends
    from logyca import OAuthTokenScheme, OAuthToken, ClaimsDTO
    import os

    ENPOINTAZUREB2C_APICRUDURL=os.getenv('APICRUD_URL','https://domain.ccc/')
    ENPOINTAZUREB2C_APICRUDMETHODVALIDATELOGIN=os.getenv('METHOD_VALIDATE_LOGIN','api/method/')
    LOGYCA_APIKEY=os.getenv('LOGYCA_APIKEY','...key...')

    app = FastAPI()

    settings_oauth_token=OAuthTokenScheme(
        endpoint_azure_b2c_apicrud=ENPOINTAZUREB2C_APICRUDURL,
        endpoint_azure_b2c_apicrud_method_validate_login=ENPOINTAZUREB2C_APICRUDMETHODVALIDATELOGIN,
        logyca_apikey=LOGYCA_APIKEY,
        enable=True)
    get_oauth_token = OAuthToken(settings_oauth_token)

    @app.get("/data/")
    def read_item(claims_dto: ClaimsDTO = Depends(get_oauth_token)):
        return {"user checked ok: ": f"{claims_dto}"}
    '''
    
    def __init__(self,oauth_token_scheme:OAuthTokenScheme):
        self.enable=oauth_token_scheme.enable
        self.endpoint_azure_b2c_apicrud=oauth_token_scheme.endpoint_azure_b2c_apicrud
        self.endpoint_azure_b2c_apicrud_method_validate_login=oauth_token_scheme.endpoint_azure_b2c_apicrud_method_validate_login
        self.logyca_apikey=oauth_token_scheme.logyca_apikey
    
    async def __call__(self,bearer_token:BearerToken = Depends(auth_scheme)):
        '''Description
        Used by fastapi dependency injection
        '''
        try:
            claimsDTO=ClaimsDTO()
            if self.enable is False:
                return claimsDTO
            else:
                headers={
                    'Authorization': 'Bearer {0}'.format(bearer_token.credentials),
                    'ApiKey': self.logyca_apikey
                    }
                urlEndpoint=buildUrl(self.endpoint_azure_b2c_apicrud,self.endpoint_azure_b2c_apicrud_method_validate_login)
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.get(urlEndpoint) as response:
                        json_body = await response.json()
                
                if response.status != HTTP_200_OK:
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail=Messages.MSG_UNAUTHORIZED,
                    )
                
                payload = jwt.decode(
                    bearer_token.credentials,
                    algorithms=["RS256"],
                    options={"verify_signature":False}
                    )            
                claimsDTO.name=payload["name"]
                claimsDTO.email=payload["emails"][0]
                claimsDTO.expirationTimeUTCBogota=convertDateTimeStampUTCtoUTCColombia(payload["exp"])
                return claimsDTO
        except Exception as e:        
            api_result_dto = APIResultDTO()
            api_result_dto.apiException.logycaStatus = LogycaStatusEnum.UnAuthenticated
            api_result_dto.apiException.status = LogycaStatusEnum.UnAuthenticated.mappingHttpStatusCode            
            api_result_dto.dataError = True

            raise HTTPException(
                detail=jsonable_encoder(api_result_dto),
                status_code=api_result_dto.apiException.status,
            )