import json
from app.presentation import app

def generate_openapi_spec():
    """Generates the OpenAPI spec and saves it to openapi.json"""
    openapi_schema = app.openapi()
    with open("api/openapi.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    generate_openapi_spec()
    print("Successfully generated openapi.json")
