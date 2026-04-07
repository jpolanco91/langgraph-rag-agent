# LangGraph RAG Agent

## Description.

This is a LangGraph/LangChain AI agent powered by Google AI LLMs and MilvusDB Vector database that answers you questions about the PDF related to the Stock Market Performance in 2024.

  

## Steps to install.

  
#### _Creating .env file_

Before trying to run the agent we must create a `.env` file in the project's root folder in order to hold the environment variables needed for the project. These environment variables are:

-  `GOOGLE_API_KEY` this one holds the API Key for google cloud AI services, like the Gemini LLM.

-  `MILVUS_DB_USER` this one holds the user name for the MilvusDB Vector database.

-  `MILVUS_DB_PASS` this one holds the password for the MilvusDB Vector database.



**Note:** the reason we are setting `MILVUS_DB_USER` and `MILVUS_DB_PASS` is because we're using the MilvusDB server which is containerized in this app.

1. We create an empty `.env` file at the project's root directory.
2. We set `GOOGLE_API_KEY=your_google_api_key` on the first line.
3. Since we're running this locally, we will set `MILVUS_DB_USER=root` and `MILVUS_DB_PASS=Milvus`

#### _Installing dependencies_

To install dependencies run: `$ pip install -r requirements.txt`
 


### Steps to run.

  

1. Change to the app's directory: `$ cd rag-agent-docsearch-app/`

2. If you have Docker run: `$ docker compose up -d` or if you have Podman: `$ podman-compose up -d`.

3. Run `$ python websocket_server.py`
