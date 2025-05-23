from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gena import Gena
import traceback

app = FastAPI()
model = Gena()

class GenerateRequest(BaseModel):
    prompt: str

@app.post("/generate/")
def generate_image(data: GenerateRequest):
    try:
        result = model.generate_from_text(data.prompt)
        return {"images": result}
        #print(f"Received prompt: {data.prompt}")
        # временный фейковый ответ
        #return {"images": ["base64_stub_image_data"]}
    except Exception as e:
        print("Error while generating image:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
