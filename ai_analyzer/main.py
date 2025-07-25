from fastapi import FastAPI, HTTPException
from ai_analyzer.schemas import AnalyzeRequest, AnalyzeResponse
from ai_analyzer.agent import analyze_single_param, analyze_text

app = FastAPI()

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    result = analyze_text(req.text)
    return result

@app.post("/analyze_param", response_model=dict)
async def analyze_param(req: AnalyzeRequest, param_code: str):
    allowed_params = {
        "type_of_pipe",
        "diameter_of_pipe",
        "pipe_wall_thickness",
        "volume_tons",
        "timeline",
        "interest_level"
    }

    if param_code not in allowed_params:
        raise HTTPException(status_code=400, detail=f"Недопустимый параметр: {param_code}")

    result = analyze_single_param(req.text, param_code)
    return result

