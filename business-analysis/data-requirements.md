# Data Requirements

## 1. Facility

The system shall maintain information about each manufacturing facility.

Required information:

- Facility ID
- Facility name
- Location
- Facility status
- Created date


## 2. Production Line

The system shall maintain information about production lines within each facility.

Required information:

- Production Line ID
- Facility ID
- Production Line name
- Production Line status
- Production capacity
- Created date


## 3. Machine

The system shall maintain information about machines operating within production lines.

Required information:

- Machine ID
- Production Line ID
- Machine name
- Machine type
- Manufacturer
- Installation date
- Operating status
- Last maintenance date


## 4. Production Record

The system shall maintain production activity records.

Required information:

- Production Record ID
- Production Line ID
- Production date
- Production target
- Actual production
- Production efficiency
- Downtime duration
- Shift


## 5. Machine Sensor Reading

The system shall maintain historical machine sensor measurements.

Required information:

- Sensor Reading ID
- Machine ID
- Timestamp
- Temperature
- Vibration
- Pressure
- Rotation speed
- Power consumption


## 6. Maintenance Record

The system shall maintain historical maintenance activity.

Required information:

- Maintenance Record ID
- Machine ID
- Maintenance date
- Maintenance type
- Maintenance description
- Technician
- Maintenance duration
- Maintenance status


## 7. Quality Record

The system shall maintain production quality information.

Required information:

- Quality Record ID
- Production Record ID
- Inspection date
- Total units inspected
- Defective units
- Defect rate
- Quality status


## 8. Employee / User

The system shall maintain information required to identify authorized system users.

Required information:

- User ID
- Name
- Email
- Role
- Account status
- Created date


## 9. Data Quality Issue

The system shall maintain information about data quality problems.

Required information:

- Issue ID
- Dataset
- Record identifier
- Issue type
- Issue description
- Severity
- Detected date
- Resolution status
- Resolved date


## 10. ML Prediction

The system shall maintain machine learning prediction results.

Required information:

- Prediction ID
- Machine ID
- Model ID
- Prediction timestamp
- Failure probability
- Risk level
- Prediction status