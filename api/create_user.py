from getpass import getpass

import psycopg2
from pwdlib import PasswordHash


def get_database_connection():
    return psycopg2.connect(
        dbname="apex_manufacturing",
        user="bidya",
        host="localhost",
        port="5432"
    )


def create_user():
    print("Apex Manufacturing - Create Application User")
    print("--------------------------------------------")

    username = input("Username: ").strip()
    email = input("Email: ").strip()

    password = getpass("Password: ")
    confirm_password = getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    role_name = input("Role [Data Analyst]: ").strip()

    if not role_name:
        role_name = "Data Analyst"

    password_hash = PasswordHash.recommended().hash(password)

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role_id
        FROM role
        WHERE role_name = %s
        """,
        (role_name,)
    )

    role = cursor.fetchone()

    if role is None:
        print(f"Role not found: {role_name}")
        cursor.close()
        connection.close()
        return

    role_id = role[0]

    cursor.execute(
        """
        INSERT INTO app_user (
            username,
            password_hash,
            email,
            account_status
        )
        VALUES (%s, %s, %s, 'Active')
        RETURNING user_id
        """,
        (
            username,
            password_hash,
            email
        )
    )

    user_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO user_role (
            user_id,
            role_id
        )
        VALUES (%s, %s)
        """,
        (
            user_id,
            role_id
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print()
    print("Application user created successfully.")
    print(f"User ID: {user_id}")
    print(f"Username: {username}")
    print(f"Role: {role_name}")


if __name__ == "__main__":
    create_user()