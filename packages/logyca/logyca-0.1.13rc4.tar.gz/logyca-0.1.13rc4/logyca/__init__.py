from logyca.utils.constants.logycastatusenum import LogycaStatusEnum
from logyca.utils.constants.app import App

from logyca.schemas.input.claimsdto import ClaimsDTO
from logyca.schemas.input.api_key import APIKeyScheme
from logyca.schemas.input.jwt import BearerToken
from logyca.schemas.input.oauth_token import OAuthTokenScheme 

from logyca.schemas.output.healthdto import HealthEnum
from logyca.schemas.output.apifilterexceptiondto import ApiFilterExceptionDTO
from logyca.schemas.output.apIresultdto import APIResultDTO
from logyca.schemas.output.healthdto import HealthDTO
from logyca.schemas.output.httpexceptiondto import HTTPExceptionDTO
from logyca.schemas.output.tokensdto import TokensDTO

from logyca.utils.helpers.datetimehelpers import convertDateTimeStampUTCtoUTCColombia
from logyca.utils.helpers.stringshelpers import buildUrl
from logyca.utils.helpers.stringshelpers import convert_string_to_boolean
from logyca.utils.helpers.parse_functions import parse_bool

from logyca.utils.handlers.logger import Logger
from logyca.utils.handlers.logger import ConstantsLogger
from logyca.utils.handlers.singleton import Singleton

# If you need the logyca library but without the utilities focused on fastapi
try:
    from logyca.dependencies.api_key_simple_auth import APIKey
    from logyca.dependencies.oauth_token import OAuthToken
    from logyca.utils.handlers.exception_handlers import validation_exception_handler_async
    from logyca.utils.handlers.exception_handlers import http_exception_handler_async
    from logyca.utils.handlers.exception_handlers import unhandled_exception_handler_async
except ImportError:
    APIKey = None
    OAuthToken = None
    validation_exception_handler_async = None
    http_exception_handler_async = None
    unhandled_exception_handler_async = None
