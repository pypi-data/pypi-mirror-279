import os
import psycopg2
from psycopg2 import sql

def store_file(db_config, file_path, model_name, model_description):
    # Read file data
    with open(file_path, 'rb') as file:
        file_data = file.read()
    
    # Extract file extension
    file_extension = os.path.splitext(file_path)[1]

    # Connect to the database and store the file
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    query = sql.SQL("""
    INSERT INTO models (name, description, file_extension, file_data)
    VALUES (%s, %s, %s, %s)
    """)
    cursor.execute(query, (model_name, model_description, file_extension, psycopg2.Binary(file_data)))
    connection.commit()
    cursor.close()
    connection.close()

def push_model(file_path, model_name, model_description, db_config):
    store_file(db_config, file_path, model_name, model_description)
