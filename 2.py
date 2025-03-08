import os
import pandas as pd
import psycopg2
import json
import time
from groq import Groq
import streamlit as st

# Set up Groq API key
groq_api_key = "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"
client = Groq(api_key=groq_api_key)

# Database connection setup
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="adobe_db",
            user="postgres",
            password="nitin9955",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        st.error(f"Database connection error: {e}")
        return None

# Function to fetch database schema
def fetch_database_schema():
    schema = {}
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
                columns = [col[0] for col in cursor.fetchall()]
                schema[table_name] = columns
        except psycopg2.Error as e:
            st.error(f"Error fetching schema: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        st.error("Failed to connect to the database.")
    return schema

# Function to load and preprocess training data from JSON files
def load_and_preprocess_data(generate_task_json, query_correction_json):
    try:
        with open(generate_task_json, 'r') as f:
            generate_task_data = json.load(f)
        with open(query_correction_json, 'r') as f:
            query_correction_data = json.load(f)
        
        generate_task_df = pd.DataFrame(generate_task_data).dropna()
        query_correction_df = pd.DataFrame(query_correction_data).dropna()
        
        return generate_task_df, query_correction_df
    except Exception as e:
        st.error(f"Error loading or preprocessing data: {e}")
        return None, None

# Function to call Groq API
def call_groq_api(prompt):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",  # Available model
                messages=[
                    {
                        "role": "user",
                        "content": prompt  # Use the prompt variable here
                    }
                ],
                max_tokens=100,
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error calling Groq API: {e}")
            time.sleep(2 ** attempt)
    return None

# Function to generate SQL from natural language
def generate_sql_from_nl(nl_query, schema, generate_task_data):
    schema_info = "\n".join([f"Table: {table} Columns: {', '.join(columns)}" for table, columns in schema.items()])
    examples = "\n".join([f"Natural Language: {row['NL']}\nSQL Query: {row['Query']}" for _, row in generate_task_data.sample(min(3, len(generate_task_data))).iterrows()])
    prompt = f"Given the following schema:\n{schema_info}\n\nHere are some examples:\n{examples}\n\nTranslate this to SQL (return only the SQL query, no additional text or explanations):\n{nl_query}"
    response = call_groq_api(prompt)
    
    if response:
        # Extract only the SQL query from the response
        sql_query = response.strip().split("```sql")[-1].split("```")[0].strip()
        return sql_query
    return None

# Function to correct SQL query
def correct_sql_query(incorrect_sql, schema, query_correction_data):
    schema_info = "\n".join([f"Table: {table} Columns: {', '.join(columns)}" for table, columns in schema.items()])
    
    # Ensure query_correction_data is not empty
    if query_correction_data.empty:
        st.error("No query correction data available.")
        return None
    
    examples = "\n".join([
        f"Incorrect SQL: {row['IncorrectQuery']}\nCorrected SQL: {row['CorrectQuery']}"
        for _, row in query_correction_data.sample(min(3, len(query_correction_data))).iterrows()
    ])
    
    prompt = f"Given the following schema:\n{schema_info}\n\nHere are some examples:\n{examples}\n\nCorrect this SQL query (return only the SQL query, no additional text or explanations):\n{incorrect_sql}"
    response = call_groq_api(prompt)
    
    if response:
        # Extract only the SQL query from the response
        sql_query = response.strip().split("```sql")[-1].split("```")[0].strip()
        return sql_query
    return None

# Streamlit UI
def main():
    st.title("AI-Powered SQL Query Generator and Corrector")
    
    # Load training data
    generate_task_json = "train_generate_task.json"
    query_correction_json = "train_query_correction_task.json"
    generate_task_data, query_correction_data = load_and_preprocess_data(generate_task_json, query_correction_json)
    
    # Fetch database schema
    schema = fetch_database_schema()
    
    # Natural Language to SQL
    st.header("Natural Language to SQL")
    nl_query = st.text_area("Enter your natural language query:")
    if st.button("Generate SQL"):
        generated_sql = generate_sql_from_nl(nl_query, schema, generate_task_data)
        st.code(generated_sql, language="sql")
    
    # SQL Query Correction
    st.header("SQL Query Correction")
    incorrect_sql = st.text_area("Enter the incorrect SQL query:")
    if st.button("Correct SQL"):
        corrected_sql = correct_sql_query(incorrect_sql, schema, query_correction_data)
        st.code(corrected_sql, language="sql")

if __name__ == "__main__":
    main()