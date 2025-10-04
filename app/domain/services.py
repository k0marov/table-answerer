import pandas as pd
from fastapi import UploadFile
from app.data import repository, gigachat
import re

def upload_xlsx(file: UploadFile):
    if not file.filename.endswith(".xlsx"):
        return {"error": "Invalid file type. Please upload a .xlsx file."}

    repository.save_xlsx_file(file)

    return {"message": f"File '{file.filename}' uploaded successfully."}

def _get_llm_top_5_from_list(prompt: str, metrics_df: pd.DataFrame):
    """
    Sends a list of metrics to the LLM and asks it to select the top 5.
    """
    # Prepare the list of metrics as a string for the prompt
    metrics_list_str = ""
    for _, row in metrics_df.iterrows():
        # Ensure we handle potential missing data gracefully
        metric_id = row.get('id', 'N/A')
        metric_name = row.get('Наименование показателя', 'N/A')
        metrics_list_str += f"{metric_id}: {metric_name}\n"

    # Construct the prompt for the LLM
    llm_prompt = f"""Ты — умный ассистент, который помогает выбрать наиболее подходящие метрики для задачи пользователя.

Задача пользователя: "{prompt}"

Вот список метрик (в формате id: Наименование показателя):
{metrics_list_str}

Выбери 5 самых релевантных метрик для указанной задачи пользователя. В ответе верни только их id через запятую, без лишних слов. Например: 1,2,3,4,5"""

    # Call the LLM. Context is empty as all info is in the prompt.
    answer = gigachat.get_gigachat_answer(llm_prompt, "")
    
    # Safely parse the LLM's response to extract IDs
    try:
        # Use regex to find all numbers in the response string
        ids = [int(i) for i in re.findall(r'\d+', answer)]
        return ids
    except (ValueError, TypeError):
        # Return an empty list if parsing fails
        return []


def ask_question(prompt: str) -> list:
    """
    Orchestrates the two-stage pipeline to get top 5 metrics.
    """
    data = repository.read_xlsx_file()
    if data is None:
        return {"error": "No data file found. Please upload a .xlsx file first."}

    # Validate that the required columns exist in the DataFrame
    if 'id' not in data.columns or 'Наименование показателя' not in data.columns:
        return {"error": "The .xlsx file must contain 'id' and 'Наименование показателя' columns."}

    batch_size = 200
    all_top_ids = []

    # 1. First Pass: Iterate through the metrics in batches
    for i in range(0, len(data), batch_size):
        batch_df = data.iloc[i:i+batch_size]
        
        # Get the top 5 IDs from the current batch
        top_5_ids_in_batch = _get_llm_top_5_from_list(prompt, batch_df)
        all_top_ids.extend(top_5_ids_in_batch)

    if not all_top_ids:
        return {"answer": "Could not determine any relevant metrics from the document."}

    # Remove duplicate IDs gathered from all batches
    unique_top_ids = list(set(all_top_ids))

    # 2. Second Pass: Rank the collected top metrics
    # Filter the original DataFrame to get the details of the candidate metrics
    combined_metrics_df = data[data['id'].isin(unique_top_ids)]

    if combined_metrics_df.empty:
        return {"answer": "Could not narrow down the relevant metrics."}

    # Get the final top 5 IDs from the combined list
    final_top_5_ids = _get_llm_top_5_from_list(prompt, combined_metrics_df)

    if not final_top_5_ids:
        return {"answer": "Failed to get a final selection of metrics from the candidates."}

    top5_df = data[data['id'].isin(final_top_5_ids)]

    return [str(elem) for elem in top5_df.values.tolist()]
