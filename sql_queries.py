import streamlit as st
import mysql.connector
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="International Debt Analysis",
    page_icon="🌍",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🌍 International Debt Analysis System")

st.write(
    "SQL Query Analysis using MySQL and Streamlit"
)

st.divider()


# =========================================================
# MYSQL CONNECTION
# =========================================================

def create_connection():

    connection = mysql.connector.connect(

        host="localhost",

        port=3306,

        user="root",

        password="amalek",

        database="debt"

    )

    return connection


# =========================================================
# CHECK MYSQL CONNECTION
# =========================================================

try:

    connection = create_connection()

    st.sidebar.success("🟢 MySQL Connected")

    connection.close()

except Exception as e:

    st.sidebar.error("🔴 MySQL Connection Failed")

    st.sidebar.error(str(e))


# =========================================================
# SQL QUESTIONS
# =========================================================

sql_questions = {


# =========================================================
# BASIC QUESTIONS
# =========================================================

"1. Retrieve all distinct country names": """

SELECT DISTINCT `Country Name`

FROM IDS_ALLCountries_Data

ORDER BY `Country Name`;

""",


"2. Count the total number of countries": """

SELECT COUNT(DISTINCT `Country Code`) AS `Total Countries`

FROM IDS_ALLCountries_Data;

""",


"3. Find the total number of indicators": """

SELECT COUNT(DISTINCT `Series Code`) AS `Total Indicators`

FROM IDS_ALLCountries_Data;

""",


"4. Display the first 10 records": """

SELECT *

FROM IDS_ALLCountries_Data

LIMIT 10;

""",


"5. Calculate the total global debt": """

SELECT

    SUM(`Debt Value`) AS `Total Global Debt`

FROM IDS_ALLCountries_Data;

""",


"6. List all unique indicator names": """

SELECT DISTINCT

    `Series Code`,

    `Series Name`

FROM IDS_ALLCountries_Data

ORDER BY `Series Name`;

""",


"7. Find the number of records for each country": """

SELECT

    `Country Name`,

    COUNT(*) AS `Record Count`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

ORDER BY `Record Count` DESC;

""",


"8. Display records where debt is greater than 1 billion USD": """

SELECT *

FROM IDS_ALLCountries_Data

WHERE `Debt Value` > 1000000000

ORDER BY `Debt Value` DESC;

""",


"9. Find minimum, maximum and average debt": """

SELECT

    MIN(`Debt Value`) AS `Minimum Debt`,

    MAX(`Debt Value`) AS `Maximum Debt`,

    AVG(`Debt Value`) AS `Average Debt`

FROM IDS_ALLCountries_Data;

""",


"10. Count total number of records": """

SELECT

    COUNT(*) AS `Total Records`

FROM IDS_ALLCountries_Data;

""",


# =========================================================
# INTERMEDIATE QUESTIONS
# =========================================================

"11. Find total debt for each country": """

SELECT

    `Country Name`,

    SUM(`Debt Value`) AS `Total Debt`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

ORDER BY `Total Debt` DESC;

""",


"12. Display top 10 countries with highest total debt": """

SELECT

    `Country Name`,

    SUM(`Debt Value`) AS `Total Debt`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

ORDER BY `Total Debt` DESC

LIMIT 10;

""",


"13. Find average debt per country": """

SELECT

    `Country Name`,

    AVG(`Debt Value`) AS `Average Debt`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

ORDER BY `Average Debt` DESC;

""",


"14. Calculate total debt for each indicator": """

SELECT

    `Series Name`,

    SUM(`Debt Value`) AS `Total Debt`

FROM IDS_ALLCountries_Data

GROUP BY `Series Name`

ORDER BY `Total Debt` DESC;

""",


"15. Identify the indicator contributing the highest total debt": """

SELECT

    `Series Name`,

    SUM(`Debt Value`) AS `Total Debt`

FROM IDS_ALLCountries_Data

GROUP BY `Series Name`

ORDER BY `Total Debt` DESC

LIMIT 1;

""",


"16. Find the country with the lowest total debt": """

SELECT

    `Country Name`,

    SUM(`Debt Value`) AS `Total Debt`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

ORDER BY `Total Debt` ASC

LIMIT 1;

""",


"17. Calculate total debt for each country and indicator": """

SELECT

    `Country Name`,

    `Series Name`,

    SUM(`Debt Value`) AS `Total Debt`

FROM IDS_ALLCountries_Data

GROUP BY

    `Country Name`,

    `Series Name`

ORDER BY `Total Debt` DESC;

""",


"18. Count how many indicators each country has": """

SELECT

    `Country Name`,

    COUNT(DISTINCT `Series Code`) AS `Indicator Count`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

ORDER BY `Indicator Count` DESC;

""",


"19. Countries whose total debt is above global average": """

SELECT

    `Country Name`,

    SUM(`Debt Value`) AS `Total Debt`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

HAVING SUM(`Debt Value`) >

(

    SELECT AVG(`Country Total`)

    FROM

    (

        SELECT

            SUM(`Debt Value`) AS `Country Total`

        FROM IDS_ALLCountries_Data

        GROUP BY `Country Name`

    ) AS CountryTotals

)

ORDER BY `Total Debt` DESC;

""",


"20. Rank countries based on total debt": """

SELECT

    `Country Name`,

    SUM(`Debt Value`) AS `Total Debt`,

    RANK() OVER (

        ORDER BY SUM(`Debt Value`) DESC

    ) AS `Debt Rank`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

ORDER BY `Debt Rank`;

""",


# =========================================================
# ADVANCED QUESTIONS
# =========================================================

"21. Find top 5 indicators contributing most to global debt": """

SELECT

    `Series Name`,

    SUM(`Debt Value`) AS `Total Debt`

FROM IDS_ALLCountries_Data

GROUP BY `Series Name`

ORDER BY `Total Debt` DESC

LIMIT 5;

""",


"22. Calculate percentage contribution of each country": """

SELECT

    `Country Name`,

    SUM(`Debt Value`) AS `Country Debt`,

    ROUND(

        SUM(`Debt Value`) /

        (

            SELECT SUM(`Debt Value`)

            FROM IDS_ALLCountries_Data

        ) * 100,

        2

    ) AS `Percentage Contribution`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

ORDER BY `Percentage Contribution` DESC;

""",


"23. Find top 3 countries for each indicator": """

SELECT

    `Country Name`,

    `Series Name`,

    `Total Debt`,

    `Indicator Rank`

FROM

(

    SELECT

        `Country Name`,

        `Series Name`,

        SUM(`Debt Value`) AS `Total Debt`,

        RANK() OVER (

            PARTITION BY `Series Code`

            ORDER BY SUM(`Debt Value`) DESC

        ) AS `Indicator Rank`

    FROM IDS_ALLCountries_Data

    GROUP BY

        `Country Name`,

        `Series Code`,

        `Series Name`

) AS RankedData

WHERE `Indicator Rank` <= 3

ORDER BY

    `Series Name`,

    `Indicator Rank`;

""",


"24. Difference between maximum and minimum debt for each country": """

SELECT

    `Country Name`,

    MAX(`Debt Value`) AS `Maximum Debt`,

    MIN(`Debt Value`) AS `Minimum Debt`,

    MAX(`Debt Value`) - MIN(`Debt Value`) AS `Debt Difference`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

ORDER BY `Debt Difference` DESC;

""",


"25. Create a view for top 10 countries": """

CREATE OR REPLACE VIEW top_10_countries AS

SELECT

    `Country Name`,

    SUM(`Debt Value`) AS `Total Debt`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

ORDER BY `Total Debt` DESC

LIMIT 10;

""",


"26. Categorize countries into High, Medium and Low Debt": """

SELECT

    `Country Name`,

    SUM(`Debt Value`) AS `Total Debt`,

    CASE

        WHEN SUM(`Debt Value`) >= 100000000000

            THEN 'High Debt'

        WHEN SUM(`Debt Value`) >= 10000000000

            THEN 'Medium Debt'

        ELSE 'Low Debt'

    END AS `Debt Category`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

ORDER BY `Total Debt` DESC;

""",


"27. Calculate cumulative debt per country": """

SELECT

    `Country Name`,

    `Year`,

    SUM(`Debt Value`) AS `Yearly Debt`,

    SUM(SUM(`Debt Value`)) OVER (

        PARTITION BY `Country Name`

        ORDER BY `Year`

    ) AS `Cumulative Debt`

FROM IDS_ALLCountries_Data

GROUP BY

    `Country Name`,

    `Year`

ORDER BY

    `Country Name`,

    `Year`;

""",


"28. Indicators whose average debt is higher than overall average": """

SELECT

    `Series Name`,

    AVG(`Debt Value`) AS `Indicator Average`

FROM IDS_ALLCountries_Data

GROUP BY `Series Name`

HAVING AVG(`Debt Value`) >

(

    SELECT AVG(`Debt Value`)

    FROM IDS_ALLCountries_Data

)

ORDER BY `Indicator Average` DESC;

""",


"29. Countries contributing more than 5% of global debt": """

SELECT

    `Country Name`,

    SUM(`Debt Value`) AS `Total Debt`,

    ROUND(

        SUM(`Debt Value`) /

        (

            SELECT SUM(`Debt Value`)

            FROM IDS_ALLCountries_Data

        ) * 100,

        2

    ) AS `Percentage Contribution`

FROM IDS_ALLCountries_Data

GROUP BY `Country Name`

HAVING

    SUM(`Debt Value`) /

    (

        SELECT SUM(`Debt Value`)

        FROM IDS_ALLCountries_Data

    ) > 0.05

ORDER BY `Percentage Contribution` DESC;

""",


"30. Find the most dominant indicator for each country": """

SELECT

    `Country Name`,

    `Series Name`,

    `Total Debt`

FROM

(

    SELECT

        `Country Name`,

        `Series Name`,

        SUM(`Debt Value`) AS `Total Debt`,

        ROW_NUMBER() OVER (

            PARTITION BY `Country Name`

            ORDER BY SUM(`Debt Value`) DESC

        ) AS `Row Number`

    FROM IDS_ALLCountries_Data

    GROUP BY

        `Country Name`,

        `Series Name`

) AS RankedIndicators

WHERE `Row Number` = 1

ORDER BY `Total Debt` DESC;

"""

}


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("📊 SQL Analysis")


selected_question = st.sidebar.selectbox(

    "Select a SQL Question",

    list(sql_questions.keys())

)


# =========================================================
# DISPLAY SELECTED QUESTION
# =========================================================

st.subheader("Selected SQL Question")

st.info(selected_question)


# =========================================================
# GET SQL QUERY
# =========================================================

selected_query = sql_questions[selected_question]


# =========================================================
# SHOW SQL QUERY
# =========================================================

with st.expander("👁️ View SQL Query"):

    st.code(

        selected_query,

        language="sql"

    )


# =========================================================
# EXECUTE BUTTON
# =========================================================

if st.button(

    "▶ Execute Query",

    type="primary"

):

    try:

        # Create MySQL connection
        connection = create_connection()

        # Create cursor
        cursor = connection.cursor()

        # Execute selected SQL query
        cursor.execute(selected_query)


        # =================================================
        # HANDLE CREATE VIEW QUERY
        # =================================================

        if selected_query.strip().upper().startswith("CREATE"):

            connection.commit()

            st.success(

                "✅ SQL query executed successfully!"

            )

            st.info(

                "The view 'top_10_countries' has been created/updated."

            )


        # =================================================
        # HANDLE SELECT QUERIES
        # =================================================

        else:

            # Get column names
            columns = [

                column[0]

                for column in cursor.description

            ]


            # Get query results
            results = cursor.fetchall()


            # Convert result into DataFrame
            result_df = pd.DataFrame(

                results,

                columns=columns

            )


            # Show success message
            st.success(

                f"✅ Query executed successfully! "
                f"{len(result_df):,} rows returned."

            )


            # =================================================
            # DISPLAY RESULT
            # =================================================

            st.subheader("📋 Query Result")

            st.dataframe(

                result_df,

                use_container_width=True,

                height=500

            )


        # Close cursor
        cursor.close()

        # Close connection
        connection.close()


    except Exception as e:

        st.error(

            "❌ Error while executing SQL query"

        )

        st.code(str(e))