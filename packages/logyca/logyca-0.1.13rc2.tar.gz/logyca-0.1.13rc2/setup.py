#!/usr/bin/env python
from setuptools import setup, find_packages

COMPANY_NAME="LOGYCA"
PACKAGE_NAME = "logyca"
VERSION = "0.1.13rc2"

install_requires = ["pydantic>=1.8","pytz>=2023.3"]
install_requires_fastapi = ["fastapi>=0.96.0","starlette>=0.24.0"]
install_requires_oauth_token = install_requires_fastapi + ["aiohttp>=3.8.5","PyJWT>=2.7.0"]
install_requires_api_key_simple_auth = install_requires_fastapi

extras_require = {
    "oauth_token": install_requires + install_requires_oauth_token,
    "api_key_simple_auth": install_requires + install_requires_api_key_simple_auth,
    "oauth_token-api_key_simple_auth": install_requires + install_requires_oauth_token + install_requires_api_key_simple_auth,
}

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=f'This package name is reserved by {COMPANY_NAME} company',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='MIT License',
    author='Jaime Andres Cardona Carrillo',
    author_email='jacardona@outlook.com',
    url='https://github.com/logyca/python-libraries/tree/main/logyca',
    keywords="api result, result dto, result scheme",
    classifiers=[
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Framework :: Pydantic :: 1",
    "Framework :: Pydantic",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python",
    "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development",
    "Typing :: Typed",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
)
