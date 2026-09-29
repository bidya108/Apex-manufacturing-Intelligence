import psycopg2


def get_database_connection():
    return psycopg2.connect(
        dbname="apex_manufacturing",
        user="bidya",
        host="localhost",
        port="5432"
    )


def log_audit_event(
    user_id,
    username,
    role_name,
    action,
    endpoint,
    http_method,
    status_code,
    details=None
):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO audit_log (
            user_id,
            username,
            role_name,
            action,
            endpoint,
            http_method,
            status_code,
            details
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            username,
            role_name,
            action,
            endpoint,
            http_method,
            status_code,
            details
        )
    )

    connection.commit()

    cursor.close()
    connection.close()