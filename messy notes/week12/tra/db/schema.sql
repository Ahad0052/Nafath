CREATE TABLE raw_telecom_data (
    year INTEGER,
    total_employees INTEGER,
    omani_employees INTEGER,
    expat_employees INTEGER,
    tra_total INTEGER,
    tra_omani INTEGER,
    tra_expat INTEGER
);

CREATE TABLE telecom_analytics (
    year INTEGER,
    total_employees INTEGER,
    omani_employees INTEGER,
    expat_employees INTEGER,
    tra_total INTEGER,
    tra_omani INTEGER,
    tra_expat INTEGER,
    employee_growth_rate REAL,
    omanization_rate REAL,
    expat_ratio REAL
);