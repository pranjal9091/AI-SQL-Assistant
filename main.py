from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

app = FastAPI(title="AI SQL Assistant API")

# Database Configuration
db_uri = "mysql+mysqlconnector://root:mahaveernagar1st@localhost:3306/Chinook"
db = SQLDatabase.from_uri(db_uri)

# Models
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
    temperature=0.1
)
model = ChatHuggingFace(llm=llm)

# Helper Functions
def get_schema(_):
    return db.get_table_info()

def run_query(query):
    try:
        res = db.run(query)
        if not res:
            return "No data found for this query."
        return res
    except Exception as e:
        return f"SQL Execution Error: {str(e)}"

def clean_sql(text):
    return text.split("```sql")[-1].split("```")[0].strip()

def is_safe_query(query: str) -> bool:
    forbidden_words = ["DROP", "DELETE", "TRUNCATE", "ALTER", "UPDATE"]
    return not any(word in query.upper() for word in forbidden_words)


# Chains
sql_prompt = ChatPromptTemplate.from_template("Write ONLY SQL for: {question}\nSchema: {schema}\nSQL Query:")
sql_chain = (RunnablePassthrough.assign(schema=get_schema) | sql_prompt | model | StrOutputParser())

final_prompt = ChatPromptTemplate.from_template("Answer question: {question} using SQL Result: {response}\nFinal Answer:")

# API Schema
class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_db(request: QueryRequest):
    try:
        # 1. Generate SQL
        raw_sql = sql_chain.invoke({"question": request.question})
        sql_query = clean_sql(raw_sql)
        
        # 2. Execute SQL
        db_res = run_query(sql_query)
        
        # 3. Final Natural Language Answer
        full_chain = (final_prompt | model | StrOutputParser())
        final_ans = full_chain.invoke({
            "question": request.question,
            "response": db_res
        })
        
        return {
            "status": "success",
            "question": request.question,
            "generated_sql": sql_query,
            "answer": final_ans
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "AI SQL API is running"}