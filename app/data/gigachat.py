from langchain_community.chat_models import GigaChat
from app.config import GIGACHAT_CREDENTIALS, GIGACHAT_SCOPE, GIGACHAT_MODEL

def get_gigachat_answer(prompt: str, context: str):
    llm = GigaChat(credentials=GIGACHAT_CREDENTIALS, verify_ssl_certs=False, scope=GIGACHAT_SCOPE, model=GIGACHAT_MODEL)
    return llm.invoke(f"Контекст: {context}\n\nВопрос: {prompt}").content
