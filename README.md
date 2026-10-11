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
