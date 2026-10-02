# Apex Manufacturing Intelligence & Predictive Operations Platform

An end-to-end manufacturing intelligence platform combining data engineering, analytics, machine learning, REST APIs, security, and an interactive dashboard.

## What It Does

- Centralized manufacturing data management
- Automated data validation and ETL pipelines
- PostgreSQL operational database and data warehouse
- Production, quality, downtime, and machine analytics
- Predictive maintenance risk analysis
- FastAPI REST APIs
- JWT authentication and role-based access control
- React dashboard with role-aware features
- Audit logging and data-quality monitoring

## Machine Learning

A Random Forest model is used to identify machines with elevated maintenance risk.

**Performance**

| Metric | Score |
|---|---:|
| Accuracy | 89.45% |
| Precision | 84.32% |
| Recall | 93.87% |
| F1 Score | 88.84% |

The synthetic dataset contains 7,300 sensor readings and predictions across 20 machines.

## Tech Stack

**Python · PostgreSQL · FastAPI · React · Pandas · Scikit-learn · JWT · Git**

## Project Structure

```text
business-analysis/   → Requirements & business analysis
database/             → PostgreSQL schemas
pipelines/            → ETL & validation
analytics/            → SQL analytics
machine-learning/    → ML training & prediction
api/                  → FastAPI backend
dashboard/             → React dashboard
tests/                → Validation & testing
Security
JWT authentication
Role-based access control
Password hashing
API audit logging
Environment-based secrets
Running the Project
pip install -r requirements.txt
uvicorn api.main:app --reload

Then start the dashboard:

cd dashboard
npm install
npm run dev
Status

Core platform completed with database, pipelines, analytics, machine learning, API, authentication, and dashboard components.

