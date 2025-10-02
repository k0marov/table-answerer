from fastapi import UploadFile
from app.data import repository, gigachat

def upload_xlsx(file: UploadFile):
    if not file.filename.endswith(".xlsx"):
        return {"error": "Invalid file type. Please upload a .xlsx file."}

    repository.save_xlsx_file(file)

    return {"message": f"File '{file.filename}' uploaded successfully."}

def ask_question(prompt: str):
    data = repository.read_xlsx_file()
    if data is None:
        return {"error": "No data file found. Please upload a .xlsx file first."}

    context = data.to_string()
    answer = gigachat.get_gigachat_answer(prompt, context)
    return {"answer": answer}