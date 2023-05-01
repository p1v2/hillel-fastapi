from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

users = {
    "vitalii": "123",
}


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    if username in users and password == users[username]:
        return username
    else:
        raise HTTPException(
            status_code=401,
        )
