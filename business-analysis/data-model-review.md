# Data Model Review and Normalization

## 1. Purpose

The database model is designed to minimize unnecessary data duplication, maintain data integrity, and support reliable analytical processing.

The model separates major manufacturing entities into independent tables connected through primary and foreign keys.


## 2. Normalization Approach

The initial database design follows the principles of relational database normalization.

The design primarily targets Third Normal Form (3NF).

### First Normal Form (1NF)

Each table should contain atomic values.

Example:

Incorrect:

| machine_id | sensor_values |
|---|---|
| 101 | 72.4, 3.2, 1010 |

Correct:

| machine_id | temperature | vibration | pressure |
|---|---:|---:|---:|
| 101 | 72.4 | 3.2 | 1010 |

Each field contains one logical value.


### Second Normal Form (2NF)

Non-key attributes should depend on the complete primary key.

The project uses appropriate primary keys so that attributes belong to the entity represented by the record.


### Third Normal Form (3NF)

Non-key attributes should depend on the primary key and not on another non-key attribute.

For example, facility information should not be repeatedly stored inside every machine record.

Instead:

Facility:

- facility_id
- facility_name
- location

Machine:

- machine_id
- production_line_id
- machine_name

The machine references the production line, and the production line references the facility.


## 3. Data Duplication Prevention

The model separates:

- Facility information
- Production line information
- Machine information
- Production records
- Sensor readings
- Maintenance records
- Quality records
- ML predictions

This prevents repeated storage of the same facility, machine, or production information across multiple datasets.


## 4. Referential Integrity

Foreign keys shall be used to maintain valid relationships between tables.

Examples:

- production_line.facility_id → facility.facility_id
- machine.production_line_id → production_line.production_line_id
- production_record.production_line_id → production_line.production_line_id
- machine_sensor_reading.machine_id → machine.machine_id
- maintenance_record.machine_id → machine.machine_id
- ml_prediction.machine_id → machine.machine_id
- quality_record.production_record_id → production_record.production_record_id


## 5. Historical Data

Sensor readings, maintenance records, production records, quality records, and ML predictions are stored as historical records rather than overwriting previous information.

This allows:

- Trend analysis
- Historical reporting
- Predictive modeling
- Maintenance analysis
- Auditing


## 6. Data Integrity Rules

The database should enforce appropriate constraints.

Examples:

- Primary keys must be unique.
- Required fields should not contain NULL values.
- Foreign keys must reference valid records.
- Production quantities should not be negative.
- Defective units should not exceed inspected units.
- Failure probability should remain between 0 and 1.
- Dates and timestamps should use valid formats.


## 7. Expected Benefits

The normalized design provides:

- Reduced data duplication
- Better data consistency
- Easier maintenance
- Improved data quality
- Reliable relationships between entities
- Better support for analytics
- Better support for ETL pipelines
- Better support for machine learning