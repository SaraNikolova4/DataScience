import pymysql
import pandas as pd

# Establish a connection to the MySQL database
connection = pymysql.connect(
    host='localhost',          # Host address of the MySQL server
    user='root',               # Username for the MySQL server
    password='Sara.0108',      # Password for the MySQL server
    database='vvnp'            # Name of the database to connect to
)

try:
    # Path to the first CSV file
    dataset_path_1 = r'C:\Users\Lenovo\Desktop\VVNP_F\src\main\java\com\example\vvnp_f\New_DataSet\model_tv.csv'
    # Read the CSV file into a DataFrame
    df1 = pd.read_csv(dataset_path_1)

    # Check if the required columns are in the DataFrame
    if 'From' in df1.columns and 'To' in df1.columns and 'Predicted_Points' in df1.columns:
        # Create a cursor object to execute SQL commands
        cursor = connection.cursor()
        # SQL query to create a table if it does not exist
        create_table_query_1 = """
        CREATE TABLE IF NOT EXISTS table1 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            `From` VARCHAR(255),
            `To` VARCHAR(255),
            Predicted_Points INT
        );
        """
        # Execute the SQL query to create the table
        cursor.execute(create_table_query_1)
        # Commit the changes to the database
        connection.commit()

        # Insert each row from the DataFrame into the table
        for _, row in df1.iterrows():
            insert_query_1 = """
            INSERT INTO table1 (`From`, `To`, `Predicted_Points`)
            VALUES (%s, %s, %s);
            """
            cursor.execute(insert_query_1, (row['From'], row['To'], row['Predicted_Points']))

        # Commit the changes to the database
        connection.commit()
        print("Yes data added in database for tv.")
    else:
        print("CSV is not good for added.")

    # Path to the second CSV file
    dataset_path_2 = r'C:\Users\Lenovo\Desktop\VVNP_F\src\main\java\com\example\vvnp_f\New_DataSet\model_ziri.csv'
    # Read the CSV file into a DataFrame
    df2 = pd.read_csv(dataset_path_2)

    # Check if the required columns are in the DataFrame
    if 'From' in df2.columns and 'To' in df2.columns and 'Predicted_Points' in df2.columns:
        # SQL query to create a table if it does not exist
        create_table_query_2 = """
        CREATE TABLE IF NOT EXISTS table2 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            `From` VARCHAR(255),
            `To` VARCHAR(255),
            Predicted_Points INT
        );
        """
        # Execute the SQL query to create the table
        cursor.execute(create_table_query_2)
        # Commit the changes to the database
        connection.commit()

        # Insert each row from the DataFrame into the table
        for _, row in df2.iterrows():
            insert_query_2 = """
            INSERT INTO table2 (`From`, `To`, `Predicted_Points`)
            VALUES (%s, %s, %s);
            """
            cursor.execute(insert_query_2, (row['From'], row['To'], row['Predicted_Points']))

        # Commit the changes to the database
        connection.commit()
        print("Yes data added in database for ziri.")
    else:
        print("CSV is not good for added.")

# Ensure that the connection is closed regardless of any errors
finally:
    connection.close()
