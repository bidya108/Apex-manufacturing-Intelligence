# Entity Relationships

## 1. Facility → Production Line

Relationship: One-to-Many

One facility can contain multiple production lines.

Each production line belongs to one facility.

Foreign Key:

- production_line.facility_id
- References facility.facility_id


## 2. Production Line → Machine

Relationship: One-to-Many

One production line can contain multiple machines.

Each machine belongs to one production line.

Foreign Key:

- machine.production_line_id
- References production_line.production_line_id


## 3. Production Line → Production Record

Relationship: One-to-Many

One production line can have many production records.

Each production record belongs to one production line.

Foreign Key:

- production_record.production_line_id
- References production_line.production_line_id


## 4. Machine → Sensor Reading

Relationship: One-to-Many

One machine can generate many sensor readings.

Each sensor reading belongs to one machine.

Foreign Key:

- machine_sensor_reading.machine_id
- References machine.machine_id


## 5. Machine → Maintenance Record

Relationship: One-to-Many

One machine can have many maintenance records.

Each maintenance record belongs to one machine.

Foreign Key:

- maintenance_record.machine_id
- References machine.machine_id


## 6. Machine → ML Prediction

Relationship: One-to-Many

One machine can have many machine learning predictions over time.

Each prediction belongs to one machine.

Foreign Key:

- ml_prediction.machine_id
- References machine.machine_id


## 7. Production Record → Quality Record

Relationship: One-to-Many

One production record can have one or more quality inspection records.

Each quality record belongs to a production record.

Foreign Key:

- quality_record.production_record_id
- References production_record.production_record_id


## 8. Employee / User

Users are responsible for accessing the platform according to their assigned roles.

Users will later be connected to:

- Authentication
- Authorization
- Audit logs
- System activities


## 9. Data Quality Issue

Data quality issues are associated with datasets and affected records.

The entity will later be connected to:

- Data validation
- ETL pipelines
- Data quality monitoring
- Data administration