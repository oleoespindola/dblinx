# DBLINX

## Overview

This project is a data downloading and upserting tool, built using Python and Selenium. It provides a framework for downloading data from various sources, including LINX and SAV, and upserting it into a database.

## Requirements

    - Python 3.8+
    - Selenium
    - requests
    - mysql
    - mysql-connector
    - sqlalchemy
    - pandas
    - lxml
    - openpyxl
    - PyMySQL

## Installation

01. Clone the repository
02. Install dependencies: `pip install -r requirements.txt`
03. Set environment variables:
    - linx_user
    - linx_password
    - sav_user
    - sav_password
    - telegram_token
    - chat_id

## Usage

Run the script: `python app.py`

The script will download data from LINX and SAV, and upsert it into the database.

## Configuration

app.py: Configure **timeout** and **download time**.

## Classes and Functions

**BaseDownload**: Base class for downloading data from various sources.
**EmployeeDownload**, **MobilePlansDownload**, **InsuranceDownload**: Subclasses for downloading specific data from LINX and SAV.

**FILEHandler**: Class for handling file downloads and uploads.
**JSONHandler** (*json/columns.json*): Mapping of column names to database column names.
**Connection**: Returns a database engine connection string.

**Telegram**: Class for sending error messages to Telegram.

**General Upserts**: upserting all files into the database.

## Contributing

Contributions are welcome! Please submit a pull request with a clear description of the changes.

#### License

This project is licensed under the MIT License. See LICENSE for details.