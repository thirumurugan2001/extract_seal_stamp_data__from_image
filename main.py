from fastapi import FastAPI
import uvicorn
from model import *
from connectAPI import *
app = FastAPI()

@app.post("/api/extract_seal_stamp_data__from_image")
async def extract_seal_stamp_data(analyzeImage: AnalyzeImage):
    try :
        if not analyzeImage.file_path or not analyzeImage.file_path.strip():
            return {
                "message":"File path cannot be empty",
                "stratusCode": 400,
                "status":False,
                "data":[{}]
            }
        response = extract_seal_stamp_data__from_image(analyzeImage.file_path)
        return response
    except Exception as e:
        print("Error in the createResume",str(e))
        return {
            "message": str(e),
            "stratusCode": 400,
            "status":False,
            "data":[{}]
        }
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)