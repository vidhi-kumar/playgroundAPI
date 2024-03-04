'''
This class `jwtBearer` extends `HTTPBearer` from FastAPI's security module.
It overrides the `__call__` method to verify and extract JWT credentials from the request.

The `verify_jwt` method checks the validity of the JWT token, and `return_email` returns the email from the decoded payload.

'''


from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid or expired token")
    
    def verify_jwt(self, jwtoken: str):
        isTokenValid: bool = False
        payload = decodeJWT(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid
    
    def return_email(self, jwtoken: str):
        payload = decodeJWT(jwtoken)
        email = payload['email']
        return email    
    
  