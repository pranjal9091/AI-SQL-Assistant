# 🤖 AI-Powered SQL Assistant

An end-to-end Natural Language to SQL interface that allows users to interact with MySQL databases using plain English. This project utilizes **Mistral-7B** and **LangChain** to bridge the gap between non-technical users and relational data.

---

## 🌟 Overview
As a student at the **Indian Institute of Information Technology (IIIT) Ranchi**, I developed this project to explore the intersection of Generative AI and database management. Building on my experience with open-source contributions like **Tenstorrent/tt-metal**, this tool focuses on high-accuracy query generation and real-time data interaction.

## 🚀 Features
* **Dual Interface**: Streamlit-based web dashboard for users and FastAPI backend for developer integration.
* **Few-Shot Prompting**: Enhanced SQL accuracy using context-aware examples for complex joins and aggregations.
* **Contextual Schema Injection**: Automatically fetches and injects database metadata into the LLM prompt for real-time accuracy.
* **Secure Execution**: Integrated validation layers to ensure safe SQL execution.

## 🛠️ Tech Stack
* **LLM**: Mistral-7B-Instruct-v0.2 (via HuggingFace Endpoint)
* **Orchestration**: LangChain (LCEL)
* **Database**: MySQL (Chinook Database)
* **API Framework**: FastAPI
* **Frontend**: Streamlit
* **Languages**: Python (Competitive Programming background helped in optimizing the logic)

## 📂 Project Structure
```plaintext
chat_with_mysql/
├── app.py              # Streamlit Frontend
├── main.py             # FastAPI Backend
├── .env                # API Keys & DB Credentials
├── requirements.txt    # Project Dependencies
└── README.md           # Documentation

⚙️ Installation & Setup
1. Clone the Repo
git clone [https://github.com/pranjal9091/AI-SQL-Assistant.git](https://github.com/pranjal9091/AI-SQL-Assistant.git)
cd chat_with_mysql

2. Activate Environment
source chat_with_mysql/bin/activate

3. Install Requirements
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the root directory:
HUGGINGFACEHUB_API_TOKEN=your_token_here

🏃 Running the Project
Web Dashboard (Streamlit)
streamlit run app.py

REST API (FastAPI)
uvicorn main:app --reload

Note: Check the interactive API docs at http://127.0.0.1:8000/docs.

👨‍💻 About Me
I am Pranjal Singh, a student at IIIT Ranchi with a strong interest in AI/ML research, competitive programming, and open-source software. I enjoy building tools that solve real-world data accessibility problems.
