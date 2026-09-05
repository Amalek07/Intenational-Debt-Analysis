CREATE TABLE IDS_CountryMetaData (
    `Code` VARCHAR(10) PRIMARY KEY,
    `Long Name` VARCHAR(200),
    `Income Group` VARCHAR(100),
    `Region` VARCHAR(150),
    `Lending category` VARCHAR(100),
    `Other groups` VARCHAR(200),
    `Currency Unit` VARCHAR(100),
    `Latest population census` VARCHAR(100),
    `Latest household survey` VARCHAR(100),
    `Special Notes` TEXT,
    `National accounts base year` VARCHAR(50),
    `National accounts reference year` VARCHAR(50),
    `System of National Accounts` VARCHAR(100),
    `SNA price valuation` VARCHAR(100),
    `PPP survey years` VARCHAR(100),
    `Balance of Payments Manual in use` VARCHAR(100),
    `External debt Reporting status` VARCHAR(150),
    `System of trade` VARCHAR(100),
    `Government Accounting concept` VARCHAR(150),
    `IMF data dissemination standard` VARCHAR(150),
    `Source of most recent Income and expenditure data` VARCHAR(200),
    `Vital registration complete` VARCHAR(100),
    `Latest agricultural census` VARCHAR(100),
    `Latest industrial data` VARCHAR(100),
    `Latest trade data` VARCHAR(100),
    `Latest water withdrawal data` VARCHAR(100),
    `2-alpha code` VARCHAR(10),
    `WB-2 code` VARCHAR(10),
    `Table Name` VARCHAR(100),
    `Short Name` VARCHAR(150)
);

#2. SERIES METADATA

CREATE TABLE IDS_SeriesMetaData (
    `Code` VARCHAR(50) PRIMARY KEY,
    `License Type` VARCHAR(100),
    `Indicator Name` VARCHAR(500),
    `Short definition` TEXT,
    `Long definition` TEXT,
    `Source` VARCHAR(300),
    `Topic` VARCHAR(200),
    `Dataset` VARCHAR(200),
    `Periodicity` VARCHAR(100),
    `Aggregation method` VARCHAR(200),
    `Limitations and exceptions` TEXT,
    `General comments` TEXT
);


# 3. DEBT DATA

CREATE TABLE IDS_ALLCountries_Data (
    `Debt ID` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `Country Name` VARCHAR(150),
    `Country Code` VARCHAR(10),
    `Counterpart-Area Name` VARCHAR(150),
    `Counterpart-Area Code` VARCHAR(10),
    `Series Name` VARCHAR(500),
    `Series Code` VARCHAR(50),
    `Year` INT,
    `Debt Value` DOUBLE,

    FOREIGN KEY (`Country Code`)
        REFERENCES IDS_CountryMetaData(`Code`),

    FOREIGN KEY (`Series Code`)
        REFERENCES IDS_SeriesMetaData(`Code`)
);



# 4. COUNTRY-SERIES METADATA


CREATE TABLE `Country-Series - Metadata` (
    `Type` VARCHAR(100),
    `Country Code` VARCHAR(10),
    `Series Code` VARCHAR(50),
    `Description` TEXT
);



# 5. FOOTNOTE METADATA


CREATE TABLE IDS_FootNoteMetaData (
    `Footnote ID` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `Type` VARCHAR(100),
    `Country Code` VARCHAR(10),
    `Series Code` VARCHAR(50),
    `Time Code` VARCHAR(20),
    `Description` TEXT
);