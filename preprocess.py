# DATA PREPROCESSING


import pandas as pd
import numpy as np
import os


# ============================================================
# 1. CREATE OUTPUT FOLDER
# ============================================================

output_folder = "cleaned_data"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("=" * 70)
print("INTERNATIONAL DEBT ANALYSIS - DATA PREPROCESSING")
print("=" * 70)


# ============================================================
# 2. LOAD ALL FIVE DATASETS
# ============================================================

print("\nLoading datasets...")

debt_df = pd.read_csv(
    "IDS_ALLCountries_Data.csv",
    encoding="latin1",
    low_memory=False
)

country_series_df = pd.read_csv(
    "Country-Series - Metadata.csv",
    encoding="latin1",
    low_memory=False
)

country_metadata_df = pd.read_csv(
    "IDS_CountryMetaData.csv",
    encoding="latin1",
    low_memory=False
)

footnote_df = pd.read_csv(
    "IDS_FootNoteMetaData.csv",
    encoding="latin1",
    low_memory=False
)

series_metadata_df = pd.read_csv(
    "IDS_SeriesMetaData.csv",
    encoding="latin1",
    low_memory=False
)

print("All datasets loaded successfully.")


# ============================================================
# 3. DISPLAY ORIGINAL DATASET INFORMATION
# ============================================================

datasets = {
    "Debt Data": debt_df,
    "Country-Series Metadata": country_series_df,
    "Country Metadata": country_metadata_df,
    "Footnote Metadata": footnote_df,
    "Series Metadata": series_metadata_df
}

print("\n" + "=" * 70)
print("ORIGINAL DATASET INFORMATION")
print("=" * 70)

for name, df in datasets.items():

    print("\n" + "-" * 60)
    print(name)

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nMissing values:")

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    if len(missing) > 0:
        print(missing.sort_values(ascending=False).head(10))
    else:
        print("No missing values.")


# ============================================================
# 4. CLEAN MAIN DEBT DATA
# ============================================================

print("\n" + "=" * 70)
print("CLEANING MAIN DEBT DATA")
print("=" * 70)


# Clean column names
debt_df.columns = (
    debt_df.columns
    .astype(str)
    .str.strip()
)


# Remove completely empty rows
before = len(debt_df)

debt_df = debt_df.dropna(how="all")

after = len(debt_df)

print(
    f"\nRemoved completely empty rows: "
    f"{before - after}"
)


# ============================================================
# 5. CLEAN TEXT COLUMNS
# ============================================================

text_columns = [
    "Country Name",
    "Country Code",
    "Counterpart-Area Name",
    "Counterpart-Area Code",
    "Series Name",
    "Series Code"
]

for column in text_columns:

    if column in debt_df.columns:

        debt_df[column] = (
            debt_df[column]
            .astype("string")
            .str.strip()
        )


# ============================================================
# 6. REMOVE ROWS WITH MISSING REQUIRED INFORMATION
# ============================================================

required_columns = [
    "Country Name",
    "Country Code",
    "Series Name",
    "Series Code"
]

before = len(debt_df)

debt_df = debt_df.dropna(
    subset=required_columns
)

after = len(debt_df)

print(
    f"Removed rows with missing required information: "
    f"{before - after}"
)


# ============================================================
# 7. VALIDATE COUNTRY CODE
# ============================================================

before = len(debt_df)

debt_df = debt_df[
    debt_df["Country Code"].str.len() == 3
]

after = len(debt_df)

print(
    f"Removed invalid country-code rows: "
    f"{before - after}"
)


# ============================================================
# 8. REMOVE DUPLICATES
# ============================================================

before = len(debt_df)

debt_df = debt_df.drop_duplicates()

after = len(debt_df)

print(
    f"Removed duplicate rows: "
    f"{before - after}"
)


# ============================================================
# 9. IDENTIFY YEAR COLUMNS
# ============================================================

year_columns = [
    column
    for column in debt_df.columns
    if str(column).isdigit()
]

print("\nYear columns identified:")

print(year_columns)

print(
    f"\nNumber of year columns: "
    f"{len(year_columns)}"
)


# ============================================================
# 10. CONVERT YEAR COLUMNS TO NUMERIC
# ============================================================

print("\nConverting year values to numeric...")

for column in year_columns:

    debt_df[column] = pd.to_numeric(
        debt_df[column],
        errors="coerce"
    )

print("Year conversion completed.")


# ============================================================
# 11. CHECK MISSING VALUES
# ============================================================

print("\nMissing values in year columns:")

missing_values = debt_df[year_columns].isnull().sum()

print(
    missing_values[
        missing_values > 0
    ].sort_values(
        ascending=False
    ).head(15)
)


# ============================================================
# 12. CHECK NEGATIVE VALUES
# ============================================================

print("\nChecking negative values...")

negative_values = {}

for column in year_columns:

    count = (
        debt_df[column] < 0
    ).sum()

    if count > 0:

        negative_values[column] = int(count)


if negative_values:

    print("Negative values found:")

    for year, count in negative_values.items():

        print(
            f"{year}: {count}"
        )

else:

    print("No negative values found.")


# NOTE:
# Negative values are NOT automatically removed because
# financial indicators may legitimately contain negative values.


# ============================================================
# 13. CONVERT WIDE DATA TO LONG FORMAT
# ============================================================

print("\n" + "=" * 70)
print("CONVERTING DEBT DATA TO LONG FORMAT")
print("=" * 70)


id_columns = [
    "Country Name",
    "Country Code",
    "Counterpart-Area Name",
    "Counterpart-Area Code",
    "Series Name",
    "Series Code"
]


debt_long = debt_df.melt(

    id_vars=id_columns,

    value_vars=year_columns,

    var_name="Year",

    value_name="Debt Value"

)


print(
    "\nRows after converting to long format:",
    len(debt_long)
)


# ============================================================
# 14. CONVERT YEAR AND DEBT VALUE
# ============================================================

debt_long["Year"] = pd.to_numeric(
    debt_long["Year"],
    errors="coerce"
).astype("Int64")


debt_long["Debt Value"] = pd.to_numeric(
    debt_long["Debt Value"],
    errors="coerce"
)


# ============================================================
# 15. REMOVE MISSING DEBT VALUES
# ============================================================

before = len(debt_long)

debt_long = debt_long.dropna(
    subset=["Debt Value"]
)

after = len(debt_long)

print(
    f"Removed rows with missing Debt Value: "
    f"{before - after}"
)


# ============================================================
# 16. REMOVE DUPLICATES AFTER TRANSFORMATION
# ============================================================

before = len(debt_long)

debt_long = debt_long.drop_duplicates()

after = len(debt_long)

print(
    f"Removed duplicate rows after transformation: "
    f"{before - after}"
)


# ============================================================
# 17. SORT DATA
# ============================================================

debt_long = debt_long.sort_values(

    by=[
        "Country Name",
        "Series Name",
        "Year"
    ]

)


# ============================================================
# 18. CLEAN COUNTRY-SERIES METADATA
# ============================================================

print("\n" + "=" * 70)
print("CLEANING COUNTRY-SERIES METADATA")
print("=" * 70)


country_series_df = (
    country_series_df
    .dropna(how="all")
    .drop_duplicates()
)


country_series_df.columns = (
    country_series_df.columns
    .astype(str)
    .str.strip()
)


for column in country_series_df.select_dtypes(
    include="object"
).columns:

    country_series_df[column] = (
        country_series_df[column]
        .astype("string")
        .str.strip()
    )


for column in [
    "Country Code",
    "Series Code"
]:

    if column in country_series_df.columns:

        country_series_df[column] = (
            country_series_df[column]
            .astype("string")
            .str.strip()
        )


# ============================================================
# 19. CLEAN COUNTRY METADATA
# ============================================================

print("\n" + "=" * 70)
print("CLEANING COUNTRY METADATA")
print("=" * 70)


country_metadata_df = (
    country_metadata_df
    .dropna(how="all")
    .drop_duplicates()
)


country_metadata_df.columns = (
    country_metadata_df.columns
    .astype(str)
    .str.strip()
)


for column in country_metadata_df.select_dtypes(
    include="object"
).columns:

    country_metadata_df[column] = (
        country_metadata_df[column]
        .astype("string")
        .str.strip()
    )


country_metadata_df["Code"] = (
    country_metadata_df["Code"]
    .astype("string")
    .str.strip()
)


# ============================================================
# 20. CLEAN FOOTNOTE METADATA
# ============================================================

print("\n" + "=" * 70)
print("CLEANING FOOTNOTE METADATA")
print("=" * 70)


footnote_df = (
    footnote_df
    .dropna(how="all")
    .drop_duplicates()
)


footnote_df.columns = (
    footnote_df.columns
    .astype(str)
    .str.strip()
)


for column in footnote_df.select_dtypes(
    include="object"
).columns:

    footnote_df[column] = (
        footnote_df[column]
        .astype("string")
        .str.strip()
    )


for column in [
    "Country Code",
    "Series Code",
    "Time Code"
]:

    if column in footnote_df.columns:

        footnote_df[column] = (
            footnote_df[column]
            .astype("string")
            .str.strip()
        )


# ============================================================
# 21. CLEAN SERIES METADATA
# ============================================================

print("\n" + "=" * 70)
print("CLEANING SERIES METADATA")
print("=" * 70)


series_metadata_df = (
    series_metadata_df
    .dropna(how="all")
    .drop_duplicates()
)


series_metadata_df.columns = (
    series_metadata_df.columns
    .astype(str)
    .str.strip()
)


for column in series_metadata_df.select_dtypes(
    include="object"
).columns:

    series_metadata_df[column] = (
        series_metadata_df[column]
        .astype("string")
        .str.strip()
    )


series_metadata_df["Code"] = (
    series_metadata_df["Code"]
    .astype("string")
    .str.strip()
)


# ============================================================
# 22. CLEAN EMPTY / NULL TEXT VALUES
# ============================================================

for df in [
    country_series_df,
    country_metadata_df,
    footnote_df,
    series_metadata_df
]:

    df.replace(

        [
            "",
            " ",
            "NA",
            "N/A",
            "NULL",
            "null"
        ],

        np.nan,

        inplace=True

    )


# ============================================================
# 23. CLEAN DEBT CODES
# ============================================================

debt_long["Country Code"] = (
    debt_long["Country Code"]
    .astype("string")
    .str.strip()
)


debt_long["Series Code"] = (
    debt_long["Series Code"]
    .astype("string")
    .str.strip()
)


# ============================================================
# 24. CHECK COUNTRY CODE MATCHING
# ============================================================

print("\n" + "=" * 70)
print("CHECKING COUNTRY CODE MATCHING")
print("=" * 70)


debt_country_codes = set(
    debt_long[
        "Country Code"
    ]
    .dropna()
    .unique()
)


metadata_country_codes = set(
    country_metadata_df[
        "Code"
    ]
    .dropna()
    .unique()
)


unmatched_country_codes = (
    debt_country_codes -
    metadata_country_codes
)


print(
    "Unique country codes in debt data:",
    len(debt_country_codes)
)


print(
    "Unique country codes in country metadata:",
    len(metadata_country_codes)
)


print(
    "Unmatched country codes:",
    len(unmatched_country_codes)
)


if unmatched_country_codes:

    print(
        sorted(unmatched_country_codes)
    )

else:

    print(
        "All country codes matched successfully."
    )


# ============================================================
# 25. CHECK SERIES CODE MATCHING
# ============================================================

print("\n" + "=" * 70)
print("CHECKING SERIES CODE MATCHING")
print("=" * 70)


debt_series_codes = set(
    debt_long[
        "Series Code"
    ]
    .dropna()
    .unique()
)


metadata_series_codes = set(
    series_metadata_df[
        "Code"
    ]
    .dropna()
    .unique()
)


unmatched_series_codes = (
    debt_series_codes -
    metadata_series_codes
)


print(
    "Unique series codes in debt data:",
    len(debt_series_codes)
)


print(
    "Unique series codes in series metadata:",
    len(metadata_series_codes)
)


print(
    "Unmatched series codes:",
    len(unmatched_series_codes)
)


if unmatched_series_codes:

    print(
        "Unmatched series codes:"
    )

    print(
        sorted(unmatched_series_codes)
    )

else:

    print(
        "All series codes matched successfully."
    )


# ============================================================
# 26. SAVE CLEANED DATASETS
# ============================================================

print("\n" + "=" * 70)
print("SAVING CLEANED DATASETS")
print("=" * 70)


debt_long.to_csv(

    f"{output_folder}/cleaned_debt_data.csv",

    index=False

)


country_series_df.to_csv(

    f"{output_folder}/cleaned_country_series_metadata.csv",

    index=False

)


country_metadata_df.to_csv(

    f"{output_folder}/cleaned_country_metadata.csv",

    index=False

)


footnote_df.to_csv(

    f"{output_folder}/cleaned_footnote_metadata.csv",

    index=False

)


series_metadata_df.to_csv(

    f"{output_folder}/cleaned_series_metadata.csv",

    index=False

)


print("\nFive cleaned files saved successfully!")


# ============================================================
# 27. FINAL DATASET SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL CLEANED DATASET SUMMARY")
print("=" * 70)


print(
    "\n1. cleaned_debt_data.csv"
)

print(
    "Rows:",
    len(debt_long)
)

print(
    "Columns:",
    len(debt_long.columns)
)


print(
    "\n2. cleaned_country_series_metadata.csv"
)

print(
    "Rows:",
    len(country_series_df)
)


print(
    "\n3. cleaned_country_metadata.csv"
)

print(
    "Rows:",
    len(country_metadata_df)
)


print(
    "\n4. cleaned_footnote_metadata.csv"
)

print(
    "Rows:",
    len(footnote_df)
)


print(
    "\n5. cleaned_series_metadata.csv"
)

print(
    "Rows:",
    len(series_metadata_df)
)


print("\n" + "=" * 70)

print(
    "PREPROCESSING COMPLETED SUCCESSFULLY!"
)

print("=" * 70)

print(
    f"\nCleaned files are available inside: "
    f"{output_folder}/"
)