-- ============================================================
-- APEX MANUFACTURING
-- AUTHENTICATION DATABASE SCHEMA
-- ============================================================

-- ============================================================
-- ROLES
-- ============================================================

CREATE TABLE IF NOT EXISTS role (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(200)
);


-- ============================================================
-- USERS
-- ============================================================

CREATE TABLE IF NOT EXISTS app_user (
    user_id SERIAL PRIMARY KEY,
    employee_id INTEGER,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    account_status VARCHAR(30) NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,

    CONSTRAINT fk_app_user_employee
        FOREIGN KEY (employee_id)
        REFERENCES employee_user(user_id),

    CONSTRAINT chk_account_status
        CHECK (
            account_status IN (
                'Active',
                'Inactive',
                'Locked'
            )
        )
);


-- ============================================================
-- USER ROLES
-- ============================================================

CREATE TABLE IF NOT EXISTS user_role (
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,

    PRIMARY KEY (user_id, role_id),

    CONSTRAINT fk_user_role_user
        FOREIGN KEY (user_id)
        REFERENCES app_user(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_user_role_role
        FOREIGN KEY (role_id)
        REFERENCES role(role_id)
        ON DELETE CASCADE
);


-- ============================================================
-- DEFAULT APPLICATION ROLES
-- ============================================================

INSERT INTO role (role_name, description)
VALUES
    ('Executive', 'Access to executive business intelligence and reports'),
    ('Production Manager', 'Access to production and operational information'),
    ('Maintenance Manager', 'Access to machine health and maintenance information'),
    ('Data Analyst', 'Access to analytics, reports and data quality information'),
    ('Data Scientist', 'Access to machine learning and predictive analytics'),
    ('Data Administrator', 'Access to data administration and data quality management'),
    ('System Administrator', 'Access to system configuration and administration')
ON CONFLICT (role_name) DO NOTHING;