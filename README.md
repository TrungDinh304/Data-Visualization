# Data-Visualization
## Project Structure
```
├── Final_Semester_project/          
│   ├── Dashboard/           
│   ├── Data/           
│   ├── Slide/             
├── Middle_Semester_project/           
│   ├── Dashboard/           
│   ├── AI Integration/          
│   ├── Report/            
└── README.md             
```
## Mid Semester project
### Data source
- https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset
### Dashboard
- Diabetes data dashboard (https://public.tableau.com/app/profile/tr.c.quan.h.a.nh.m.18/viz/Book1_17303573383040/Dashboard1)
## Final Semester project
### Data source
- https://www.kaggle.com/datasets/vanviethieuanh/vietnam-weather-data
## Technical Requirements
### Prerequisites
- Python3
- Python libries: streamlit, pandas, base64, altair, pg8000, dotenv, os, google.generativeai.
- PostgeSQL.
### Setup Instructions
- Run create schema script
```
-- Table: public.weather_data

-- DROP TABLE IF EXISTS public.weather_data;

CREATE DATABASE weather
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
    
CREATE TABLE IF NOT EXISTS public.weather_data
(
    province character varying(255) COLLATE pg_catalog."default",
    max double precision,
    min double precision,
    wind double precision,
    wind_d character varying(50) COLLATE pg_catalog."default",
    rain double precision,
    humidi double precision,
    cloud double precision,
    pressure double precision,
    date date,
    year integer,
    month integer,
    is_outlier boolean,
    region character varying(255) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.weather_data
    OWNER to postgres;
```
- Import data source
```
-- Use the following statement to import cleaned data at ./AI Integration/AI
COPY your_table_name (column1, column2, ...)
FROM '/absolute/path/to/your_file.csv'
DELIMITER ','
CSV HEADER;
```
### Run streamlit application
```cmd
streamlit run streamlit_app.py
```

## Features and Analysis
- Diabetes Data Dashboard
- Weather In VietNam Data Dashboard
- Supported query chatbox.
- Supported external visualizatioin requirements chatbox.
## Project Timeline
### Middle Semester Project
- Project Start: October 22, 2024
- Final Submission: November 5, 2024
### Final Semester Project
- Project Start: December 20, 2024
- Final Submission: January 18, 2024

## References
1. [Behavioral Risk Factor Surveillance System](https://www.cdc.gov/brfss/annual_data/2015/pdf/codebook15_llcp.pdf)
2. [Diabetes Health Indicators Dataset](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset)


## License
This project is created for educational purposes as part of the CSC10108 - Data Visualization course at University of Science - VNUHCM.



