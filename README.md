# DBLINX

## Overview
This repository contains a collection of scripts and tools for managing employee data, sales data, and mobile plans. The scripts are written in Python and utilize various libraries such as pandas, numpy, and sqlalchemy.

## Structure
The repository is organized into the following directories:

- src: Contains the source code for the scripts and tools.
- sql: Contains the SQL scripts for creating the database tables.
- json: Contains the JSON files used for configuration and data storage.

## Scripts
**Employee**
The `EmployeeDownload` script is used to download employee data from a web portal. It uses selenium to navigate the website and download the data as a CSV file.
The `EmployeeUpsert` script is used to upsert employee data into the database. It reads the employee data from a CSV file and uses sqlalchemy to insert or update the data in the database.

**Sales**
The `SalesDownload` script is used to download sales data from a web portal. It uses selenium to navigate the website and download the data as a CSV file.
The `SalesUpsert` script is used to upsert sales data into the database. It reads the sales data from a CSV file and uses sqlalchemy to insert or update the data in the database.

**Mobile Plans**
The `MobilePlansDownload` script is used to download mobile plans data from a web portal. It uses selenium to navigate the website and download the data as a xlsx file.
The `MobilePlansUpsert` script is used to upsert mobile plans data into the database. It reads the mobile plans data from a xlsx file and uses sqlalchemy to insert or update the data in the database.

**Insurance**
The `InsuranceDownload` script is used to download insurance data from a web portal. It uses selenium to navigate the website and download the data as a xls (html table) file.
The `InsuranceUpsert` script is used to upsert insurance data into the database. It reads the insurance data from a xls (html table) file and uses sqlalchemy to insert or update the data in the database.

## Database
The database schema is defined in the sql/Create Tables.sql file. The database contains the following tables:

**employees**: Stores employee data.
**sales**: Stores sales data.
**customers**: Customers emploee data
**mobile_plans**: Stores mobile plans data.

## Configuration
The scripts use configuration files in the json directory to store settings and data. The configuration files are:

columns.json: Defines the column mappings for the sales and employees data.
phoen_numbers.json: Stores the phone numbers used for sending notifications.

Requirements
- Python 3.8+
- pandas
- numpy
- sqlalchemy
- selenium
- requests

### Usage
To use the scripts, run app.py

### License
This repository is licensed under the MIT License. See the LICENSE file for details