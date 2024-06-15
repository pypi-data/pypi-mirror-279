<p align="center">
  <a href="https://logyca.com/"><img src="https://logyca.com/sites/default/files/logyca.png" alt="Logyca"></a>
</p>
<p align="center">
    <em>LOGYCA public libraries</em>
</p>

<p align="center">
<a href="https://pypi.org/project/logyca" target="_blank">
    <img src="https://img.shields.io/pypi/v/logyca?color=orange&label=PyPI%20Package" alt="Package version">
</a>
<a href="(https://www.python.org" target="_blank">
    <img src="https://img.shields.io/badge/Python-%5B%3E%3D3.8%2C%3C%3D3.11%5D-orange" alt="Python">
</a>
</p>


---

# About us

* <a href="http://logyca.com" target="_blank">LOGYCA Company</a>
* <a href="https://www.youtube.com/channel/UCzcJtxfScoAtwFbxaLNnEtA" target="_blank">LOGYCA Youtube Channel</a>
* <a href="https://www.linkedin.com/company/logyca" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="Linkedin"></a>
* <a href="https://twitter.com/LOGYCA_Org" target="_blank"><img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter"></a>
* <a href="https://www.facebook.com/OrganizacionLOGYCA/" target="_blank"><img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>

---

# LOGYCA public libraries

* **Traversal libraries**: Standard methods to be used by microservices.
* **Return codes**: Standard methods for reporting result status codes using APIResult.
* **Monitoring**: Standard methods to report check health status codes.
* **Helpers**: Standard methods to be used. *

[Source code](https://github.com/logyca/python-libraries/tree/main/logyca)
| [Package (PyPI)](https://pypi.org/project/logyca/)
| [Samples](https://github.com/logyca/python-libraries/tree/main/logyca/samples)
| [Unit tests](https://github.com/logyca/python-libraries/tree/main/logyca/tests)

---

---

# "pip install" dependency check
The user must select the required libraries and versions for the project that uses this library, which validates that they are pre-installed in order to be installed.

To install the libraries of the logyca package (APIResult,Health) verifying the pydantic,pytz prerequisite without validating other packages, use the following command:

```Python
# Check pydantic dependency that is installed
pip install logyca
```

To install the fastapi package libraries and logyca authentication dependency injection, use the following command:

```Python
# Check the aiohttp dependency that is installed, for use with oauth authentication, e.g. single sign-on (SSO).
pip install logyca[oauth_token]
# Check the fastapi dependency that is installed, for use with Api-key authentication.
pip install logyca[api_key_simple_auth]
# Check the fastapi dependency that is installed, for use with Api-key and oauth authentication.
pip install logyca[oauth_token-api_key_simple_auth]
```

---

# Semantic Versioning

logyca < MAJOR >.< MINOR >.< PATCH >

* **MAJOR**: version when you make incompatible API changes
* **MINOR**: version when you add functionality in a backwards compatible manner
* **PATCH**: version when you make backwards compatible bug fixes

## Definitions for releasing versions
* https://peps.python.org/pep-0440/

    - X.YaN (Alpha release): Identify and fix early-stage bugs. Not suitable for production use.
    - X.YbN (Beta release): Stabilize and refine features. Address reported bugs. Prepare for official release.
    - X.YrcN (Release candidate): Final version before official release. Assumes all major features are complete and stable. Recommended for testing in non-critical environments.
    - X.Y (Final release/Stable/Production): Completed, stable version ready for use in production. Full release for public use.

# Quick install

```console
# Windows
python -m pip install logyca
# Linux
pip install logyca
```

---

# Example of concepts using library APIResult

```python
# Example output from ApiResult:
result={
  "resultToken": {
    "token": "",
    "refreshToken": "",
    "result": "",
    "emailActiveDirectory": "",
    "message": ""
  },
  "resultObject": [
    {
      "name": "Database server",
      "status": 0,
      "description": "Connection status fine"
    },
    {
      "name": "Redis server",
      "status": 0,
      "description": "Connection status fine"
    }
  ],
  "apiException": {
    "message": "",
    "isError": false,
    "detail": null,
    "status": 200,
    "logycaStatus": 0
  },
  "resultMessage": "",
  "dataError": false
}
```

## Use cases: you must catch de exception

1. if you get data only the token:
```json
{
"dataError":false,
"resultObject":null,
"resultToken":"Not Null"
}
```

2. if you get data correctly
```json
{
"dataError":false,
"resultObject"="Not Null"
"resultToken"=null
}
```

3. if you don't get because the operation was cancelled
```json
{
"dataError":true,
"resultObject":null,
"resultToken":null,
"apiException.logycaStatus":1,
"apiException.status"=404,
"resultMessage":"exception messages: the operation was cancelled"
}
```
[optional]apiException.message="if needed, return an object with structured failure data other than exception messages"


# Example of using library APIResult + Health Check

```python
from fastapi.encoders import jsonable_encoder
from logyca import HealthEnum, LogycaStatusEnum, APIResultDTO, ApiFilterExceptionDTO, HTTPExceptionDTO, HealthDTO, TokensDTO
from starlette.responses import JSONResponse
import json

def example_service():
    tokensDTO=TokensDTO()
    tokensDTO.token='Token Example'

    apiFilterExceptionDTO=ApiFilterExceptionDTO()
    apiFilterExceptionDTO.isError=False
    apiFilterExceptionDTO.logycaStatus=int(LogycaStatusEnum.Already_Exists)
    apiFilterExceptionDTO.status=int(LogycaStatusEnum.Already_Exists.mappingHttpStatusCode)

    httpExceptionDTO=HTTPExceptionDTO()
    httpExceptionDTO.detail='No Problem'

    listHealth=[]

    listHealth.append(HealthDTO(name='Check CPU',status=HealthEnum.Ok,description='OK').__dict__)
    listHealth.append(HealthDTO(name='Check Connect DB',status=HealthEnum.Warning,description='Warning').__dict__)
    listHealth.append(HealthDTO(name='Check Connect Storage',status=HealthEnum.Critical,description='Critical').__dict__)

    apiResultDTO=APIResultDTO()
    apiResultDTO.resultMessage=httpExceptionDTO.detail
    apiResultDTO.resultObject=listHealth
    apiResultDTO.dataError=False
    apiResultDTO.resultToken=tokensDTO
    apiResultDTO.apiException=apiFilterExceptionDTO

    return apiResultDTO

def simulator_api_return():
    apiResultDTO = example_service()
    content = jsonable_encoder(apiResultDTO)
    print((json.dumps(content,indent=4)))
    return JSONResponse(content=content,status_code=200)

simulator_api_return()

# output sample
  #
  # {
  #     "resultToken": {
  #         "token": "Token Example",
  #         "refreshToken": "",
  #         "result": "",
  #         "emailActiveDirectory": "",
  #         "message": ""
  #     },
  #     "resultObject": [
  #         {
  #             "name": "Check CPU",
  #             "status": 0,
  #             "description": "OK"
  #         },
  #         {
  #             "name": "Check Connect DB",     
  #             "status": 1,
  #             "description": "Warning"        
  #         },
  #         {
  #             "name": "Check Connect Storage",
  #             "status": 2,
  #             "description": "Critical"       
  #         }
  #     ],
  #     "apiException": {
  #         "message": "",
  #         "isError": false,
  #         "detail": null,
  #         "status": 409,
  #         "logycaStatus": 6
  #     },
  #     "resultMessage": "No Problem",
  #     "dataError": false
  # }

```

---

# Example of using helpers

```python
from logyca import buildUrl,convertDateTimeStampUTCtoUTCColombia

url1='https://domain.com'
url2='api/get'
print(f'buildUrl={buildUrl(url1,url2)}')
# ouput
# buildUrl=https://domain.com/api/get

datetimestampUTC=1679729109
print(f'datetimeUTCColombia={convertDateTimeStampUTCtoUTCColombia(datetimestampUTC)}')
# output
# datetimeUTCColombia=2023-03-25 02:25:09-05:00
```

---

# Example of using Logger
At the root of the project, the logs folder is created and the types of errors are differentiated by different files.
```python

# main.py
from logyca import Logger, ConstantsLogger
logger = Logger(logger_name=ConstantsLogger.NAME,log_dir=FOLDER_LOGS,log_file_name=f"{App.Settings.NAME}")
logger.info(f"message")

# Other files.py
from logyca import Logger, ConstantsLogger
import logging
logger = logging.getLogger(ConstantsLogger.NAME)

logger.info(f"message")
logger.error(f"message")

```
---

# Current library test

```console
# Library installation

# Windows
python -m pip install logyca[test]
# Linux
pip install logyca

# Run it
pytest -s
```

---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

## [0.1.9] - 2024-05-21
### Added
- New logger functionality.
- new authentication functionality in fastapi by dependency injection with api-key, to be used on endpoints.
- new authentication functionality in fastapi by dependency injection with oauth (single sign on), to be used on endpoints.
- In the samples folder of this library, there are complete working examples of using the code.

## [0.1.8] - 2023-10-03
### Fixed
- Due to a link error in the readme to internal documents in pypi, we chose to leave the changelog at the end of the readme. 

## [0.1.7] - 2023-10-02
### Fixed
- The url address for the logyca logo is corrected
- Adjust return code for LogycaStatusEnum class: LogycaStatusEnum.Created==HTTPStatus.CREATED
- Adjust return code for LogycaStatusEnum class: LogycaStatusEnum.InProcess==HTTPStatus.ACCEPTED
- Adjust return code for LogycaStatusEnum class: LogycaStatusEnum.Partial==HTTPStatus.ACCEPTED
- Empty files __init__.py removed

## [0.1.6] - 2023-09-11
### Fixed
- Pydantic restriction for versions lower than 2.0 is removed

## [0.1.5] - 2023-03-27
### Added
- Release ready for production

## [0.1.6-9] - 2024-5-21<
### Added
- new features such as: logging, helpers for fastapi

## [0.1.10] - 2024-05-23
### Added
- Documentation improvements.
- Documentation integrated with github

## [0.1.11] - 2024-05-24
### Deprecated
- add print info deprecated in convert_string_to_boolean()
### Added
- new parse_bool() function that will replace convert_string_to_boolean()

## [0.1.12-13] - 2024-06-13
### Fixed
- Oauth fix

## [0.1.13] - 2024-06-14
### Added
- New Logger feature to rotate backup logs and allow them to be written.
