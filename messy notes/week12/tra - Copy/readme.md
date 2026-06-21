# TRA Oman Telecom Analytics Pipeline

## Overview

This project implements a complete ETL pipeline using Prefect, SQLite, and Docker.

The pipeline processes labor force statistics from the Telecommunications Regulatory Authority (TRA) Oman and loads analytics-ready data into a structured database.

## Dataset

Source: Telecommunications Regulatory Authority (TRA) Oman

Dataset used:

Labor force in the Telecom Sector

Excel file location:

data/raw/Labor force in the Telecom Sector-2.xlsx

Sheet used:

التوظيف

## Architecture

Extract → Transform → Load

### Extract

* Read Excel dataset
* Validate file existence
* Log record count

### Transform

* Clean data
* Standardize column names
* Create derived metrics:

  * employee_growth_rate
  * omanization_rate
  * expat_ratio

### Load

Load data into SQLite database:

* raw_telecom_data
* telecom_analytics

## Technologies

* Python
* Pandas
* Prefect
* SQLite
* Docker

## Running Locally

Install dependencies:

pip install -r requirements.txt

Run:

python flows/telecom_flow.py

## Running with Docker

Build and run:

docker compose up --build

## Output

Database:

db/telecom.db

Processed CSV:

data/processed/telecom_analytics.csv

## Business Insight

The telecom workforce generally increased over the years.

A high Omanization rate indicates strong localization efforts and investment in developing national telecom talent.

Growth in telecom employment is likely driven by broadband expansion, digital transformation initiatives, and increasing demand for telecommunications services in Oman.
