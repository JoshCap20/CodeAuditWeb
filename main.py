from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse

from models import CodeRequest, Results
from measures import PerformanceAnalyzer

app = FastAPI()

@app.get("/")
def serve_frontend():
    try:
        return FileResponse("./static/index.html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/flamegraph")
def serve_flamegraph():
    try:
        return FileResponse("./static/flamegraph.svg")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/analyze", response_model=Results)
def process_code(request: CodeRequest) -> Results:
    try:
        return PerformanceAnalyzer.measure(request)
    # Except frontend model validation
    # Exception backend model validation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)