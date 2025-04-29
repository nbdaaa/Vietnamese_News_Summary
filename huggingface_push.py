from huggingface_hub import HfApi
import os

api = HfApi(token="HF_TOKEN")
api.upload_folder(
    folder_path="data",
    repo_id="nbdaaa/Vietnamese_Newspaper_Summarization",
    repo_type="dataset",
)