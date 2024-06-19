import json

from jose import jwt


class AuthenticationTokenException(Exception):
    def __init__(self, error):
        super().__init__(error)


def extract_claims(token: str) -> list:
    if not token:
        raise AuthenticationTokenException(
            "Authentication error: Authorization header is missing"
        )

    parts: list[str] = token.split()

    if parts[0].lower() != "bearer":
        raise AuthenticationTokenException(
            "Authentication error: Authorization header must start with ' Bearer'"
        )
    elif len(parts) == 1:
        raise AuthenticationTokenException("Authentication error: Token not found")
    elif len(parts) > 2:
        raise AuthenticationTokenException(
            "Authentication error: Authorization header must be 'Bearer <token>'"
        )

    token_claims: dict[str, any] = jwt.get_unverified_claims(parts[1])
    return token_claims


def validate_claims(
    token_claims: dict[str, any], required_claims: dict[str, any]
) -> bool:
    for key in required_claims:
        if key not in token_claims or token_claims[key] != required_claims[key]:
            raise AuthenticationTokenException(
                "Authentication error: The token provided does not have sufficiently valid claims to authorize access to this service."
            )

    return True
