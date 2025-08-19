from pydantic import BaseModel

class AnalyzeImage(BaseModel):
    file_path : str