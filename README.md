# table-answerer 

OpenAPI spec is available at [./api/openapi.json](./api/openapi.json)

### Running

1. `cp .env.example .env`

2. Edit `.env` 

3. `docker compose up --build`

#### Regenerating OpenAPI spec

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `PYTHONPATH="$PYTHONPATH:." python utils/generate_openapi.py`
