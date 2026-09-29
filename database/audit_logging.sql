CREATE TABLE IF NOT EXISTS audit_log (
    audit_id BIGSERIAL PRIMARY KEY,

    user_id INTEGER,
    username VARCHAR(100),
    role_name VARCHAR(100),

    action VARCHAR(100) NOT NULL,
    endpoint VARCHAR(255),
    http_method VARCHAR(10),

    status_code INTEGER,

    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    details TEXT,

    CONSTRAINT fk_audit_user
        FOREIGN KEY (user_id)
        REFERENCES app_user(user_id)
        ON DELETE SET NULL
);


CREATE INDEX IF NOT EXISTS idx_audit_log_user
    ON audit_log(user_id);


CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp
    ON audit_log(event_timestamp);


CREATE INDEX IF NOT EXISTS idx_audit_log_action
    ON audit_log(action);


CREATE INDEX IF NOT EXISTS idx_audit_log_endpoint
    ON audit_log(endpoint);