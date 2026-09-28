# Data Dictionary

## 1. Facility

| Field | Data Type | Required | Description |
|---|---|---|---|
| facility_id | INTEGER | Yes | Unique identifier for the facility |
| facility_name | VARCHAR(100) | Yes | Name of the manufacturing facility |
| location | VARCHAR(150) | Yes | Physical location of the facility |
| facility_status | VARCHAR(30) | Yes | Current operational status of the facility |
| created_date | DATE | Yes | Date the facility record was created |


## 2. Production Line

| Field | Data Type | Required | Description |
|---|---|---|---|
| production_line_id | INTEGER | Yes | Unique identifier for the production line |
| facility_id | INTEGER | Yes | Facility associated with the production line |
| production_line_name | VARCHAR(100) | Yes | Name of the production line |
| production_line_status | VARCHAR(30) | Yes | Current status of the production line |
| production_capacity | INTEGER | Yes | Expected production capacity |
| created_date | DATE | Yes | Date the production line record was created |


## 3. Machine

| Field | Data Type | Required | Description |
|---|---|---|---|
| machine_id | INTEGER | Yes | Unique identifier for the machine |
| production_line_id | INTEGER | Yes | Production line where the machine operates |
| machine_name | VARCHAR(100) | Yes | Name or identifier of the machine |
| machine_type | VARCHAR(100) | Yes | Type or category of machine |
| manufacturer | VARCHAR(100) | No | Machine manufacturer |
| installation_date | DATE | No | Date the machine was installed |
| operating_status | VARCHAR(30) | Yes | Current operating status |
| last_maintenance_date | DATE | No | Date of most recent maintenance |


## 4. Production Record

| Field | Data Type | Required | Description |
|---|---|---|---|
| production_record_id | INTEGER | Yes | Unique production record identifier |
| production_line_id | INTEGER | Yes | Production line associated with the production record |
| production_date | DATE | Yes | Date of production |
| production_target | INTEGER | Yes | Planned number of units |
| actual_production | INTEGER | Yes | Actual number of units produced |
| production_efficiency | DECIMAL(5,2) | Yes | Production performance relative to target |
| downtime_duration | DECIMAL(10,2) | Yes | Downtime duration in minutes |
| shift | VARCHAR(30) | Yes | Production shift |


## 5. Machine Sensor Reading

| Field | Data Type | Required | Description |
|---|---|---|---|
| sensor_reading_id | BIGINT | Yes | Unique sensor reading identifier |
| machine_id | INTEGER | Yes | Machine that generated the reading |
| reading_timestamp | TIMESTAMP | Yes | Date and time of the sensor reading |
| temperature | DECIMAL(8,2) | Yes | Machine temperature measurement |
| vibration | DECIMAL(8,2) | Yes | Machine vibration measurement |
| pressure | DECIMAL(8,2) | Yes | Machine pressure measurement |
| rotation_speed | DECIMAL(10,2) | Yes | Machine rotation speed |
| power_consumption | DECIMAL(10,2) | Yes | Machine power consumption |


## 6. Maintenance Record

| Field | Data Type | Required | Description |
|---|---|---|---|
| maintenance_record_id | INTEGER | Yes | Unique maintenance record identifier |
| machine_id | INTEGER | Yes | Machine receiving maintenance |
| maintenance_date | DATE | Yes | Date maintenance was performed |
| maintenance_type | VARCHAR(50) | Yes | Type of maintenance performed |
| maintenance_description | TEXT | No | Description of maintenance activity |
| technician | VARCHAR(100) | Yes | Technician responsible for maintenance |
| maintenance_duration | DECIMAL(10,2) | Yes | Duration of maintenance in minutes |
| maintenance_status | VARCHAR(30) | Yes | Current status of the maintenance activity |


## 7. Quality Record

| Field | Data Type | Required | Description |
|---|---|---|---|
| quality_record_id | INTEGER | Yes | Unique quality record identifier |
| production_record_id | INTEGER | Yes | Production record associated with the quality inspection |
| inspection_date | DATE | Yes | Date of quality inspection |
| total_units_inspected | INTEGER | Yes | Total number of units inspected |
| defective_units | INTEGER | Yes | Number of defective units identified |
| defect_rate | DECIMAL(5,2) | Yes | Percentage of inspected units that were defective |
| quality_status | VARCHAR(30) | Yes | Overall quality result |


## 8. Employee / User

| Field | Data Type | Required | Description |
|---|---|---|---|
| user_id | INTEGER | Yes | Unique user identifier |
| name | VARCHAR(100) | Yes | User's name |
| email | VARCHAR(150) | Yes | User's email address |
| role | VARCHAR(50) | Yes | User's assigned system role |
| account_status | VARCHAR(30) | Yes | Current account status |
| created_date | DATE | Yes | Date the user account was created |


## 9. Data Quality Issue

| Field | Data Type | Required | Description |
|---|---|---|---|
| issue_id | BIGINT | Yes | Unique data quality issue identifier |
| dataset | VARCHAR(100) | Yes | Dataset containing the data issue |
| record_identifier | VARCHAR(100) | Yes | Identifier of the affected record |
| issue_type | VARCHAR(50) | Yes | Type of data quality problem |
| issue_description | TEXT | Yes | Description of the detected issue |
| severity | VARCHAR(30) | Yes | Severity level of the issue |
| detected_date | TIMESTAMP | Yes | Date and time the issue was detected |
| resolution_status | VARCHAR(30) | Yes | Current resolution status |
| resolved_date | TIMESTAMP | No | Date and time the issue was resolved |


## 10. ML Prediction

| Field | Data Type | Required | Description |
|---|---|---|---|
| prediction_id | BIGINT | Yes | Unique prediction identifier |
| machine_id | INTEGER | Yes | Machine for which the prediction was generated |
| model_id | VARCHAR(100) | Yes | Identifier of the machine learning model |
| prediction_timestamp | TIMESTAMP | Yes | Date and time the prediction was generated |
| failure_probability | DECIMAL(6,5) | Yes | Predicted probability of machine failure |
| risk_level | VARCHAR(30) | Yes | Machine failure risk category |
| prediction_status | VARCHAR(30) | Yes | Status of the prediction |