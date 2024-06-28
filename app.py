import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure GenAI key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    # Assuming response.text gives the generated text, adjust based on actual response structure
    return response[0].text if isinstance(response, list) else response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        rows = []
        st.error(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
    return rows

# Define your prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION. 

    For example:
    Example 1 - How many entries of records are present?, 
    the SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;
    
    Example 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this: SELECT * FROM STUDENT WHERE CLASS="Data Science"; 

    Do not include any backticks or the word 'sql' in the output.
    """
]

# Streamlit App
st.set_page_config(page_title="SQL Query Generator", layout="wide")
st.title("Gemini App to Retrieve SQL Data")

# Input and button
question = st.text_input("Ask a question related to the SQL database:", key="input")
submit = st.button("Generate SQL Query")

# If submit is clicked
if submit:
    with st.spinner("Generating SQL query..."):
        try:
            sql_query = get_gemini_response(question, prompt)
            st.subheader("Generated SQL Query:")
            st.code(sql_query, language="sql")
            
            response = read_sql_query(sql_query, "student.db")
            
            if response:
                st.subheader("Query Results:")
                st.dataframe(response)
            else:
                st.warning("No results found or an error occurred.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Additional styling and information
st.sidebar.title("About")
st.sidebar.info("""
    This app uses Google's Gemini Model to convert natural language questions into SQL queries.
    It then executes the queries on a local SQLite database named `student.db`.
    
    **Instructions:**
    1. Enter a question related to the `STUDENT` database.
    2. Click on "Generate SQL Query" to see the generated SQL query and its results.
    
    **Note:** Ensure the `student.db` SQLite database is available in the same directory.
""")

st.sidebar.title("Contact")
st.sidebar.info("""
    For any queries or support, contact us at: support@example.com
""")






