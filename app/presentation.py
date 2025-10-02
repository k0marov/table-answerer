from fastapi import FastAPI, APIRouter, UploadFile, File, Query
from app.domain import services

# Add metadata for Swagger UI
app = FastAPI(
    title="Table Answerer API",
    description="API to answer questions based on uploaded XLSX files.",
    version="1.0.0",
)

# Create a router for version 1 of the API
router_v1 = APIRouter(prefix="/api/v1")

@router_v1.post("/upload-xlsx/")
async def upload_xlsx(file: UploadFile = File(...)):
    return services.upload_xlsx(file)

@router_v1.get("/ask")
def ask(prompt: str = Query(..., min_length=1)):
    return services.ask_question(prompt)

@router_v1.get("/status")
def get_status():
    return {"status": "ok"}

# Include the versioned router in the main app
app.include_router(router_v1)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Table Answerer API. Visit /docs for API documentation."}