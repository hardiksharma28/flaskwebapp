"""
Routes and views for the flask application.
"""

from flask import render_template, request
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import AzureOpenAI
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse
import os

# Set up SQLAlchemy connection string
conn_str = "DRIVER={SQL Server};SERVER=UC-DT21;DATABASE=Unify;Trusted_Connection=True"

# Create SQLAlchemy engine
quoted_conn_str = urllib.parse.quote_plus(conn_str)
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={quoted_conn_str}')

# Execute SQL query and fetch data into a DataFrame
query = 'SELECT * FROM Windows'
df = pd.read_sql(query, engine)


# Set up OpenAI environment variables
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_KEY"] = "ca54d9c9a14f4308b1f8da08fbcb5d44"
os.environ["OPENAI_API_BASE"] = "https://azureopenaichatbot123.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2022-12-01"

 


# Create an instance of AzureOpenAI language model

 

llm = AzureOpenAI(
    deployment_name="MyChatBotDeployment",
    model_name="text-davinci-003",
    openai_api_key="ca54d9c9a14f4308b1f8da08fbcb5d44",
    model_kwargs={
        "api_type": "azure",
        "api_version": "2022-12-01"
    }
)


# Create the agent
agent = create_pandas_dataframe_agent(llm, df)

def home():
    return render_template('index.html')

def ask_question():
    question = request.form.get('question').strip()
    if not question:
        return "Please enter a question."
    try:
        response = agent.run(question)
        return response
    except Exception as e:
        return str(e)
