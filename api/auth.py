import psycopg2

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pwdlib import PasswordHash

from api.security import create_access_token


router = APIRouter()

password_hash = PasswordHash.recommended()


class LoginRequest(BaseModel):
    username: str
    password: str


def get_database_connection():
    return psycopg2.connect(
        dbname="apex_manufacturing",
        user="bidya",
        host="localhost",
        port="5432"
    )


@router.post("/login")
def login(request: LoginRequest):

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            u.user_id,
            u.username,
            u.password_hash,
            u.account_status,
            r.role_name
        FROM app_user u
        JOIN user_role ur
            ON u.user_id = ur.user_id
        JOIN role r
            ON ur.role_id = r.role_id
        WHERE u.username = %s
        """,
        (request.username,)
    )

    user = cursor.fetchone()

    if user is None:
        cursor.close()
        connection.close()

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    user_id, username, stored_hash, account_status, role_name = user

    if account_status != "Active":
        cursor.close()
        connection.close()

        raise HTTPException(
            status_code=403,
            detail="User account is not active"
        )

    if not password_hash.verify(
        request.password,
        stored_hash
    ):
        cursor.close()
        connection.close()

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    cursor.execute(
        """
        UPDATE app_user
        SET last_login = CURRENT_TIMESTAMP
        WHERE user_id = %s
        """,
        (user_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    access_token = create_access_token(
        user_id,
        username,
        role_name
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id,
        "username": username,
        "role": role_name
    }