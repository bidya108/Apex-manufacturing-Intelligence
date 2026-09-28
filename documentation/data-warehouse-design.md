# Apex Manufacturing Data Warehouse Design

## 1. Purpose

The Apex Manufacturing Data Warehouse is designed to support analytical reporting, business intelligence, dashboards, machine learning preparation, and management decision-making.

The warehouse separates analytical workloads from the operational PostgreSQL database.

## 2. Architecture

Operational Database
        |
        v
Data Extraction / ETL
        |
        v
Data Warehouse
        |
        +---- SQL Analytics
        |
        +---- Dashboards
        |
        +---- Machine Learning
        |
        +---- Reports

## 3. Schema Design

The warehouse follows a Star Schema.

### Fact Tables

#### fact_production

Stores production activity and production performance measurements.

Measures:
- production_target
- actual_production
- production_efficiency
- downtime_duration

Foreign Keys:
- date_key
- facility_key
- production_line_key
- machine_key

#### fact_machine_sensor

Stores machine sensor measurements.

Measures:
- temperature
- vibration
- pressure
- rotation_speed
- power_consumption

Foreign Keys:
- date_key
- machine_key

#### fact_maintenance

Stores maintenance activities.

Measures:
- maintenance_duration

Foreign Keys:
- date_key
- machine_key

#### fact_quality

Stores production quality measurements.

Measures:
- total_units_inspected
- defective_units
- defect_rate

Foreign Keys:
- date_key
- production_line_key

## 4. Dimension Tables

### dim_date

Stores calendar information.

Attributes:
- date_key
- full_date
- year
- quarter
- month
- month_name
- day
- day_of_week

### dim_facility

Stores manufacturing facility information.

Attributes:
- facility_key
- facility_id
- facility_name
- location
- facility_status

### dim_production_line

Stores production line information.

Attributes:
- production_line_key
- production_line_id
- production_line_name
- production_line_status
- production_capacity
- facility_key

### dim_machine

Stores machine information.

Attributes:
- machine_key
- machine_id
- machine_name
- machine_type
- manufacturer
- operating_status
- production_line_key

## 5. Benefits

The warehouse provides:

- Faster analytical queries
- Separation of operational and analytical workloads
- Centralized reporting data
- Easier dashboard development
- Consistent business metrics
- Historical analysis
- Machine learning data preparation
- Scalable analytical architecture

## 6. Data Flow

Operational tables provide the source data.

ETL processes will:

1. Extract operational data.
2. Validate incoming data.
3. Transform data into analytical structures.
4. Load dimension tables.
5. Load fact tables.
6. Validate warehouse data.

## 7. Future Extensions

The warehouse can later be extended with:

- Machine failure facts
- ML prediction facts
- Employee dimensions
- Maintenance technician dimensions
- Supplier dimensions
- Product dimensions
- Slowly Changing Dimensions
- Historical machine status tracking
