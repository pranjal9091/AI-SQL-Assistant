import streamlit as st
from dotenv import load_dotenv
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

# Configuration
st.set_page_config(page_title="SQL Chat AI", page_icon="🤖")
st.title("💾 Database Interaction Interface")

load_dotenv()

# Database Connection
db_uri = "mysql+mysqlconnector://root:mahaveernagar1st@localhost:3306/Chinook"
db = SQLDatabase.from_uri(db_uri)

def get_schema(_):
    return db.get_table_info()

def run_query(query):
    try:
        return db.run(query)
    except Exception as e:
        return f"Error: {str(e)}"

# Model Initialization
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    temperature=0.1
)
model = ChatHuggingFace(llm=llm)

# SQL Generation Chain
sql_template = """
You are a SQL expert. 

Example 1: "How many artists?" -> SELECT COUNT(*) FROM Artist;
Example 2: "List all albums by the artist AC/DC" -> SELECT Album.Title FROM Album JOIN Artist ON Album.ArtistId = Artist.ArtistId WHERE Artist.Name = 'AC/DC';
Example 3: "Who are the top 5 artists with most tracks?" -> SELECT Artist.Name FROM Artist JOIN Album ON Artist.ArtistId = Album.ArtistId JOIN Track ON Album.AlbumId = Track.AlbumId GROUP BY Artist.Name ORDER BY COUNT(Track.TrackId) DESC LIMIT 5;

Context: {schema}
Question: {question}
SQL Query:"""

sql_prompt = ChatPromptTemplate.from_template(sql_template)
sql_prompt = ChatPromptTemplate.from_template(sql_template)

sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | sql_prompt
    | model
    | StrOutputParser()
)

# Natural Language Response Chain
final_template = """
You are a database reporting assistant. 
Based on the SQL Result provided below, give a direct answer to the user's question.
If the SQL Result contains data, simply state the findings. 
Do NOT analyze the SQL query or suggest subqueries.

Question: {question}
SQL Result: {response}

Final Answer:"""
final_prompt = ChatPromptTemplate.from_template(final_template)

def clean_sql(text):
    return text.split("```sql")[-1].split("```")[0].strip()

# User Interface
question = st.text_input("Enter your query (e.g., Who are the top 5 artists?):")

if st.button("Execute") and question:
    with st.spinner("Analyzing..."):
        # Process SQL Generation
        generated_sql_raw = sql_chain.invoke({"question": question})
        sql_query = clean_sql(generated_sql_raw)
        
        # Execute Query on MySQL
        db_res = run_query(sql_query)
        
        # Generate Final Answer
        full_chain = (
            final_prompt 
            | model 
            | StrOutputParser()
        )
        
        final_ans = full_chain.invoke({
            "question": question,
            "query": sql_query,
            "response": db_res
        })
        
        # UI Output
        st.success("Execution Complete")
        st.subheader("Generated SQL Query")
        st.code(sql_query, language='sql')
        st.subheader("Final Answer")
        st.info(final_ans)