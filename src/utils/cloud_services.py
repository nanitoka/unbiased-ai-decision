import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import bigquery
import json
import uuid

def init_vertex():
    try:
        vertexai.init()
        return True
    except:
        return False

def get_ai_explanation(all_results):
    try:
        model = GenerativeModel("gemini-1.5-flash")
        prompt = f"Analyze these bias metrics: {json.dumps(all_results)}. Provide a clear, 2-sentence explanation of the bias for a non-technical manager."
        ai_response = model.generate_content(prompt)
        return ai_response.text.strip()
    except Exception as e:
        return None

def upload_to_bigquery(data, dataset_name="bias_audit"):
    try:
        client = bigquery.Client()
        table_id = f"{dataset_name}.audit_{uuid.uuid4().hex[:8]}"
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        client.load_table_from_dataframe(data, table_id, job_config=job_config).result()
        return "BigQuery Cloud Engine"
    except:
        return "Local Engine"
