import functools
import json
import logging
from typing import Callable

import azure.functions as func
from jose import JWTError

from .bearer import AuthenticationTokenException
from .bearer import extract_claims
from .bearer import validate_claims


def extract_authentication_claims(req: func.HttpRequest):
    auth = req.headers.get("Authorization", None)
    return extract_claims(auth)

def authenticate_request(required_claims: dict[str, any]) -> func.HttpResponse:
    def argument_wrapper(callback: Callable[..., any]):
        @functools.wraps(callback)
        def wrapper(req: func.HttpRequest, *args, **kwargs) -> func.HttpResponse:
            try:
                logging.info(
                    f"KBRAIN Authentication. Required claims: {json.dumps(required_claims)}"
                )
                try:
                    token_claims = extract_authentication_claims(req)
                    validate_claims(token_claims, required_claims)
                except (AuthenticationTokenException, JWTError) as ae:
                    return func.HttpResponse(str(ae), status_code=401)

                data, status, headers = callback(req, *args, **kwargs)
                return func.HttpResponse(
                    data, 
                    status_code=status,
                    headers=headers
                )
            except Exception as ex:
                return func.HttpResponse(str(ex), status_code=500)

        return wrapper

    return argument_wrapper
