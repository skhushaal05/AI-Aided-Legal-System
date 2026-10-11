Setup
    -> create python venv -> python -m venv .venv(and activate it)
    -> install requiremnts -> pip install -r requirements.txt
    -> add .env file
    -> install docker  
        -> run docker-compose services
        following commands inside docker ollama cli
        -> ollama pull nomic-embed-text:latest
        -> ollama pull llama3.2:1b

Make sure that Docker is running

To access fast api client:
    -> enter the dir  cd .\api\
    -> fastapi dev main.py
    -> http://127.0.0.1:8000[/docs (for auto documents)] (api acessable at port 8000)

To access qdrant
    -> http://localhost:6333/dashboard
    -> Raw_Law_Extractors > posh > posh_chunking.py # create chunks.
    -> qdrant_script > ingest_chunks.py #store them in qdrant storage.
    ->
    
<div align="center">
  <img src="https://shields.io" alt="Work In Progress" />
  <p><i>This project is a work in progress. Please use with caution as breaking changes may occur.</i></p>
</div>
